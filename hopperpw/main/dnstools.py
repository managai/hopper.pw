# coding=utf-8
"""
Misc. DNS related code: query, dynamic update, etc.

Usually, higher level code wants to call the add/update/delete functions.
"""

from django.conf import settings

import dns.inet
import dns.name
import dns.resolver
import dns.query
import dns.update
import dns.tsig
import dns.tsigkeyring

import logging
logger = logging.getLogger(__name__)


class SameIpError(ValueError):
    """
    raised if an IP address is already present in DNS and and update was
    requested, but is not needed.
    """


class DnsUpdateError(ValueError):
    """
    raised if DNS update return code is not NOERROR
    """


def get_rdtype(ipaddr):
    """
    Get the record type 'A' or 'AAAA' for this ipaddr.

    :param ipaddr: ip address v4 or v6 (str)
    :return: 'A' or 'AAAA'
    """
    af = dns.inet.af_for_address(ipaddr)
    return 'A' if af == dns.inet.AF_INET else 'AAAA'


def add(fqdn, ipaddr, ttl=60, origin=None):
    """
    intelligent dns adder - first does a lookup on the master server to find
    the current ip and only sends an 'add' if there is no such entry.
    otherwise send an 'upd' if the if we have a different ip.

    :param fqdn: fully qualified domain name (str)
    :param ipaddr: new ip address
    :param ttl: time to live, default 60s (int)
    :raises: SameIpError if new and old IP is the same
    """
    rdtype = get_rdtype(ipaddr)
    try:
        current_ipaddr = query_ns(fqdn, rdtype, origin=origin)
        # check if ip really changed
        ok = ipaddr != current_ipaddr
        action = 'upd'
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        # no dns entry yet, ok
        ok = True
        action = 'add'
    if ok:
        # only send an add/update if the ip really changed as the update
        # causes write I/O on the nameserver and also traffic to the
        # dns slaves (they get a notify if we update the zone).
        update_ns(fqdn, rdtype, ipaddr, action=action, ttl=ttl, origin=origin)
    else:
        raise SameIpError


def delete(fqdn, rdtype=None, origin=None):
    """
    dns deleter

    :param fqdn: fully qualified domain name (str)
    :param rdtype: 'A', 'AAAA' or None (deletes 'A' and 'AAAA')
    """
    if rdtype is not None:
        assert rdtype in ['A', 'AAAA', ]
        rdtypes = [rdtype, ]
    else:
        rdtypes = ['A', 'AAAA']
    for rdtype in rdtypes:
        update_ns(fqdn, rdtype, action='del', origin=origin)


def update(fqdn, ipaddr, ttl=60, origin=None):
    """
    intelligent dns updater - first does a lookup on the master server to find
    the current ip and only sends a dynamic update if we have a different ip.

    :param fqdn: fully qualified domain name (str)
    :param ipaddr: new ip address
    :param ttl: time to live, default 60s (int)
    :raises: SameIpError if new and old IP is the same
    """
    rdtype = get_rdtype(ipaddr)
    try:
        current_ipaddr = query_ns(fqdn, rdtype, origin=origin)
        # check if ip really changed
        ok = ipaddr != current_ipaddr
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        # no dns entry yet, ok
        ok = True
    if ok:
        # only send an update if the ip really changed as the update
        # causes write I/O on the nameserver and also traffic to the
        # dns slaves (they get a notify if we update the zone).
        update_ns(fqdn, rdtype, ipaddr, action='upd', ttl=ttl, origin=origin)
    else:
        raise SameIpError


def query_ns(qname, rdtype, origin=None):
    """
    query a dns name from our master server

    :param qname: the query name
    :type qname: dns.name.Name object or str
    :param rdtype: the query type
    :type rdtype: int or str
    :return: IP (as str)
    """
    origin, name = parse_name(qname, origin)
    origin_str = str(origin)
    nameserver = get_ns_info(origin_str)[0]
    resolver = dns.resolver.Resolver(configure=False)
    # we do not configure it from resolv.conf, but patch in the values we
    # want into the documented attributes:
    resolver.nameservers = [nameserver, ]
    resolver.search = [dns.name.from_text(settings.BASEDOMAIN), ]
    answer = resolver.query(qname, rdtype)
    return str(list(answer)[0])


def parse_name(fqdn, origin=None):
    """
    Parse a fully qualified domain name into a relative name
    and a origin zone. Please note that the origin return value will
    have a trailing dot.

    :param fqdn: fully qualified domain name (str)
    :param origin: origin zone (optional, str)
    :return: origin, relative name (both dns.name.Name)
    """
#    from .models import Domain
#    for d in Domain.objects.all():
#        origin = d.domain[0]
#        if not origin[0] == '.':
#            origin = '.' + origin
#        i = fqdn.rfind(origin)
#        if not i == -1:
#            return dns.name.from_text(d.domain), dns.name.from_text(fqdn[:i + 1])
    fqdn = dns.name.from_text(fqdn)
    if origin is None:
        origin = dns.resolver.zone_for_name(fqdn)
        rel_name = fqdn.relativize(origin)
    else:
        origin = dns.name.from_text(origin)
        rel_name = fqdn - origin
    return origin, rel_name


def get_ns_info(origin):
    """
    Get the master nameserver for the <origin> zone, the key needed
    to update the zone and the key algorithm used.

    :param origin: zone we are dealing with, must be with trailing dot
    :return: master nameserver, update key, update algo
    """
    from .models import Domain
    d = Domain.objects.get(domain=origin.rstrip('.'))
    algorithm = getattr(dns.tsig, d.nameserver_update_algorithm)
    return d.nameserver_ip, d.nameserver_update_key, algorithm


def update_ns(fqdn, rdtype='A', ipaddr=None, origin=None, action='upd', ttl=60):
    """
    update our master server

    :param fqdn: the fully qualified domain name to update (str)
    :param rdtype: the record type (default: 'A') (str)
    :param ipaddr: ip address (v4 or v6), if needed (str)
    :param origin: the origin zone to update (default; autodetect) (str)
    :param action: 'add', 'del' or 'upd'
    :param ttl: time to live for the added/updated resource, default 60s (int)
    :return: dns response
    """
    assert action in ['add', 'del', 'upd', ]
    origin, name = parse_name(fqdn, origin)
    origin_str = str(origin)
    nameserver, key, algo = get_ns_info(origin_str)
    upd = dns.update.Update(origin,
                            keyring=dns.tsigkeyring.from_text({origin_str: key}),
                            keyalgorithm=algo)
    if action == 'add':
        assert ipaddr is not None
        upd.add(name, ttl, rdtype, ipaddr)
    elif action == 'del':
        upd.delete(name, rdtype)
    elif action == 'upd':
        assert ipaddr is not None
        upd.replace(name, ttl, rdtype, ipaddr)
    logger.debug("performing %s for name %s and origin %s with rdtype %s and ipaddr %s" % (
        action, name, origin, rdtype, ipaddr))
    try:
        response = dns.query.tcp(upd, nameserver)
        return response
    except EOFError as e: 
        logger.error("EOFError [%s] - zone: %s" % (str(e), origin, ))
        #set_ns_availability(domain, False)
        raise DnsUpdateError("EOFError")
