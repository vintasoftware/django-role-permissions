=====================
Mixins and Decorators
=====================

Decorators
==========

Decorators require that the current logged user attend some permission grant.
They are meant to be used on function based views.

.. function:: has_role_decorator(role)

Accepts the same arguments as ``has_role`` function and raises PermissionDenied in case it returns ``False``.

.. code-block:: python
	
	from rolepermissions.decorators import has_role_decorator

	@has_role_decorator('doctor')
	def my_view(request, *args, **kwargs):
		...


.. function:: has_permission_decorator(permission_name)

Accepts the same arguments as ``has_permission`` function and raises PermissionDenied in case it returns ``False``.

.. code-block:: python
	
	from rolepermissions.decorators import has_permission_decorator

	@has_permission_decorator('create_medical_record')
	def my_view(request, *args, **kwargs):
		...

Mixins
======

Mixins require that the current logged user attend some permission grant.
They are meant to be used on class based views.

.. function:: class HasRoleMixin(object):

.. function:: class HasPermissionsMixin(object):
