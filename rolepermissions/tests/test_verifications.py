
from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.verifications import has_role, has_permission, has_object_permission
from rolepermissions.permissions import register_object_checker
from rolepermissions.models import UserPermission


class Role1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }

class Role2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }

class Role3(AbstractUserRole):
    role_name = 'new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class HasRoleTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())

        Role1.assign_role_to_user(self.user)

    def test_user_has_Role1(self):
        user = self.user

        self.assertTrue(has_role(user, Role1))

    def test_user_does_not_have_Role2(self):
        user = self.user

        self.assertFalse(has_role(user, Role2))

    def test_user_has_Role1_or_Role2(self):
        user = self.user

        self.assertTrue(has_role(user, [Role1, Role2]))

    def test_has_role_by_name(self):
        user = self.user

        self.assertTrue(has_role(user, 'role1'))

    def test_user_has_Role1_or_Role3_by_name(self):
        user = self.user

        Role3.assign_role_to_user(user)

        self.assertTrue(has_role(user, ['role1', 'new_name']))

    def test_not_existent_role(self):
        user = self.user

        self.assertFalse(has_role(user, 'not_a_role'))

    def test_none_user_param(self):
        self.assertFalse(has_role(None, 'role1'))


class HasPermissionTests(TestCase):
    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())

        Role1.assign_role_to_user(self.user)

    def test_has_Role1_permission(self):
        user = self.user

        self.assertTrue(has_permission(user, 'permission1'))

    def test_dos_not_have_Role1_permission(self):
        user = self.user

        Role1.assign_role_to_user(user)

        self.assertFalse(has_permission(user, 'permission3'))

    def test_creates_permission_when_not_existent(self):
        user = self.user

        class Role4(AbstractUserRole):
            available_permissions = {
                'the_permission': True
            }
        RolesManager.register_role(Role4)

        Role4.assign_role_to_user(user)

        Role4.available_permissions = { 'different_one': True }

        self.assertTrue(has_permission(user, 'different_one'))

        permission = UserPermission.objects.get(user=user, permission_name='different_one')

        self.assertTrue(permission.is_granted)

    def test_does_not_creates_if_permission_does_not_exists_in_role(self):
        user = self.user

        Role1.assign_role_to_user(user)

        self.assertFalse(has_permission(user, 'different_permission'))

        try:
            permission = UserPermission.objects.get(user=user, 
                permission_name='different_permission')
        except:
            permission = None

        self.assertIsNone(permission)

    def test_not_existent_permission(self):
        user = self.user

        self.assertFalse(has_permission(user, 'not_a_permission'))

    def test_user_with_no_role(self):
        user = mommy.make(get_user_model())

        self.assertFalse(has_permission(user, 'permission1'))

    def test_none_user_param(self):
        self.assertFalse(has_permission(None, 'role1'))


class HasObjectPermissionTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())

        Role1.assign_role_to_user(self.user)

        @register_object_checker()
        def obj_checker(role, user, obj):
            return obj and True

    def test_has_object_permission(self):
        user = self.user

        self.assertTrue(has_object_permission('obj_checker', user, True))

    def test_does_not_have_object_permission(self):
        user = self.user

        self.assertFalse(has_object_permission('obj_checker', user, False))
