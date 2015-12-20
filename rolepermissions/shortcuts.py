from __future__ import unicode_literals

from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import RolesManager


def get_permission(permission_name):
    user_ct = ContentType.objects.get_for_model(get_user_model())
    permission, created = Permission.objects.get_or_create(content_type=user_ct,
        codename=permission_name)

    return permission


def get_user_role(user):
    if user:
        roles = user.groups.filter(name__in=RolesManager.get_roles_names())
        if roles:
            return RolesManager.retrieve_role(roles[0].name)

    return None


def available_perm_status(user):
    from rolepermissions.verifications import has_permission

    role = get_user_role(user)
    permission_names = role.permission_names_list()

    permission_hash = {}

    for permission_name in permission_names:
        permission_hash[permission_name] = has_permission(user, permission_name)

    return permission_hash


def grant_permission(user, permission_name):
    role = get_user_role(user)

    if role and permission_name in role.permission_names_list():
        permission = get_permission(permission_name)
        user.user_permissions.add(permission)
        return True

    return False


def revoke_permission(user, permission_name):
    role = get_user_role(user)

    if role and permission_name in role.permission_names_list():
        permission = get_permission(permission_name)
        user.user_permissions.remove(permission)
        return True

    return False


def retrieve_role(role_name):
    return RolesManager.retrieve_role(role_name)
