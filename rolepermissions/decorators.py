
from django.core.exceptions import PermissionDenied

from rolepermissions.roles import RolesManager
from rolepermissions.verifications import has_role, has_permission


def has_role_decorator(role):
    def request_decorator(dispatch):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated():
                if has_role(user, role):
                    return dispatch(request, *args, **kwargs)

            raise PermissionDenied
        return wrapper
    return request_decorator


def has_permission_decorator(permission_name):
    def request_decorator(dispatch):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated():
                if has_permission(user, permission_name):
                    return dispatch(request, *args, **kwargs)

            raise PermissionDenied
        return wrapper
    return request_decorator
