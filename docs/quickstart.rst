===========
Quick Start
===========

Install
=======

Install from PyPI with ``pip``::

    pip install django-role-permissions


Configure
=========

Add ```rolepermissions``` to you ```INSTALLED_APPS```

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rolepermissions',
        ...
    )


Create a ``roles.py`` file in the same folder as your ``settings.py`` and two roles:

.. code-block:: python

    from rolepermissions.roles import AbstractUserRole

    class Doctor(AbstractUserRole):
        available_permissions = {
            'create_medical_record': True,
        }

    class Nurse(AbstractUserRole):
        available_permissions = {
            'eddit_pacient_file': True,
        }

and add 
