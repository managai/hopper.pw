Administrator Guide
===================

Creating database
-----------------
::

    python manage.py check
    python manage.py migrate


Creating an admin user
----------------------
 
Run the following command:
::
 
    python manage.py createsuperuser

Enter your desired username and press enter:
::

    Username: admin

You will then be prompted for your desired email address:
::

    Email address: admin@example.com

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first:
::

    Password: **********
    Password (again): *********
    Superuser created successfully.


Add a new domain
----------------

You need an API key to manage domains on DNS server  
Get an API key:

* `Dreamhost <https://panel.dreamhost.com/index.cgi?tree=home.api>`_
* other

visit page /admin/main/domain/add/


