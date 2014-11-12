===========
Quick Start
===========

Install from PyPI with ``pip``::

    pip install django-role-permissions


Add ``rolepermissions`` to you ``INSTALLED_APPS``

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

When you create a new user, set its role using:

.. code-block:: python
    
    >>> user = User.objects.get(id=1)
    >>> Doctor.assign_role_to_user(user)

and check its permissions using

.. code-block:: python
    
    >>> from rolepermissions.verifications import has_permission
    >>>
    >>> has_permission(user, 'create_medical_record')
    True
    >>> has_permission(user, 'edit_pacient_file')
    False
