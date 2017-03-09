from __future__ import unicode_literals

import inspect

from rolepermissions.roles import (
    RolesManager, get_user_roles)
from rolepermissions.permissions import (
    PermissionsManager, available_perm_status)


def has_role(user, roles):
    """Check if a user has any of the given roles."""
    if user and user.is_superuser:
        return True

    if not isinstance(roles, list):
        roles = [roles]

    normalized_roles = []
    for role in roles:
        if not inspect.isclass(role):
            role = RolesManager.retrieve_role(role)

        normalized_roles.append(role)

    user_roles = get_user_roles(user)

    return any([role in user_roles for role in normalized_roles])


def has_permission(user, permission_name):
    """Check if a user has a given permission."""
    if user and user.is_superuser:
        return True

    return available_perm_status(user).get(permission_name, False)


def has_object_permission(checker_name, user, obj):
    """Check if a user has permission to perform an action on an object."""
    if user and user.is_superuser:
        return True

    checker = PermissionsManager.retrieve_checker(checker_name)
    user_roles = get_user_roles(user)

    return any([checker(user_role, user, obj) for user_role in user_roles])
