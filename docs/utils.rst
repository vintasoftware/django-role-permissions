=====
Utils
=====

Shortcuts
=========

.. function:: get_user_role(user)

Returns the role class of the user.

.. code-block:: python

    from rolepermissions.shortcuts import get_user_role

    role = get_user_role(user)

.. function:: assign_role(user, role)

Assigns a role to the user. Role parameter can be passed as string or role class object.

.. code-block:: python

    from rolepermissions.shortcuts import assign_role

    assign_role(user, 'doctor')

.. function:: remove_role(user)

Remove any role that was assigned to the specified user.

.. code-block:: python
    from rolepermissions.shortcuts import remove_role

    remove_role(user)

.. function:: available_perm_status(user)

Returns a dictionary containg all permissions available to the role of the specified user.
Permissions are the keys of the dictionary, and values are ``True`` or ``False`` indicating if the
permission is granted or not.

.. code-block:: python

    from rolepermissions.shortcuts import available_perm_status

    permissions = available_perm_status(user)

    if permissions['create_medical_record']:
        print 'user can create medical record'

.. function:: grant_permission(user, permission_name)

Grants a permission to a user. Will not grant a permission that is not listed in the role
``available_permissions``.

.. code-block:: python

    from rolepermissions.shortcuts import grant_permission

    grant_permission(user, 'create_medical_record')

.. function:: revoke_permission(user, permission_name)

Revokes a permission.

.. code-block:: python

    from rolepermissions.shortcuts import revoke_permission

    revoke_permission(user, 'create_medical_record')


Permission and role verification
================================

The following functions will always return ``True`` for users with supper_user status.

.. function:: has_role(user, roles)

Receives a user and a role and returns ``True`` if user has the specified role. Roles can be passed as
object, snake cased string representation or inside a list.

.. code-block:: python

    from rolepermissions.verifications import has_role
    from my_project.roles import Doctor

    if has_role(user, [Doctor, 'nurse']):
        print 'User is a Doctor or a nurse'

.. function:: has_permission(user, permission)

Receives a user and a permission and returns ``True`` is the user has ths specified permission.

.. code-block:: python

    from rolepermissions.verifications import has_permission
    from my_project.roles import Doctor
    from records.models import MedicalRecord

    if has_permission(user, 'create_medical_record'):
        medical_record = MedicalRecord(...)
        medical_record.save()

.. _has-object-permission:

.. function:: has_object_permission(checker_name, user, obj)

Receives a string referencing the object permission checker, a user and the object to be verified.

.. code-block:: python

    from rolepermissions.verifications import has_object_permission
    from clinics.models import Clinic

    clinic = Clinic.objects.get(id=1)

    if has_object_permission('access_clinic', user, clinic):
        print 'access granted'


Template tags
=============

To load template tags use:

.. code-block:: python

    {% load permission_tags %}

.. function:: *filter* has_role

Receives a camel case representation of a role or more than one separated by coma.

.. code-block:: python

    {% load permission_tags %}
    {% if user|has_role:'doctor,nurse' %}
        the user is a doctor or a nurse
    {% endif %}

.. function:: *filter* can

Role permission filter.

.. code-block:: python

    {% load permission_tags %}
    {% if user|can:'create_medical_record' %}
        <a href="/create_record">create record</a>
    {% endif %}

.. function:: *tag* can

If no user is passed to the tag, the logged user will be used in the verification.

.. code-block:: python

    {% load permission_tags %}

    {% can "access_clinic" clinic user=user as can_access_clinic %}
    {% if can_access_clinic %}
        <a href="/clinic/1/">Clinic</a>
    {% endif %}
