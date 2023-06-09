from __future__ import unicode_literals

from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login as dj_redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect as dj_redirect

from rolepermissions.checkers import has_role, has_permission
from rolepermissions.utils import user_is_authenticated


def _role_permission_checker(function, subject, redirect_to_login, redirect_url):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user_is_authenticated(user):
                if function(user, subject):
                    return dispatch(request, *args, **kwargs)

            if redirect_url:
                return dj_redirect(redirect_url)

            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(
                    settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            raise PermissionDenied
        return wrapper
    return request_decorator


def has_role_decorator(role, redirect_to_login=None, redirect_url=None):
    return _role_permission_checker(has_role, role, redirect_to_login, redirect_url)


def has_permission_decorator(permission_name, redirect_to_login=None, redirect_url=None):
    return _role_permission_checker(has_permission, permission_name, redirect_to_login, redirect_url)
