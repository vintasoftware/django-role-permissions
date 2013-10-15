
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import Http404

from model_mommy import mommy

from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.shortcuts import (
    get_user_role, get_user_permissions, grant_permission,
    revoke_permission, retrieve_role,
)
from rolepermissions.models import UserPermission
from rolepermissions.verifications import has_permission



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


class GetUserRoleTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())

    def test_get_user_role(self):
        user = self.user

        user_role = Role1.assign_role_to_user(user)

        self.assertEquals(get_user_role(user), Role1)

    def test_get_user_role_after_role_change(self):
        user = self.user

        user_role = Role1.assign_role_to_user(user)
        user_role = Role3.assign_role_to_user(user)

        self.assertEquals(get_user_role(user), Role3)

    def test_user_without_role(self):
        user = self.user

        self.assertIsNone(get_user_role(user))

    def tearDown(self):
        RolesManager._roles = {}


class GetUserPermissionsTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())
        self.user_role = Role2.assign_role_to_user(self.user)

    def test_get_user_permissinons(self):
        user = self.user

        permissions = get_user_permissions(user)

        self.assertIn('permission3', permissions)
        self.assertIn('permission4', permissions)
        self.assertTrue(permissions['permission3'])
        self.assertFalse(permissions['permission4'])
        self.assertEquals(len(permissions), 2)

    def test_creates_when_does_not_exists(self):
        user = self.user

        class Role4(AbstractUserRole):
            available_permissions = {
                'the_permission': True,
            }
        RolesManager.register_role(Role4)

        Role4.assign_role_to_user(user)

        Role4.available_permissions = {
            'the_permission': True,
            'new_permission': True,
        }

        permissions = get_user_permissions(user)

        self.assertIn('the_permission', permissions)
        self.assertIn('new_permission', permissions)
        self.assertTrue(permissions['the_permission'])
        self.assertTrue(permissions['new_permission'])
        self.assertEquals(len(permissions), 2)

        new_permission = UserPermission.objects.get(user=user, permission_name='new_permission')

        self.assertTrue(new_permission.is_granted)

    def test_get_permission_for_user_with_no_role(self):
        user = mommy.make(get_user_model())

        permissions = get_user_permissions(user)

        self.assertEquals(permissions, {})


class GrantPermissionTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())
        self.user_role = Role2.assign_role_to_user(self.user)

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
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

        self.user = mommy.make(get_user_model())
        self.user_role = Role2.assign_role_to_user(self.user)

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
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)
        RolesManager.register_role(Role3)

    def test_retrive_role1(self):
        self.assertEquals(retrieve_role('role1'), Role1)

    def test_retrive_role2(self):
        self.assertEquals(retrieve_role('role2'), Role2)

    def test_retrive_role3(self):
        self.assertEquals(retrieve_role('new_name'), Role3)

    def test_retrieve_unknowun_role(self):
        with self.assertRaises(RoleDoesNotExist):
            retrieve_role('unknowun_role')


