=================
Admin Integration
=================

Use Django User Admin Site to manage roles and permissions interactively.


Permission Names
================

Permissions defined in ``roles.py`` are given 'human-friendly' names.

All such permissions are assigned to the ``auth | user`` Content Type.

Permission names are a Title Case version of the snake_case or camelCase permission codename, so...

* ``create_medical_record``  is named ``auth | user | Create Medical Record``
* ``enterSurgery``  is named ``auth | user | Enter Surgery``


.. _rolepermissions-useradmin:

RolePermissions User Admin
==========================

Assign / remove roles when editing Users in the Django User Admin Site.

.. function:: RolePermissionsUserAdmin

    Custom ``django.contrib.auth.admin.UserAdmin`` that essentially adds the following logic. To be used with standard django User model:

    * ``remove_role(user, group)`` is called for each Group, removed via the Admin, that represents a role.
    * ``assign_role(user, group)`` is called for each Group, added via the Admin, that represents a role.

    Opt-in with ``setting``: :ref:`ROLEPERMISSIONS_REGISTER_ADMIN <register-user-admin-setting>` = True

.. function:: RolePermissionsUserAdminMixin

    Mixin the functionality of ``RolePermissionsUserAdmin`` to your own custom ``UserAdmin`` class. To be used with custom User model:


    .. code-block:: python

        class MyCustomUserAdmin(RolePermissionsUserAdminMixin, django.contrib.auth.admin.UserAdmin):
            ...

.. warning:: ``remove_role`` removes every permission associated with a removed ``Group``,
    regardless of how those permissions were originally assigned.
    See :ref:`remove_role() <remove-role>`


Management Commands
===================

.. code-block:: shell

    django-admin sync_roles

Ensures that ``django.contrib.auth.models`` ``Group`` and ``Permission`` objects exist
for each role defined in ``roles.py``

This makes the roles and permissions defined in code immediately acccessible via the Django User Admin

.. note:: ``sync_roles`` never deletes a ``Group`` or ``Permission``.

   If you remove a role or permission from ``roles.py``, the corresponding ``Group`` / ``Persission``
   continues to exist until it is manually removed.

.. code-block:: shell

    django-admin sync_roles --reset_user_permissions

Additionally, update every User's permissions to ensure they include all those defined by their current roles.

.. warning:: ``--reset_user_permissions`` is primarily intended for development, not production!

    Changing which permissions are associated with a role in ``roles.py`` does NOT change any User's actual permissions!
    ``--reset_user_permissions`` simply clears each User's roles and then re-assign them.
    This guarantees that Users will have all permissions defined by their role(s) in ``roles.py``,
    but in no way does this imply that any permissions previously granted to the User have been revoked!
