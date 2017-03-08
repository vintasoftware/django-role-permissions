from __future__ import unicode_literals

import inspect

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

from rolepermissions.roles import RolesManager
from rolepermissions.exceptions import RoleDoesNotExist, RolePermissionScopeException


# Roles


def retrieve_role(role_name):
    """Get a Role object from a role name."""
    return RolesManager.retrieve_role(role_name)


def get_user_roles(user):
    """Get a list of a users's roles."""
    if user:
        roles = user.groups.filter(
            name__in=RolesManager.get_roles_names()).order_by("name")
        return [RolesManager.retrieve_role(role.name) for role in roles]
    else:
        return []


def _assign_or_remove_role(user, role, method_name):
    role_cls = role
    if not inspect.isclass(role):
        role_cls = retrieve_role(role)

    if not role_cls:
        raise RoleDoesNotExist

    getattr(role_cls, method_name)(user)

    return role_cls


def assign_role(user, role):
    """Assign a role to a user."""
    return _assign_or_remove_role(user, role, "assign_role_to_user")


def remove_role(user, role):
    """Remove a role from a user."""
    return _assign_or_remove_role(user, role, "remove_role_from_user")


def clear_roles(user):
    """Remove all roles from a user."""
    roles = get_user_roles(user)

    for role in roles:
        role.remove_role_from_user(user)

    return roles


# Permissions


def get_permission(permission_name):
    """Get a Permission object from a permission name."""
    user_ct = ContentType.objects.get_for_model(get_user_model())
    permission, _created = Permission.objects.get_or_create(
        content_type=user_ct, codename=permission_name)

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
