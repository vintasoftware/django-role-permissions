
from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.shortcuts import (
    get_user_roles, grant_permission,
    revoke_permission, retrieve_role,
    available_perm_status, assign_role,
    remove_role, clear_roles
)
from rolepermissions.verifications import has_permission
from rolepermissions.exceptions import RoleDoesNotExist, RolePermissionScopeException


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


class ShoRole4(AbstractUserRole):
    available_permissions = {
        'permission1': False,
        'permission3': False,
    }


class AssignRoleTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_assign_role(self):
        user = self.user

        assign_role(user, 'sho_role1')

        self.assertListEqual([ShoRole1], get_user_roles(user))

    def test_assign_role_by_class(self):
        user = self.user

        assign_role(user, ShoRole1)

        self.assertListEqual([ShoRole1], get_user_roles(user))

    def test_assign_invalid_role(self):
        user = self.user

        with self.assertRaises(RoleDoesNotExist):
            assign_role(user, 'no role')

    def test_assign_multiple_roles(self):
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)

        self.assertListEqual([ShoRole1, ShoRole2], get_user_roles(user))


class RemoveRoleTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_remove_role_from_user(self):
        user = self.user

        assign_role(user, ShoRole1)
        remove_role(user, ShoRole1)

        self.assertListEqual([], get_user_roles(user))

    def test_remove_role_from_user_with_multiple_roles(self):
        """Ensure that remove_role() only removes the role specified, not all of the user's roles."""
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)

        remove_role(user, ShoRole2)

        self.assertListEqual([ShoRole3, ShoRole1], get_user_roles(user))

    def test_remove_role_user_isnt_assigned_to(self):
        user = self.user

        remove_role(user, ShoRole1)

        self.assertListEqual([], get_user_roles(user))

    def test_remove_invalid_role(self):
        user = self.user

        with self.assertRaises(RoleDoesNotExist):
            assign_role(user, 'no role')

    def test_remove_role_reinstates_permissions_correctly(self):
        user = self.user

        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)
        assign_role(user, ShoRole4)

        self.assertDictEqual(
            {
                "permission1": False,
                "permission3": True,
                "permission4": False,
                "permission5": False,
                "permission6": False,
            },
            available_perm_status(user)
        )

        remove_role(user, ShoRole2)

        self.assertDictEqual(
            {
                "permission1": False,
                "permission3": False,
                "permission5": False,
                "permission6": False,
            },
            available_perm_status(user)
        )


class ClearRolesTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_clear_roles(self):
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)

        clear_roles(user)

        self.assertListEqual([], get_user_roles(user))


class GetUserRoleTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_get_user_roles(self):
        user = self.user

        ShoRole1.assign_role_to_user(user)

        self.assertListEqual([ShoRole1], get_user_roles(user))

    def test_get_user_roles_multiple_roles(self):
        user = self.user

        ShoRole1.assign_role_to_user(user)
        ShoRole3.assign_role_to_user(user)

        self.assertListEqual([ShoRole3, ShoRole1], get_user_roles(user))

    def test_user_without_role(self):
        user = self.user

        self.assertListEqual([], get_user_roles(user))

    def test_ensure_user_roles_are_in_order(self):
        user = self.user

        assign_role(user, ShoRole2)
        assign_role(user, ShoRole4)
        assign_role(user, ShoRole1)
        assign_role(user, ShoRole3)

        self.assertListEqual([ShoRole3, ShoRole1, ShoRole2, ShoRole4], get_user_roles(user))

    def tearDown(self):
        RolesManager._roles = {}


class AvailablePermStatusTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_permission_hash(self):
        perm_hash = available_perm_status(self.user)

        self.assertTrue(perm_hash['permission3'])
        self.assertFalse(perm_hash['permission4'])

    def test_permission_hash_multiple_groups(self):
        """
        If a user has a permission in any role, that permission should show as True,
        no matter what other roles dictate.
        """
        ShoRole1.assign_role_to_user(self.user)
        ShoRole4.assign_role_to_user(self.user)

        perm_hash = available_perm_status(self.user)

        self.assertTrue(perm_hash['permission1'])
        self.assertTrue(perm_hash['permission2'])
        self.assertTrue(perm_hash['permission3'])
        self.assertFalse(perm_hash['permission4'])

    def test_permission_hash_after_modification(self):
        revoke_permission(self.user, 'permission3')

        perm_hash = available_perm_status(self.user)

        self.assertFalse(perm_hash['permission3'])
        self.assertFalse(perm_hash['permission4'])


class GrantPermissionTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_grant_permission(self):
        user = self.user

        grant_permission(user, 'permission4')

        self.assertTrue(has_permission(user, 'permission4'))

    def test_grat_granted_permission(self):
        user = self.user

        grant_permission(user, 'permission3')

        self.assertTrue(has_permission(user, 'permission3'))

    def test_not_allowed_permission(self):
        user = self.user

        with self.assertRaises(RolePermissionScopeException):
            grant_permission(user, 'permission1')

    def test_not_allowed_permission_multiple_roles(self):
        user = self.user
        ShoRole3.assign_role_to_user(self.user)

        with self.assertRaises(RolePermissionScopeException):
            grant_permission(user, 'permission1')


class RevokePermissionTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_revoke_permission(self):
        user = self.user

        revoke_permission(user, 'permission3')

        self.assertFalse(has_permission(user, 'permission3'))

    def test_revoke_revoked_permission(self):
        user = self.user

        revoke_permission(user, 'permission4')

        self.assertFalse(has_permission(user, 'permission4'))

    def test_not_allowed_permission(self):
        user = self.user

        with self.assertRaises(RolePermissionScopeException):
            revoke_permission(user, 'permission1')

    def test_not_allowed_permission_multiple_roles(self):
        user = self.user
        ShoRole3.assign_role_to_user(self.user)

        with self.assertRaises(RolePermissionScopeException):
            revoke_permission(user, 'permission1')


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
