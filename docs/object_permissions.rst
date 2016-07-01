==========================
Object permission checkers
==========================


permissions.py file
===================

You can add a ``permissions.py`` file to each app. This file should contain
registered object permission checker functions.


``my_app/permissions.py``

.. code-block:: python

    from rolepermissions.permissions import register_object_checker
    from my_project.roles import SystemAdmin

    @register_object_checker()
    def access_clinic(role, user, clinic):
        if role == SystemAdmin:
            return True

        if user.clinic == clinic:
            return True

        return False

when requested the object permission checker will receive the role of the user,
the user and the object being verified and should return ``True`` if the permission is granted.


Checking object permission
==========================

Use the :ref:`has_object_permission <has-object-permission>` method to check for object permissions.
