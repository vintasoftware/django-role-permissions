
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rolepermissions.utils import camelToSnake


class RolesClassRegister(type):
    def __init__(cls, name, bases, nmspc):
        super(RolesClassRegister, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, '_roles'):
            cls._roles = {}
        if not cls in bases:
            cls._roles[cls.get_name()] = cls

    def __iter__(cls):
        return iter(cls._roles)


class RolesManager(object):

    @classmethod
    def retrieve_role(cls, role_name):
        if role_name in AbstractUserRole._roles:
            return AbstractUserRole._roles[role_name]

    @classmethod
    def get_roles_names(cls):
        return [r for r, c in AbstractUserRole._roles.iteritems()]


class AbstractUserRole(object):

    __metaclass__ = RolesClassRegister

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'role_name'):
            return cls.role_name

        return camelToSnake(cls.__name__)

    @classmethod
    def assign_role_to_user(cls, user):
        old_groups = user.groups.all()
        
        if old_groups:
            old_group = old_groups[0] # assumes a user has only one group
            role = RolesManager.retrieve_role(old_group.name)
            permissions_to_remove = Permission.objects.filter(codename__in=role.permission_names_list()).all()
            user.user_permissions.remove(*permissions_to_remove)
            user.groups.clear()

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
        permissions = list(Permission.objects.filter(content_type=user_ct, codename__in=permission_names).all())

        if len(permissions) != len(permission_names):
            for permission_name in permission_names:
                permission, created = Permission.objects.get_or_create(content_type=user_ct, codename=permission_name)
                if created:
                    permissions.append(permission)

        return permissions


    @classmethod
    def get_default(cls, permission_name):
        return cls.available_permissions[permission_name]

