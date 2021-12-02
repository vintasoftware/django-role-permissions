
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.roles import (
    get_user_roles, retrieve_role,
    assign_role, remove_role, clear_roles
)
from rolepermissions.permissions import (
    grant_permission, revoke_permission,
    available_perm_status, available_perm_names)
from rolepermissions.checkers import has_permission
from rolepermissions.exceptions import (
    RoleDoesNotExist, RolePermissionScopeException)


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
    enter_surgery_room = "enter_surgery_room"
    operate = "operate"

    class Doctor(AbstractUserRole):
        available_permissions = {
            "enter_surgery_room": False,
        }

    class Surgeon(AbstractUserRole):
        available_permissions = {
            "enter_surgery_room": True,
            "operate": True,
        }

    class Anesthesiologist(AbstractUserRole):
        available_permissions = {
            "enter_surgery_room": True,
            "operate": False,
        }

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_remove_role_from_user(self):
        assign_role(self.user, self.Doctor)
        remove_role(self.user, self.Doctor)

        self.assertListEqual([], get_user_roles(self.user))

    def test_remove_role_from_user_with_multiple_roles(self):
        """Ensure that remove_role() only removes the role specified, not all of the user's roles."""
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)
        assign_role(self.user, self.Anesthesiologist)

        remove_role(self.user, self.Doctor)

        self.assertListEqual([self.Anesthesiologist, self.Surgeon], get_user_roles(self.user))

    def test_remove_role_user_isnt_assigned_to(self):
        remove_role(self.user, self.Doctor)

        self.assertListEqual([], get_user_roles(self.user))

    def test_remove_invalid_role(self):
        with self.assertRaises(RoleDoesNotExist):
            assign_role(self.user, 'no role')

    def test_remove_role_reinstates_permissions_correctly_scenario_1(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Remove role: Surgeon

        Expected resulting permissions:
            enter_surgery_room = False
            operate = False
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        remove_role(self.user, self.Surgeon)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_2(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Remove role: Doctor

        Expected resulting permission:
            enter_surgery_room = True
            operate = True
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        remove_role(self.user, self.Doctor)

        self.assertTrue(has_permission(self.user, self.enter_surgery_room))
        self.assertTrue(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_3(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Revoke permission: enter_surgery_room
            Remove role: Surgeon

        Expected resulting permission:
            enter_surgery_room = False
            operate = False
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        revoke_permission(self.user, self.enter_surgery_room)
        remove_role(self.user, self.Surgeon)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_4(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Revoke permission: enter_surgery_room
            Remove role: Doctor

        Expected resulting permission:
            enter_surgery_room = False
            operate = True
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        revoke_permission(self.user, self.enter_surgery_room)
        remove_role(self.user, self.Doctor)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertTrue(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_5(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Grant permission: operate
            Remove role: Surgeon

        Expected resulting permission:
            enter_surgery_room = False
            operate = True
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        grant_permission(self.user, self.operate)
        remove_role(self.user, self.Surgeon)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_6(self):
        """
        Initial Roles:
            Doctor
            Surgeon

        Actions:
            Revoke permission: enter_surgery_room
            Revoke permission: operate
            Remove role: Doctor

        Expected resulting permission:
            enter_surgery_room = False
            operate = False
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)

        revoke_permission(self.user, self.enter_surgery_room)
        revoke_permission(self.user, self.operate)
        remove_role(self.user, self.Doctor)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_7(self):
        """
        Initial Roles:
            Doctor
            Surgeon
            Anesthesiologist

        Actions:
            Remove role: Surgeon

        Expected resulting permission:
            enter_surgery_room = True
            operate = False
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)
        assign_role(self.user, self.Anesthesiologist)

        remove_role(self.user, self.Surgeon)

        self.assertTrue(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_8(self):
        """
        Initial Roles:
            Doctor
            Surgeon
            Anesthesiologist

        Actions:
            Remove role: Doctor

        Expected resulting permission:
            enter_surgery_room = True
            operate = True
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)
        assign_role(self.user, self.Anesthesiologist)

        remove_role(self.user, self.Doctor)

        self.assertTrue(has_permission(self.user, self.enter_surgery_room))
        self.assertTrue(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_9(self):
        """
        Initial Roles:
            Doctor
            Surgeon
            Anesthesiologist

        Actions:
            Revoke permission: enter_surgery_room
            Remove role: Surgeon

        Expected resulting permission:
            enter_surgery_room = False
            operate = False
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)
        assign_role(self.user, self.Anesthesiologist)

        revoke_permission(self.user, self.enter_surgery_room)
        remove_role(self.user, self.Surgeon)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertFalse(has_permission(self.user, self.operate))

    def test_remove_role_reinstates_permissions_correctly_scenario_10(self):
        """
        Initial Roles:
            Doctor
            Surgeon
            Anesthesiologist

        Actions:
            Revoke permission: enter_surgery_room
            Remove role: Doctor

        Expected resulting permission:
            enter_surgery_room = False
            operate = True
        """
        assign_role(self.user, self.Doctor)
        assign_role(self.user, self.Surgeon)
        assign_role(self.user, self.Anesthesiologist)

        revoke_permission(self.user, self.enter_surgery_room)
        remove_role(self.user, self.Doctor)

        self.assertFalse(has_permission(self.user, self.enter_surgery_room))
        self.assertTrue(has_permission(self.user, self.operate))


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

    def test_returns_list(self) :
        user = self.user

        user_roles = get_user_roles(user)
        self.assertEquals(type(user_roles), type([]))

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

    def test_dont_return_non_role_groups(self):
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)
        assign_role(user, ShoRole4)

        other_group = mommy.make(Group)
        user.groups.add(other_group)

        self.assertNotIn(other_group, get_user_roles(user))

    def test_queries_no_prefetch(self):
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)

        fetched_user = get_user_model().objects.get(pk=self.user.pk)
        N = 3
        with self.assertNumQueries(N):  # One query (fetch roles) per call
            for i in range(N):
                user_roles = get_user_roles(fetched_user)

    def test_queries_with_prefetch(self):
        user = self.user

        assign_role(user, ShoRole1)
        assign_role(user, ShoRole2)
        assign_role(user, ShoRole3)

        fetched_user = get_user_model().objects.prefetch_related('groups').get(pk=self.user.pk)
        N = 3
        with self.assertNumQueries(0):  # all data required is cached with fetched_user
            for i in range(N):
                user_roles = get_user_roles(fetched_user)

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


class AvailablePermNamesTests(TestCase):

    def assert_available_perm_names_equals_available_perm_status(self):
        perm_hash = available_perm_status(self.user)
        perm_names = available_perm_names(self.user)

        self.assertEqual( set(perm_names), set(p for p, has_perm in perm_hash.items() if has_perm) )

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.user_role = ShoRole2.assign_role_to_user(self.user)

    def test_permission_names(self):
        self.assert_available_perm_names_equals_available_perm_status()

    def test_permission_names_multiple_groups(self):
        """
        If a user has a permission in any role, that permission should show as True,
        no matter what other roles dictate.
        """
        ShoRole1.assign_role_to_user(self.user)
        ShoRole4.assign_role_to_user(self.user)

        self.assert_available_perm_names_equals_available_perm_status()

    def test_permission_names_after_modification(self):
        revoke_permission(self.user, 'permission3')

        self.assert_available_perm_names_equals_available_perm_status()

    def test_queries_no_prefetch(self):
        fetched_user = get_user_model().objects.get(pk=self.user.pk)
        N = 3
        with self.assertNumQueries(2 * N):  # Two query (fetch roles, fetch permissions) per call
            for i in range(N):
                perm_names = available_perm_names(fetched_user)

    def test_queries_with_prefetch(self):
        fetched_user = get_user_model().objects.prefetch_related('groups', 'user_permissions').get(pk=self.user.pk)
        N = 3
        with self.assertNumQueries(0):  # all data required is cached with fetched_user
            for i in range(N):
                perm_names = available_perm_names(fetched_user)


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
