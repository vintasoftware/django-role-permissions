
import inspect
import re

from django.core.exceptions import ObjectDoesNotExist

from rolepermissions.models import UserRole, UserPermission


def camelToSnake(s):
    """ 
    https://gist.github.com/jaytaylor/3660565
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    _underscorer2 = re.compile('([a-z0-9])([A-Z])')

    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


class RolesManager(object):
    _roles = {}

    @classmethod
    def register_role(cls, role):
        cls._roles[role().get_name()] = role

    @classmethod
    def get_roles(cls):
        return cls._roles

    @classmethod
    def retrieve_role(cls, role_name):
        if role_name in cls._roles:
            return cls._roles[role_name]


class AbstractUserRole(object):

    @classmethod
    def get_name(cls):
        if hasattr(cls, 'role_name'):
            return cls.role_name

        return camelToSnake(cls.__name__)

    @classmethod
    def assign_role_to_user(cls, user):
        try:
            user_role = UserRole.objects.get(user=user)
        except ObjectDoesNotExist:
            user_role = None

        UserPermission.objects.filter(user=user).delete()

        if not user_role:
            user_role = UserRole(user=user)

        user_role.role_name = cls.get_name()
        user_role.save()

        user.role = user_role

        cls.assign_default_permissions(user)

        return user_role

    @classmethod
    def assign_default_permissions(cls, user):
        role_permissions = cls.available_permissions
        for permission in role_permissions:
            UserPermission.objects.get_or_create(
                user=user, permission_name=permission,
                is_granted=role_permissions[permission])

    @classmethod
    def permission_list(cls):
        return cls.available_permissions.keys()

    @classmethod
    def get_default(cls, permission_name):
        return cls.available_permissions[permission_name]

