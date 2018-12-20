from __future__ import unicode_literals

from rolepermissions.exceptions import (
    RolePermissionScopeException, CheckerNotRegistered)
from rolepermissions.roles import get_user_roles, get_or_create_permission, _clear_user_available_perm_names


class PermissionsManager(object):
    _checkers = {}

    @classmethod
    def register_checker(cls, name, function):
        cls._checkers[name] = function

    @classmethod
    def get_checkers(cls):
        return cls._checkers

    @classmethod
    def retrieve_checker(cls, checker_name):
        if checker_name in cls._checkers:
            return cls._checkers[checker_name]

        raise CheckerNotRegistered('Checker with name %s was not registered' % checker_name)


def register_object_checker(name=None):
    def fuction_decorator(func):
        checker_name = name if name else func.__name__
        PermissionsManager.register_checker(checker_name, func)
    return fuction_decorator


def get_permission(permission_name):
    """Get a Permission object from a permission name."""
    permission, created = get_or_create_permission(permission_name)

    return permission


def available_perm_status(user):
    """
    Get a boolean map of the permissions available to a user
    based on that user's roles.
    """
    roles = get_user_roles(user)
    permission_hash = {}

    for role in roles:
        permission_names = role.permission_names_list()

        for permission_name in permission_names:
            permission_hash[permission_name] = get_permission(
                permission_name) in user.user_permissions.all()

    return permission_hash


def available_perm_names(user):
    """
    Return a list of permissions codenames available to a user, based on that user's roles.
      i.e., keys for all "True" permissions from available_perm_status(user):
       Assert: set(available_perm_names(user)) == set(perm for perm,has_perm in available_perm_status(user) if has_perm)
       Query efficient; especially when prefetch_related('group', 'user_permissions') on user object.
       No side-effects; permissions are not created in DB as side-effect.
    """
    if user is None:
        return []

    try:
        return user._available_perm_names

    except AttributeError:
        roles = get_user_roles(user)
        if roles:
            perm_names = set(p for role in roles for p in role.permission_names_list())
            user._available_perm_names = [p.codename for p in user.user_permissions.all() if p.codename in perm_names]
        else:
            user._available_perm_names = []

    return user._available_perm_names


def grant_permission(user, permission_name):
    """
    Grant a user a specified permission.

    Permissions are only granted if they are in the scope any of the
    user's roles. If the permission is out of scope,
    a RolePermissionScopeException is raised.
    """
    roles = get_user_roles(user)
    _clear_user_available_perm_names(user)

    for role in roles:
        if permission_name in role.permission_names_list():
            permission = get_permission(permission_name)
            user.user_permissions.add(permission)
            return

    raise RolePermissionScopeException(
        "This permission isn't in the scope of "
        "any of this user's roles.")


def revoke_permission(user, permission_name):
    """
    Revoke a specified permission from a user.

    Permissions are only revoked if they are in the scope any of the user's
    roles. If the permission is out of scope, a RolePermissionScopeException
    is raised.
    """
    roles = get_user_roles(user)
    _clear_user_available_perm_names(user)

    for role in roles:
        if permission_name in role.permission_names_list():
            permission = get_permission(permission_name)
            user.user_permissions.remove(permission)
            return

    raise RolePermissionScopeException(
        "This permission isn't in the scope of "
        "any of this user's roles.")
