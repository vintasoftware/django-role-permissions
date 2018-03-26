from __future__ import unicode_literals

from rolepermissions.exceptions import (
    RolePermissionScopeException, CheckerNotRegistered)
from rolepermissions.roles import get_user_roles, get_or_create_permission


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
    permission_hash = {}
    for perm in user.user_permissions.all():
        permission_hash[(perm.name).lower().replace(" ", "_")] = True
    return permission_hash


def grant_permission(user, permission_name):
    """
    Grant a user a specified permission.

    Permissions are only granted if they are in the scope any of the
    user's roles. If the permission is out of scope,
    a RolePermissionScopeException is raised.
    """
    roles = get_user_roles(user)

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

    for role in roles:
        if permission_name in role.permission_names_list():
            permission = get_permission(permission_name)
            user.user_permissions.remove(permission)
            return

    raise RolePermissionScopeException(
        "This permission isn't in the scope of "
        "any of this user's roles.")
