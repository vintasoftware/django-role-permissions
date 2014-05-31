===========
Quick Start
===========

Install from PyPI with ``pip``::

    pip install django-role-permissions


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
            'edit_pacient_file': True,
        }

Add a reference to your roles module to your settings:

.. code-block:: python

    ROLEPERMISSIONS_MODULE = 'myapplication.roles'
