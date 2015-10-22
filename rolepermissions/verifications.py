from __future__ import unicode_literals

import inspect

from django.core.exceptions import ObjectDoesNotExist

from rolepermissions.roles import RolesManager
from rolepermissions.permissions import PermissionsManager
from rolepermissions.shortcuts import get_user_role, get_permission


def has_role(user, roles):
    if user and user.is_superuser:
        return True

    if not isinstance(roles, list):
        roles = [roles]

    normalized_roles = []
    for role in roles:
        if not inspect.isclass(role):
            role = RolesManager.retrieve_role(role)

        normalized_roles.append(role)

    try:
        user_role = get_user_role(user)
    except ObjectDoesNotExist:
        return False

    if not user_role:
        return False

    return user_role in normalized_roles


def has_permission(user, permission_name):
    if user and user.is_superuser:
        return True

    role = get_user_role(user)

    if role and permission_name in role.permission_names_list():
        permission = get_permission(permission_name)

        if permission in user.user_permissions.all():
            return True

    return False


def has_object_permission(checker_name, user, obj):
    if user.is_superuser:
        return True

    checker = PermissionsManager.retrieve_checker(checker_name)
    role = get_user_role(user)

    return checker(role, user, obj)
