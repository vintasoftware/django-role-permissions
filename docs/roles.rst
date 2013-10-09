=====
Roles
=====

Roles File
==========

Create a ```roles.py``` file anywere inside your django project and reference it in the project settings file.

```my_project/roles.py```

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

```settings.py```

.. code-block:: python

    ROLEPERMISSIONS_MODULE = 'my_project.roles'

Each class that import's ```AbstractUserRole``` is a role on the project and has a snake case string representation.  
For example: 

.. code-block:: python

    from rolepermissions.roles import AbstractUserRole

    class SystemAdmin(AbstractUserRole):
        available_permissions = {
            'drop_tables': True,
        }

will have the string representation: ```system_admin```.

Avaible Role Permissions
========================

The field ```available_permissions``` lists what permissions the role can be granted. 
The boolean referenced on the ```available_permissions``` dictionary is the default value to the 
refered permission.  


New permissions can be added at any time and users will be granted the default permission value until it's explicitly changed.
