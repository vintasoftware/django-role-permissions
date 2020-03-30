from collections import namedtuple
from django.core.management import call_command
from django.test import TestCase

try:
    # django 3 don't have django.utils.six
    from django.utils.six import StringIO
except ImportError:
    from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from model_mommy import mommy

from rolepermissions.roles import AbstractUserRole, get_user_roles
from rolepermissions.admin import RolePermissionsUserAdminMixin


class AdminRole1(AbstractUserRole):
    available_permissions = {
        'admin_perm1': True,
        'admin_perm2': False,
    }


class UserAdminMixinTest(TestCase):

    class UserAdminMock:
        def save_related(self, request, form, formsets, change):
            pass

    class CustomUserAdminMock(RolePermissionsUserAdminMixin, UserAdminMock):
        pass

    FormMock = namedtuple('FormMock', ['instance', ])

    def setup(self):
        pass

    def test_admin_save_related_syncs_roles(self):
        user = mommy.make(get_user_model())
        grp1 = mommy.make(Group)
        grp2 = mommy.make(Group, name=AdminRole1.get_name())
        user.groups.add(grp1)
        user.groups.add(grp2)
        form = self.FormMock(instance=user)
        self.CustomUserAdminMock().save_related(None, form, None, None)
        user_roles = get_user_roles(user)
        self.assertNotIn(grp1.name, (role.get_name() for role in user_roles))
        self.assertIn(AdminRole1, user_roles)


class SyncRolesTest(TestCase):

    def setup(self):
        pass

    def test_sync_group(self):
        out = StringIO()
        call_command('sync_roles', stdout=out)
        self.assertIn('Created Group: %s' % AdminRole1.get_name(), out.getvalue())
        group_names = [group['name'] for group in Group.objects.all().values('name')]
        self.assertIn(AdminRole1.get_name(), group_names)

    def test_sync_permissions(self):
        out = StringIO()
        call_command('sync_roles', stdout=out)
        permissions = [perm['codename'] for perm in Permission.objects.all().values('codename')]
        self.assertIn('admin_perm1', permissions)
        self.assertNotIn('admin_perm2', permissions)

    def test_sync_all_permissions(self):
        out = StringIO()
        call_command('sync_roles', all_permissions=True, stdout=out)
        permissions = [perm['codename'] for perm in Permission.objects.all().values('codename')]
        self.assertIn('admin_perm1', permissions)
        self.assertIn('admin_perm2', permissions)

    def test_sync_user_role_permissions(self):
        user = mommy.make(get_user_model())
        grp1 = mommy.make(Group)
        grp2 = mommy.make(Group, name=AdminRole1.get_name())
        user.groups.add(grp1)
        user.groups.add(grp2)
        out = StringIO()
        call_command('sync_roles', reset_user_permissions=True, stdout=out)

        user_group_names = [group['name'] for group in user.groups.all().values('name')]
        self.assertIn(grp1.name, user_group_names)
        self.assertIn(grp2.name, user_group_names)

        user_permission_names = [perm['codename'] for perm in user.user_permissions.all().values('codename')]
        self.assertIn('admin_perm1', user_permission_names)
        self.assertNotIn('admin_perm2', user_permission_names)

    def test_sync_preserves_groups(self):
        grp1 = mommy.make(Group)
        grp2 = mommy.make(Group, name=AdminRole1.get_name())
        out = StringIO()
        call_command('sync_roles', stdout=out)
        group_names = [group['name'] for group in Group.objects.all().values('name')]
        self.assertIn(grp1.name, group_names)
        self.assertIn(grp2.name, group_names)
