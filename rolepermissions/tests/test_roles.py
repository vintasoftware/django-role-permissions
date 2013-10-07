
from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
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


class AbstractUserRoleTests(TestCase):

    def setUp(self):
        pass

    def test_get_name(self):
        self.assertEquals(Role1.get_name(), 'role1')
        self.assertEquals(Role2.get_name(), 'role2')
        self.assertEquals(Role3.get_name(), 'new_name')

    def test_assign_Role1_default_permissions(self):
        user = mommy.make(get_user_model())

        Role1.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission1', permission_hash)
        self.assertTrue(permission_hash['permission1'])
        self.assertIn('permission2', permission_hash)
        self.assertTrue(permission_hash['permission2'])
        self.assertEquals(len(permissions), 2)

    def test_assign_Role2_default_permissions(self):
        user = mommy.make(get_user_model())

        Role2.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission3', permission_hash)
        self.assertTrue(permission_hash['permission3'])
        self.assertIn('permission4', permission_hash)
        self.assertFalse(permission_hash['permission4'])
        self.assertEquals(len(permissions), 2)

    def test_assign_Role3_default_permissions(self):
        user = mommy.make(get_user_model())

        Role3.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission5', permission_hash)
        self.assertFalse(permission_hash['permission5'])
        self.assertIn('permission6', permission_hash)
        self.assertFalse(permission_hash['permission6'])
        self.assertEquals(len(permissions), 2)

    def test_assign_role_to_user(self):
        user = mommy.make(get_user_model())

        user_role = Role1.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'role1')

    def test_instanciate_role(self):
        user = mommy.make(get_user_model())

        user_role = Role1.assign_role_to_user(user)

        self.assertIsNotNone(user_role.pk)

    def test_change_user_role(self):
        user = mommy.make(get_user_model())

        user_role = Role1.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'role1')

        user_role = Role2.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'role2')

    def test_delete_old_permissions_on_role_change(self):
        user = mommy.make(get_user_model())

        Role1().assign_role_to_user(user)
        
        permissions = UserPermission.objects.filter(user=user)

        permission_names = [n.permission_name for n in permissions]

        self.assertIn('permission1', permission_names)
        self.assertIn('permission2', permission_names)
        self.assertEquals(len(permissions), 2)

        Role2.assign_role_to_user(user)

        permissions = UserPermission.objects.filter(user=user)

        permission_names = [n.permission_name for n in permissions]

        self.assertIn('permission3', permission_names)
        self.assertIn('permission4', permission_names)
        self.assertEquals(len(permissions), 2)


    def test_permission_list(self):
        self.assertIn('permission1', Role1.permission_list())
        self.assertIn('permission2', Role1.permission_list())

        self.assertIn('permission3', Role2.permission_list())
        self.assertIn('permission4', Role2.permission_list())


class RolesManagerTests(TestCase):

    def setUp(self):
        RolesManager._roles = {}

    def test_registering_role(self):
        self.assertNotIn('role1', RolesManager._roles)

        RolesManager.register_role(Role1)

        self.assertIn('role1', RolesManager._roles)

    def test_get_roles(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)

        self.assertTrue(isinstance(RolesManager.get_roles(), dict))
        self.assertEquals(len(RolesManager.get_roles()), 2)

    def test_retrieve_role(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)

        self.assertEquals(RolesManager.retrieve_role('role1'), Role1)
        self.assertEquals(RolesManager.retrieve_role('role2'), Role2)
