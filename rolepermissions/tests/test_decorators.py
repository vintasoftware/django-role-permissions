
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse

from model_mommy import mommy

from rolepermissions.roles import AbstractUserRole
from rolepermissions.decorators import has_role_decorator, has_permission_decorator


class DecRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }


class DecRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }


class HasRoleDetailView(DetailView):

    @method_decorator(has_role_decorator('dec_role1'))
    def dispatch(self, request, *args, **kwargs):
        return super(HasRoleDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("Test")


class MultipleHasRoleDetailView(DetailView):

    @method_decorator(has_role_decorator(['dec_role1', DecRole2]))
    def dispatch(self, request, *args, **kwargs):
        return super(MultipleHasRoleDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("Test")


class HasRoleDecoratorTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_has_allowed_role_to_view(self):
        user = self.user
        request = self.request

        DecRole1.assign_role_to_user(user)

        response = HasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_does_not_have_allowed_role_to_view(self):
        user = self.user
        request = self.request

        DecRole2.assign_role_to_user(user)

        with self.assertRaises(PermissionDenied):
            HasRoleDetailView.as_view()(request)

    def test_view_with_multiple_allowed_roles(self):
        user = self.user
        request = self.request

        DecRole2.assign_role_to_user(user)

        response = MultipleHasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

        DecRole1.assign_role_to_user(user)

        response = MultipleHasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)


class HasPermissionDetailView(DetailView):

    @method_decorator(has_permission_decorator('permission2'))
    def dispatch(self, request, *args, **kwargs):
        return super(HasPermissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("Test")


class PermissionOverhiddenRedirectView(DetailView):

    @method_decorator(has_permission_decorator('permission2', redirect_to_login=False))
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionOverhiddenRedirectView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("Test")


class RoleOverhiddenRedirectView(DetailView):

    @method_decorator(has_role_decorator('permission2', redirect_to_login=False))
    def dispatch(self, request, *args, **kwargs):
        return super(RoleOverhiddenRedirectView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return True

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("Test")


class HasPermissionDecoratorTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_has_permission_granted(self):
        user = self.user
        request = self.request

        DecRole1.assign_role_to_user(user)

        response = HasPermissionDetailView.as_view()(request)

        self.assertEquals(response.status_code, 200)

    def test_permission_denied(self):
        user = self.user
        request = self.request

        DecRole2.assign_role_to_user(user)

        with self.assertRaises(PermissionDenied):
            HasPermissionDetailView.as_view()(request)


@override_settings(
    ROLEPERMISSIONS_REDIRECT_TO_LOGIN=True, LOGIN_URL='/login/',
    ROOT_URLCONF='rolepermissions.tests.mock_urls')
class RedirectToLoginTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_permission_redirects_to_login(self):
        request = self.request

        response = HasPermissionDetailView.as_view()(request)

        self.assertEquals(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_permision_overhiding_setting(self):
        request = self.request

        with self.assertRaises(PermissionDenied):
            PermissionOverhiddenRedirectView.as_view()(request)

    def test_role_redirects_to_login(self):
        request = self.request

        response = HasRoleDetailView.as_view()(request)

        self.assertEquals(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_role_overhiding_setting(self):
        request = self.request

        with self.assertRaises(PermissionDenied):
            RoleOverhiddenRedirectView.as_view()(request)


@override_settings(
    ROLEPERMISSIONS_REDIRECT_TO_LOGIN=False, LOGIN_URL='/login/',
    ROOT_URLCONF='rolepermissions.tests.mock_urls')
class NotRedirectToLoginTests(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        self.factory = RequestFactory()

        self.request = self.factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_permission_does_not_redirects_to_login(self):
        request = self.request

        with self.assertRaises(PermissionDenied):
            HasPermissionDetailView.as_view()(request)

    def test_role_does_not_redirects_to_login(self):
        request = self.request

        with self.assertRaises(PermissionDenied):
            HasRoleDetailView.as_view()(request)
