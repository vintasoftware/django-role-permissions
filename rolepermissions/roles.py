from __future__ import unicode_literals

from six import add_metaclass

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rolepermissions.utils import camelToSnake


registered_roles = {}


class RolesManager(object):

    def __iter__(cls):
        return iter(registered_roles)

    @classmethod
    def retrieve_role(cls, role_name):
        if role_name in registered_roles:
            return registered_roles[role_name]

    @classmethod
    def get_roles_names(cls):
        return registered_roles.keys()


class RolesClassRegister(type):

    def __new__(cls, name, parents, dct):
        role_class = super(RolesClassRegister, cls).__new__(cls, name, parents, dct)
        if object not in parents:
            registered_roles[role_class.get_name()] = role_class
        return role_class


@add_metaclass(RolesClassRegister)
class AbstractUserRole(object):

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'role_name'):
            return cls.role_name

        return camelToSnake(cls.__name__)

    @classmethod
    def assign_role_to_user(cls, user):
        """Deletes all of user's previous roles, and removes all permissions
        mentioned in their available_permissions property.

        :returns: :py:class:`django.contrib.auth.models.Group` The group for the
            new role.
        """

        old_groups = user.groups.filter(name__in=registered_roles.keys())

        for old_group in old_groups:  # Normally there is only one, but remove all other role groups
            role = RolesManager.retrieve_role(old_group.name)
            permissions_to_remove = Permission.objects.filter(codename__in=role.permission_names_list()).all()
            user.user_permissions.remove(*permissions_to_remove)
        user.groups.remove(*old_groups)

        group, created = Group.objects.get_or_create(name=cls.get_name())
        user.groups.add(group)
        permissions_to_add = cls.get_default_true_permissions()
        user.user_permissions.add(*permissions_to_add)

        return group

    @classmethod
    def permission_names_list(cls):
        available_permissions = getattr(cls, 'available_permissions', {})
        return [key for (key, value) in available_permissions.items()]

    @classmethod
    def get_default_true_permissions(cls):
        if hasattr(cls, 'available_permissions'):
            permission_names = [key for (key, default) in cls.available_permissions.items() if default]

            return cls.get_or_create_permissions(permission_names)
        else:
            return []

    @classmethod
    def get_or_create_permissions(cls, permission_names):
        user_ct = ContentType.objects.get_for_model(get_user_model())
        permissions = list(Permission.objects.filter(
            content_type=user_ct, codename__in=permission_names).all())

        if len(permissions) != len(permission_names):
            for permission_name in permission_names:
                permission, created = Permission.objects.get_or_create(
                    content_type=user_ct, codename=permission_name)
                if created:
                    permissions.append(permission)

        return permissions

    @classmethod
    def get_default(cls, permission_name):
        return cls.available_permissions[permission_name]
