
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import Http404

from model_mommy import mommy

from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.shortcuts import (
    get_user_role, get_user_permissions,
    grant_permission, revoke_permission,
    retrieve_role,
)
from rolepermissions.verifications import has_permission



class ShoRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }

class ShoRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }

class ShoRole3(AbstractUserRole):
    role_name = 'sho_new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class GetUserRoleTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_get_user_role(self):
        user = self.user

        user_role = ShoRole1.assign_role_to_user(user)

        self.assertEquals(get_user_role(user), ShoRole1)

    def test_get_user_role_after_role_change(self):
        user = self.user

        user_role = ShoRole1.assign_role_to_user(user)
        user_role = ShoRole3.assign_role_to_user(user)

        self.assertEquals(get_user_role(user), ShoRole3)

    def test_user_without_role(self):
        user = self.user

        self.assertIsNone(get_user_role(user))

    def tearDown(self):
        RolesManager._roles = {}


class GetUserPermissionsTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.role_class = ShoRole1
        self.user_role = self.role_class.assign_role_to_user(self.user)

    def test_get_user_permissios(self):
        user = self.user

        user_permissions = get_user_permissions(user)

        self.assertEquals(user_permissions, self.role_class.available_permissions)

    def test_after_revoke_permission(self):
        user = self.user
        role_class = self.role_class

        revoke_permission(user, 'permission1')

        user_permissions = get_user_permissions(user)

        self.assertEquals(user_permissions['permission1'], False)


class GrantPermissionTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_grant_permission(self):
        user = self.user
        
        self.assertTrue(grant_permission(user, 'permission4'))

        self.assertTrue(has_permission(user, 'permission4'))

    def test_grat_granted_permission(self):
        user = self.user
        
        self.assertTrue(grant_permission(user, 'permission3'))

        self.assertTrue(has_permission(user, 'permission3'))

    def test_not_allowed_permission(self):
        user = self.user

        self.assertFalse(grant_permission(user, 'permission1'))


class RevokePermissionTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_revoke_permission(self):
        user = self.user
        
        self.assertTrue(revoke_permission(user, 'permission3'))

        self.assertFalse(has_permission(user, 'permission3'))

    def test_revoke_revoked_permission(self):
        user = self.user
        
        self.assertTrue(revoke_permission(user, 'permission4'))

        self.assertFalse(has_permission(user, 'permission4'))

    def test_not_allowed_permission(self):
        user = self.user

        self.assertFalse(revoke_permission(user, 'permission1'))


class RetrieveRole(TestCase):

    def setUp(self):
        pass

    def test_retrive_role1(self):
        self.assertEquals(retrieve_role('sho_role1'), ShoRole1)

    def test_retrive_role2(self):
        self.assertEquals(retrieve_role('sho_role2'), ShoRole2)

    def test_retrive_role3(self):
        self.assertEquals(retrieve_role('sho_new_name'), ShoRole3)

    def test_retrieve_unknowun_role(self):
        role = retrieve_role('unknowun_role')
        self.assertIsNone(role)


