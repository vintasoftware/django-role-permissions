from __future__ import unicode_literals

import inspect

from django.conf import settings
from rolepermissions.roles import (
    RolesManager, get_user_roles)
from rolepermissions.permissions import (
    PermissionsManager, available_perm_names)


def has_role(user, roles):
    """Check if a user has any of the given roles."""
    if _check_superpowers(user):
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
    if _check_superpowers(user):
        return True

    return permission_name in available_perm_names(user)

def has_object_permission(checker_name, user, obj):
    """Check if a user has permission to perform an action on an object."""
    if _check_superpowers(user):
        return True

    checker = PermissionsManager.retrieve_checker(checker_name)
    user_roles = get_user_roles(user)

    if not user_roles:
        user_roles = [None]

    return any([checker(user_role, user, obj) for user_role in user_roles])


def _check_superpowers(user):
    """
    Check if user is superuser and should have superpowers.

    Default is true to maintain backward compatibility.
    """
    key = 'ROLEPERMISSIONS_SUPERUSER_SUPERPOWERS'

    superpowers = getattr(settings, key, True)
    if not superpowers:
        return False

    return user and user.is_superuser
