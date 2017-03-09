from __future__ import unicode_literals

from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from rolepermissions.checkers import has_role, has_permission


def has_role_decorator(role):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated():
                if has_role(user, role):
                    return dispatch(request, *args, **kwargs)
            if hasattr(settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN'):
                return redirect_to_login(request.get_full_path())
            raise PermissionDenied
        return wrapper
    return request_decorator


def has_permission_decorator(permission_name):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated():
                if has_permission(user, permission_name):
                    return dispatch(request, *args, **kwargs)
            if hasattr(settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN'):
                return redirect_to_login(request.get_full_path())
            raise PermissionDenied
        return wrapper
    return request_decorator
