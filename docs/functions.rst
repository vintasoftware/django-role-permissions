=========
Functions
=========

Shortcuts
=========

.. function:: get_user_role(user)

.. function:: get_user_permissions(user)
    
Returns a dictionary containg all permissions available to the role of the specified user. 
Permissions are the keys of the dictionary, and values are ```True``` or ```False``` indicating if the 
permission is granted or not.

.. function:: grant_permission(user, permission_name):

Permission and role verification
================================

.. function:: has_role(user, roles)

Receives a user and a role and returns ```True``` if user has the specified role. Roles can be passed as 
object, camel cased string representation or inside a list.

.. code-block:: python

    from rolepermissions.verifications import has_role
    from my_project.roles import Doctor

    if has_role(user, [Doctor, 'nurse']):
        print 'User is a Doctor or a nurse'

.. function:: has_permission(user, permission)

Receives a user and a permission and returns ```True``` is the user has ths specified permission.

.. code-block:: python

    from rolepermissions.verifications import has_permission
    from my_project.roles import Doctor
    from records.models import MedicalRecord

    if has_permission(user, 'create_medical_record'):
        medical_record = MedicalRecord(...)
        medical_record.save()

.. function:: has_object_permission(checker_name, user, obj)

Receives a string referencing the object permission checker, a user and the object to be verified.

.. code-block:: python

    from rolepermissions.verifications import has_object_permission
    from clinics.models import Clinic

    clinic = Clinic.objects.get(id=1)

    if has_object_permission('access_clinic', user, clinic):
        print 'access permited'


Template tags
=============


