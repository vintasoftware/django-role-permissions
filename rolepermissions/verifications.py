
import inspect

from django.core.exceptions import ObjectDoesNotExist

from rolepermissions.roles import RolesManager
from rolepermissions.permissions import PermissionsManager
from rolepermissions.shortcuts import get_user_role
from rolepermissions.models import UserPermission


def has_role(user, roles):
    if user.is_superuser:
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
    if user.is_superuser:
        return True

    role = get_user_role(user)

    if role and permission_name in role.permission_list():
        try:
            permission = UserPermission.objects.get(user=user, 
                permission_name=permission_name)
            return permission.is_granted
        except ObjectDoesNotExist:
            permission = UserPermission(user=user, 
                permission_name=permission_name, 
                is_granted=role.get_default(permission_name))
            permission.save()
            return permission.is_granted
            
    return False


def has_object_permission(checker_name, user, obj):
    if user.is_superuser:
        return True

    checker = PermissionsManager.retrieve_checker(checker_name)
    role = get_user_role(user)

    return checker(role, user, obj)
