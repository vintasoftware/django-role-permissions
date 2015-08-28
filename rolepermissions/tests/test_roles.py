
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole


class RolRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }


class RolRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }


class RolRole3(AbstractUserRole):
    role_name = 'new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class AbstractUserRoleTests(TestCase):

    def setUp(self):
        pass

    def test_get_name(self):
        self.assertEquals(RolRole1.get_name(), 'rol_role1')
        self.assertEquals(RolRole2.get_name(), 'rol_role2')
        self.assertEquals(RolRole3.get_name(), 'new_name')

    def test_assign_Role1_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole1.assign_role_to_user(user)
        permissions = user.user_permissions.all()

        permission_names_list = [perm.codename for perm in permissions]

        self.assertIn('permission1', permission_names_list)
        self.assertIn('permission2', permission_names_list)
        self.assertEquals(len(permissions), 2)

    def test_assign_Role2_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole2.assign_role_to_user(user)
        permissions = user.user_permissions.all()

        permission_names_list = [perm.codename for perm in permissions]

        self.assertIn('permission3', permission_names_list)
        self.assertNotIn('permission4', permission_names_list)
        self.assertEquals(len(permissions), 1)

    def test_assign_Role3_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole3.assign_role_to_user(user)
        permissions = user.user_permissions.all()

        permission_names_list = [perm.codename for perm in permissions]

        self.assertNotIn('permission5', permission_names_list)
        self.assertNotIn('permission6', permission_names_list)
        self.assertEquals(len(permissions), 0)

    def test_assign_role_to_user(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertEquals(user_role.name, 'rol_role1')

    def test_instanciate_role(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertIsNotNone(user_role.pk)

    def test_change_user_role(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertEquals(user_role.name, 'rol_role1')

        new_user_role = RolRole2.assign_role_to_user(user)

        self.assertEquals(new_user_role.name, 'rol_role2')
        self.assertIn(new_user_role, user.groups.all())
        self.assertNotIn(user_role, user.groups.all())

    def test_dont_remove_other_groups(self):
        user = mommy.make(get_user_model())
        other_group = mommy.make(Group)
        user.groups.add(other_group)

        user_role = RolRole1.assign_role_to_user(user)

        self.assertEquals(user_role.name, 'rol_role1')

        new_user_role = RolRole2.assign_role_to_user(user)

        self.assertEquals(new_user_role.name, 'rol_role2')
        self.assertIn(new_user_role, user.groups.all())
        self.assertIn(other_group, user.groups.all())
        self.assertNotIn(user_role, user.groups.all())

    def test_delete_old_permissions_on_role_change(self):
        user = mommy.make(get_user_model())

        RolRole1().assign_role_to_user(user)

        permissions = user.user_permissions.all()

        permission_names = [n.codename for n in permissions]

        self.assertIn('permission1', permission_names)
        self.assertIn('permission2', permission_names)
        self.assertEquals(len(permissions), 2)

        RolRole2.assign_role_to_user(user)

        permissions = user.user_permissions.all()

        permission_names = [n.codename for n in permissions]

        self.assertNotIn('permission1', permission_names)
        self.assertNotIn('permission2', permission_names)
        self.assertIn('permission3', permission_names)
        self.assertNotIn('permission4', permission_names)
        self.assertEquals(len(permissions), 1)

    def test_permission_names_list(self):
        self.assertIn('permission1', RolRole1.permission_names_list())
        self.assertIn('permission2', RolRole1.permission_names_list())

        self.assertIn('permission3', RolRole2.permission_names_list())
        self.assertIn('permission4', RolRole2.permission_names_list())


class RolesManagerTests(TestCase):

    def setUp(self):
        pass

    def test_retrieve_role(self):
        self.assertEquals(RolesManager.retrieve_role('rol_role1'), RolRole1)
        self.assertEquals(RolesManager.retrieve_role('rol_role2'), RolRole2)
