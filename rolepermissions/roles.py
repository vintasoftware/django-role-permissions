from __future__ import unicode_literals

import inspect

from six import add_metaclass

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rolepermissions.utils import camelToSnake, camel_or_snake_to_title
from rolepermissions.exceptions import RoleDoesNotExist


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

    @classmethod
    def get_roles(cls):
        return registered_roles.values()


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
        """
        Assign this role to a user.

        :returns: :py:class:`django.contrib.auth.models.Group` The group for the
            new role.
        """
        group, _created = Group.objects.get_or_create(name=cls.get_name())
        user.groups.add(group)
        permissions_to_add = cls.get_default_true_permissions()
        user.user_permissions.add(*permissions_to_add)

        return group

    @classmethod
    def _get_adjusted_true_permissions(cls, user):
        """
        Get all true permissions for a user excluding ones that
        have been explicitly revoked.
        """
        from rolepermissions.permissions import available_perm_status

        default_true_permissions = set()
        user_permission_states = available_perm_status(user)
        adjusted_true_permissions = set()

        # Grab the default true permissions from each of the user's roles
        for role in get_user_roles(user):
            default_true_permissions.update(role.get_default_true_permissions())

        # For each of those default true permissions, only keep ones
        # that haven't been explicitly revoked
        for permission in default_true_permissions:
            if user_permission_states[permission.codename]:
                adjusted_true_permissions.add(permission)

        return adjusted_true_permissions

    @classmethod
    def remove_role_from_user(cls, user):
        """
        Remove this role from a user.

        WARNING: Any permissions that were explicitly granted to the user
        that are also defined to be granted by this role will be revoked
        when this role is revoked.

        Example:
            >>> class Doctor(AbstractUserRole):
            ...     available_permissions = {
            ...         "operate": False,
            ...     }
            >>>
            >>> class Surgeon(AbstractUserRole):
            ...     available_permissions = {
            ...         "operate": True,
            ...     }
            >>>
            >>> grant_permission(user, "operate")
            >>> remove_role(user, Surgeon)
            >>>
            >>> has_permission(user, "operate")
            False
            >>>

        In the example, the user no longer has the ``"operate"`` permission,
        even though it was set explicitly before the ``Surgeon`` role was removed.
        """

        # Grab the adjusted true permissions before the removal
        current_adjusted_true_permissions = cls._get_adjusted_true_permissions(user)

        group, _created = cls.get_or_create_group()
        user.groups.remove(group)

        # Grab the adjusted true permissions after the removal
        new_adjusted_true_permissions = cls._get_adjusted_true_permissions(user)

        # Remove true permissions that were default granted only by the removed role
        permissions_to_remove = (current_adjusted_true_permissions
                                 .difference(new_adjusted_true_permissions))
        user.user_permissions.remove(*permissions_to_remove)

        return group

    @classmethod
    def permission_names_list(cls):
        available_permissions = getattr(cls, 'available_permissions', {})
        return available_permissions.keys()

    @classmethod
    def get_all_permissions(cls):
        permission_names = list(cls.permission_names_list())
        if permission_names:
            return cls.get_or_create_permissions(permission_names)

        return []

    @classmethod
    def get_default_true_permissions(cls):
        if hasattr(cls, 'available_permissions'):
            permission_names = [
                key for (key, default) in
                cls.available_permissions.items() if default]

            return cls.get_or_create_permissions(permission_names)

        return []

    @classmethod
    def get_or_create_permissions(cls, permission_names):
        user_ct = ContentType.objects.get_for_model(get_user_model())
        permissions = list(Permission.objects.filter(
            content_type=user_ct, codename__in=permission_names).all())

        missing_permissions = set(permission_names) - set((p.codename for p in permissions))
        if len(missing_permissions) > 0:
            for permission_name in missing_permissions:
                permission, created = get_or_create_permission(permission_name)
                if created:  # assert created is True
                    permissions.append(permission)

        return permissions

    @classmethod
    def get_default(cls, permission_name):
        return cls.available_permissions[permission_name]

    @classmethod
    def get_or_create_group(cls):
        return Group.objects.get_or_create(name=cls.get_name())


def get_or_create_permission(codename, name=camel_or_snake_to_title):
    """
    Get a Permission object from a permission name.
    @:param codename: permission code name
    @:param name: human-readable permissions name (str) or callable that takes codename as
                  argument and returns str
    """
    user_ct = ContentType.objects.get_for_model(get_user_model())
    return Permission.objects.get_or_create(content_type=user_ct, codename=codename,
                                            defaults={'name': name(codename) if callable(name) else name})


def retrieve_role(role_name):
    """Get a Role object from a role name."""
    return RolesManager.retrieve_role(role_name)


def get_user_roles(user):
    """Get a list of a users's roles."""
    if user:
        groups = user.groups.all()   # Important! all() query may be cached on User with prefetch_related.
        roles = (RolesManager.retrieve_role(group.name) for group in groups if group.name in RolesManager.get_roles_names())
        return sorted(roles, key=lambda r: r.get_name() )
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
