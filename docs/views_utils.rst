=====================
Mixins and Decorators
=====================

Decorators
==========

Decorators require that the current logged user attend some permission grant.
They are meant to be used on function based views.

.. function:: has_role_decorator(role)

Accepts the same arguments as ``has_role`` function and raises PermissionDenied in case it returns ``False``.
You can pass an optional key word argument ``redirect_to_login`` to overhide the ``ROLEPERMISSIONS_REDIRECT_TO_LOGIN`` setting.

.. code-block:: python

	from rolepermissions.decorators import has_role_decorator

	@has_role_decorator('doctor')
	def my_view(request, *args, **kwargs):
		...


.. function:: has_permission_decorator(permission_name)

Accepts the same arguments as ``has_permission`` function and raises PermissionDenied in case it returns ``False``.
You can pass an optional key word argument ``redirect_to_login`` to overhide the ``ROLEPERMISSIONS_REDIRECT_TO_LOGIN`` setting.

.. code-block:: python

	from rolepermissions.decorators import has_permission_decorator

	@has_permission_decorator('create_medical_record')
	def my_view(request, *args, **kwargs):
		...

Mixins
======

Mixins require that the current logged user attend some permission grant.
They are meant to be used on class based views.

.. function:: class HasRoleMixin(object)

Add ``HasRoleMixin`` mixin to the desired CBV (class based view) and use the ``allowed_roles`` attribute to set the roles that can access the view.
``allowed_roles`` attribute will be passed to ``has_role`` function, and PermissionDenied will be raised in case it returns ``False``.
You can set an optional ``redirect_to_login`` attribute to overhide the ``ROLEPERMISSIONS_REDIRECT_TO_LOGIN`` setting.


.. code-block:: python

	from django.views.generic import TemplateView
	from rolepermissions.mixins import HasRoleMixin

	class MyView(HasRoleMixin, TemplateView):
		allowed_roles = 'doctor'
		...

.. function:: class HasPermissionsMixin(object)

Add ``HasPermissionsMixin`` mixin to the desired CBV (class based view) and use the ``required_permission`` attribute to set the roles that can access the view.
``required_permission`` attribute will be passed to ``has_permission`` function, and PermissionDenied will be raised in case it returns ``False``.
You can set an optional ``redirect_to_login`` attribute to overhide the ``ROLEPERMISSIONS_REDIRECT_TO_LOGIN`` setting.

.. code-block:: python

	from django.views.generic import TemplateView
	from rolepermissions.mixins import HasPermissionsMixin

	class MyView(HasPermissionsMixin, TemplateView):
		required_permission = 'create_medical_record'
		...
