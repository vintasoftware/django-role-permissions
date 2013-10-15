
from django.http import Http404

from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import RolesManager
from rolepermissions.models import UserPermission


def get_user_role(user):
    if hasattr(user, 'role'):
        return RolesManager.retrieve_role(user.role.role_name)
    return None


def get_user_permissions(user):
    role = get_user_role(user)

    permissions = UserPermission.objects.filter(user=user)
    permissions = { p.permission_name: p for p in permissions }

    user_permissions = []
    for permission_name in role.permission_list():
        if permission_name in permissions:
            permission = permissions[permission_name]
        else:
            permission = UserPermission(user=user, 
                permission_name=permission_name, 
                is_granted=role.get_default(permission_name))
            permission.save()
        user_permissions.append(permission)

    permission_hash = { p.permission_name: p.is_granted for p in user_permissions }

    return permission_hash


def grant_permission(user, permission_name):
    user_permissions = get_user_permissions(user)

    if permission_name in user_permissions:
        permission = UserPermission.objects.get(user=user, 
            permission_name=permission_name)

        permission.is_granted = True
        permission.save()

        return True

    return False


def revoke_permission(user, permission_name):
    user_permissions = get_user_permissions(user)

    if permission_name in user_permissions:
        permission = UserPermission.objects.get(user=user, 
            permission_name=permission_name)

        permission.is_granted = False
        permission.save()

        return True

    return False


def retrieve_role(role_name):
    role = RolesManager.retrieve_role(role_name)
    if role is None:
        raise RoleDoesNotExist

    return role
