
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole, get_or_create_permission


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

class RolRole4(AbstractUserRole):
    available_permissions = {
        'permission_number_7': True,
        'PermissionNumber8': True,
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

    def test_assign_multiple_roles(self):
        user = mommy.make(get_user_model())

        user_role_1 = RolRole1.assign_role_to_user(user)
        self.assertEquals(user_role_1.name, 'rol_role1')

        user_role_2 = RolRole2.assign_role_to_user(user)
        self.assertEquals(user_role_2.name, 'rol_role2')

        user_groups = user.groups.all()

        self.assertEqual(2, len(user_groups))
        self.assertIn(user_role_1, user_groups)
        self.assertIn(user_role_2, user_groups)

    def test_dont_remove_other_groups(self):
        user = mommy.make(get_user_model())
        other_group = mommy.make(Group)
        user.groups.add(other_group)

        user_role_1 = RolRole1.assign_role_to_user(user)
        self.assertEquals(user_role_1.name, 'rol_role1')

        user_role_2 = RolRole2.assign_role_to_user(user)
        self.assertEquals(user_role_2.name, 'rol_role2')

        RolRole2.remove_role_from_user(user)

        user_groups = user.groups.all()

        self.assertIn(user_role_1, user_groups)
        self.assertIn(other_group, user_groups)

    def test_permission_names_list(self):
        self.assertIn('permission1', RolRole1.permission_names_list())
        self.assertIn('permission2', RolRole1.permission_names_list())

        self.assertIn('permission3', RolRole2.permission_names_list())
        self.assertIn('permission4', RolRole2.permission_names_list())

    def test_permission_labels(self):
        user = mommy.make(get_user_model())

        RolRole4.assign_role_to_user(user)
        permissions = user.user_permissions.all()

        permission_labels = [perm.name for perm in permissions]

        self.assertIn('Permission Number 7', permission_labels)
        self.assertIn('Permission Number8', permission_labels)
        self.assertEquals(len(permissions), 2)


class RolesManagerTests(TestCase):

    def setUp(self):
        pass

    def test_retrieve_role(self):
        self.assertEquals(RolesManager.retrieve_role('rol_role1'), RolRole1)
        self.assertEquals(RolesManager.retrieve_role('rol_role2'), RolRole2)


class GetOrCreatePermissionsTests(TestCase):

    def setUp(self):
        pass

    def test_create_default_named_permission(self):
        perm_snake, _created = get_or_create_permission("my_perm_name1")
        self.assertEqual(perm_snake.name, "My Perm Name1")

        perm_camel, _created = get_or_create_permission("myPermName2")
        self.assertEqual(perm_camel.name, "My Perm Name2")

    def test_create_and_get_named_permission(self) :
        perm1, _created = get_or_create_permission("my_perm_name", name="My Custom Name")
        self.assertEqual(perm1.name, "My Custom Name")

        perm2, _created = get_or_create_permission("my_perm_name", name="My Custom Name")
        self.assertEqual(perm1, perm2)

    def test_create_and_get_specialty_named_permission(self) :
        def name_perm(codename):
            return "Custom-"+codename
        perm, _created = get_or_create_permission("my_perm_name", name_perm)
        self.assertEqual(perm.name, "Custom-my_perm_name")

    def test_backwards_compat_with_unnamed_permission(self) :
        unnamed_perm, _created = get_or_create_permission("my_perm_name", name="")
        self.assertEqual(unnamed_perm.name, "")

        perm, _created = get_or_create_permission("my_perm_name")
        self.assertEqual(unnamed_perm, perm)
