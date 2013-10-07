
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.test import TestCase
from django.contrib.auth import get_user_model, login
from django.test.client import RequestFactory
from django.core.exceptions import PermissionDenied

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.decorators import has_role_decorator, has_permission_decorator


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


class HasRoleDetailView(DetailView):

    @method_decorator(has_role_decorator('role1'))
    def dispatch(self, request, *args, **kwargs):
        return super(HasRoleDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

class MultipleHasRoleDetailView(DetailView):

    @method_decorator(has_role_decorator(['role1', Role2]))
    def dispatch(self, request, *args, **kwargs):
        return super(MultipleHasRoleDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

class HasRoleDecoratorTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)

        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_has_allowed_role_to_view(self):
        user = self.user
        request = self.request

        Role1.assign_role_to_user(user)

        response = HasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_does_not_have_allowed_role_to_view(self):
        user = self.user
        request = self.request

        Role2.assign_role_to_user(user)

        with self.assertRaises(PermissionDenied):
            response = HasRoleDetailView.as_view()(request)

    def test_view_with_multiple_allowed_roles(self):
        user = self.user
        request = self.request

        Role2.assign_role_to_user(user)

        response = MultipleHasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

        Role1.assign_role_to_user(user)

        response = MultipleHasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        RolesManager._roles = {}


class HasPermissionDetailView(DetailView):

    @method_decorator(has_permission_decorator('permission2'))
    def dispatch(self, request, *args, **kwargs):
        return super(HasPermissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True


class HasPermissionDecoratorTests(TestCase):

    def setUp(self):
        RolesManager.register_role(Role1)
        RolesManager.register_role(Role2)

        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_has_permission_granted(self):
        user = self.user
        request = self.request

        Role1.assign_role_to_user(user)

        response = HasPermissionDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_permission_denied(self):
        user = self.user
        request = self.request

        Role2.assign_role_to_user(user)

        with self.assertRaises(PermissionDenied):
            response = HasPermissionDetailView.as_view()(request)

    def tearDown(self):
        RolesManager._roles = {}
