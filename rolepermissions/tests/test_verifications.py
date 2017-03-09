
from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy

from rolepermissions.roles import AbstractUserRole
from rolepermissions.checkers import has_role, has_permission, has_object_permission
from rolepermissions.permissions import register_object_checker


class VerRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }

class VerRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }

class VerRole3(AbstractUserRole):
    role_name = 'ver_new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class HasRoleTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        VerRole1.assign_role_to_user(self.user)

    def test_user_has_VerRole1(self):
        user = self.user

        self.assertTrue(has_role(user, VerRole1))

    def test_user_does_not_have_VerRole2(self):
        user = self.user

        self.assertFalse(has_role(user, VerRole2))

    def test_user_has_VerRole1_or_VerRole2(self):
        user = self.user

        self.assertTrue(has_role(user, [VerRole1, VerRole2]))

    def test_has_role_by_name(self):
        user = self.user

        self.assertTrue(has_role(user, 'ver_role1'))

    def test_user_has_VerRole1_or_VerRole3_by_name(self):
        user = self.user

        VerRole3.assign_role_to_user(user)

        self.assertTrue(has_role(user, ['ver_role1', 'ver_new_name']))

    def test_not_existent_role(self):
        user = self.user

        self.assertFalse(has_role(user, 'not_a_role'))

    def test_none_user_param(self):
        self.assertFalse(has_role(None, 'ver_role1'))


class HasPermissionTests(TestCase):
    def setUp(self):
        self.user = mommy.make(get_user_model())

        VerRole1.assign_role_to_user(self.user)

    def test_has_VerRole1_permission(self):
        user = self.user

        self.assertTrue(has_permission(user, 'permission1'))

    def test_dos_not_have_VerRole1_permission(self):
        user = self.user

        VerRole1.assign_role_to_user(user)

        self.assertFalse(has_permission(user, 'permission3'))

    def test_not_existent_permission(self):
        user = self.user

        self.assertFalse(has_permission(user, 'not_a_permission'))

    def test_user_with_no_role(self):
        user = mommy.make(get_user_model())

        self.assertFalse(has_permission(user, 'permission1'))

    def test_none_user_param(self):
        self.assertFalse(has_permission(None, 'ver_role1'))


class HasObjectPermissionTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        VerRole1.assign_role_to_user(self.user)

        @register_object_checker()
        def obj_checker(role, user, obj):
            return obj and True

    def test_has_object_permission(self):
        user = self.user

        self.assertTrue(has_object_permission('obj_checker', user, True))

    def test_does_not_have_object_permission(self):
        user = self.user

        self.assertFalse(has_object_permission('obj_checker', user, False))
