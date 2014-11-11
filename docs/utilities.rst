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

	@has_role_decorator()
	def my_view(request, *args, **kwargs):


.. function:: has_permission_decorator(permission_name):


Mixins
======

Mixins require that the current logged user attend some permission grant.
They are meant to be used on class based views.

.. function:: class HasRoleMixin(object):

.. function:: class HasPermissionsMixin(object):
