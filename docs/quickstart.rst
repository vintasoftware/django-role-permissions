===========
Quick Start
===========

Create a ``roles.py`` file in the same folder as your ``settings.py`` and two roles:

.. code-block:: python

    from rolepermissions.roles import AbstractUserRole

    class Doctor(AbstractUserRole):
        available_permissions = {
            'create_medical_record': True,
        }

    class Nurse(AbstractUserRole):
        available_permissions = {
            'edit_patient_file': True,
        }

Add a reference to your roles module to your settings:

.. code-block:: python

    ROLEPERMISSIONS_MODULE = 'myapplication.roles'

When you create a new user, set its role using:

.. code-block:: python

    >>> from rolepermissions.roles import assign_role
    >>> user = User.objects.get(id=1)
    >>> assign_role(user, 'doctor')

and check its permissions using

.. code-block:: python

    >>> from rolepermissions.checkers import has_permission
    >>>
    >>> has_permission(user, 'create_medical_record')
    True
    >>> has_permission(user, 'edit_patient_file')
    False

You can also change users permissions:

.. code-block:: python

    >>> from rolepermissions.permissions import grant_permission, revoke_permission
    >>>
    >>> revoke_permission(user, 'create_medical_record')
    >>> grant_permission(user, 'edit_patient_file')
    >>>
    >>> has_permission(user, 'create_medical_record')
    False
    >>> has_permission(user, 'edit_patient_file')
    True
