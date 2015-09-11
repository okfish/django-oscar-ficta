=============================
django-oscar-ficta
=============================

Persona ficta (juristic person) management for the Oscar E-commerce Project.

Documentation
-------------

The full documentation will be at https://django-oscar-ficta.readthedocs.org sometimes :)

Quickstart
----------

Install django-oscar-ficta::

    pip install -e git+https//github.com/okfish/django-oscar-ficta/django-oscar-ficta.git#egg=django-oscar-ficta

Then use it in a project::

    * add 'oscar_ficta' and 'invoice' to INSTALLED_APPS;
    * migrate database;
    * TODO: install sandbox project

Features
--------

* Select _current_ Juristic Person to deal with
* Checkout as Juristic Person and save all reqired attributes in the database
* Forms with VAT and BIC validation using django-internationalflavor, customized for localized use (e.g. in Russia). Note: we using our own branch with some additions not PRed yet  


Requirements
------------
	django-oscar
	django-internationalflavor

TODO
* Basic CRM functions 
* django-oscar-accounts integration
* DaData.ru integration

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
