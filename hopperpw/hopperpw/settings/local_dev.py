# coding=utf-8

"""
Common settings and globals for all environments.

Do not use this setting directly! Instead import these and override DATABASE settings.
"""

# ######### IMPORT CONFIGURATION
from __future__ import absolute_import

from .base import *
# ######### END IMPORT CONFIGURATION


# ######### PATH CONFIGURATION
# ######### END PATH CONFIGURATION


# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    # 'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = ['127.0.0.1']
# ######### END DEBUG CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ######### END EMAIL CONFIGURATION


# ######### CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# ######### END CACHE CONFIGURATION


# ######### MANAGER CONFIGURATION
# ######### END MANAGER CONFIGURATION


# ######### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'hopperpw.sqlite',
    }
}
# ######### END DATABASE CONFIGURATION


# ######### GENERAL CONFIGURATION
# ######### END GENERAL CONFIGURATION


# ######### MEDIA CONFIGURATION
# ######### END MEDIA CONFIGURATION


# ######### STATIC FILE CONFIGURATION
# ######### END STATIC FILE CONFIGURATION


# ######### SECRET CONFIGURATION
SECRET_KEY = 'secretkey'

SESSION_COOKIE_SECURE = False
# ######### END SECRET CONFIGURATION


# ######### SITE CONFIGURATION
ALLOWED_HOSTS = []
# ######### END SITE CONFIGURATION


# ######### FIXTURE CONFIGURATION
# ######### END FIXTURE CONFIGURATION


# ######### TEMPLATE CONFIGURATION
# ######### END TEMPLATE CONFIGURATION


# ######### MIDDLEWARE CONFIGURATION
# ######### END MIDDLEWARE CONFIGURATION


# ######### URL CONFIGURATION
# ######### END URL CONFIGURATION


# ######### APP CONFIGURATION
# ######### END APP CONFIGURATION


# ######### LOGGING CONFIGURATION
# ######### END LOGGING CONFIGURATION


# ######### WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = None
# ######### END WSGI CONFIGURATION


# ######### MISCELLANEA CONFIGURATION
SECURE_PROXY_SSL_HEADER = None
ENABLE_TRACKING = True
ENABLE_ADS = True
# ######### END MISCELLANEA CONFIGURATION


# ######### DJANGO ALLAUTH
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
# ######### END DJANGO ALLAUTH

# ######### CELERY CONFIGURATION
# ######### END CELERY CONFIGURATION

# ######### TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
)
# ######### END TOOLBAR CONFIGURATION

try:
    from .local_settings import *
except ImportError as e:
    import logging
    logging.info('Could not find local settings. If you want to use custom settings add a local_settings.py in the'
                 'settings directory')
