=========
Utilities
=========

Decorators
==========

Decorators require that the current logged user attend some permission grant.
They are meant to be used on function based views.

.. function:: has_role_decorator(role):


.. function:: has_permission_decorator(permission_name):


Mixins
======

Mixins require that the current logged user attend some permission grant.
They are meant to be used on class based views.

.. function:: class HasRoleMixin(object):

.. function:: class HasPermissionsMixin(object):
