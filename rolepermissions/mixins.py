from __future__ import unicode_literals

from rolepermissions.decorators import has_permission_decorator, has_role_decorator


class HasRoleMixin(object):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        roles = self.allowed_roles
        return (has_role_decorator(roles)
                (super(HasRoleMixin, self).dispatch)
                (request, *args, **kwargs))


class HasPermissionsMixin(object):
    required_permission = ''

    def dispatch(self, request, *args, **kwargs):
        permission = self.required_permission
        return (has_permission_decorator(permission)
                (super(HasPermissionsMixin, self).dispatch)
                (request, *args, **kwargs))
