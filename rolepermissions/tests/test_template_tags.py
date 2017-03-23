
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.template import Context, Template

from model_mommy import mommy

from rolepermissions.roles import AbstractUserRole
from rolepermissions.permissions import register_object_checker


class TemRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }

class TemRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }

class TemRole3(AbstractUserRole):
    role_name = 'new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class BaseTagTestCase(TestCase):

    def tag_test(self, template, context, output):
        t = Template('{% load permission_tags %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)


class HasRoleTests(BaseTagTestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        TemRole1.assign_role_to_user(self.user)

    def test_has_role_tag(self):
        user = self.user

        template = '{% if user|has_role:"tem_role1" %}passed{% endif %}'

        context = {
            'user': user,
        }

        output = 'passed'

        self.tag_test(template, context, output)

    def test_has_role_tag_with_multiple_roles(self):
        user = self.user

        template = '{% if user|has_role:"tem_role1,tem_role2" %}passed{% endif %}'

        context = {
            'user': user,
        }

        output = 'passed'

        self.tag_test(template, context, output)

    def test_does_not_have_role_tag_with_multiple_roles(self):
        user = self.user

        template = '{% if user|has_role:"tem_role2,tem_role3" %}passed{% endif %}'

        context = {
            'user': user,
        }

        output = ''

        self.tag_test(template, context, output)


class CanFilterTests(BaseTagTestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        TemRole1.assign_role_to_user(self.user)

    def test_can_see(self):
        user = self.user

        template = (
            "{% if user|can:'permission1' %}passed{% endif %}")

        context = {
            'user': user,
        }

        output = 'passed'

        self.tag_test(template, context, output)

    def test_can_not_see(self):
        user = self.user

        template = (
            "{% if user|can:'permission3' %}passed{% endif %}")

        context = {
            'user': user,
        }

        output = ''

        self.tag_test(template, context, output)


class CanTagTests(BaseTagTestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

        TemRole1.assign_role_to_user(self.user)

    def test_can_print_stuff(self):
        user = self.user

        @register_object_checker()
        def can_print_stuff(role, user, clinic):
            return True

        template = (
            "{% can 'can_print_stuff' '' as can_print %}"
            "{% if can_print %}passed{% endif %}")

        context = {
            'user': user,
        }

        output = 'passed'

        self.tag_test(template, context, output)

    def test_can_not_print_stuff(self):
        user = self.user

        @register_object_checker()
        def can_print_stuff(role, user, clinic):
            return False

        template = (
            "{% can 'can_print_stuff' '' as can_print %}"
            "{% if can_print %}passed{% endif %}")

        context = {
            'user': user,
        }

        output = ''

        self.tag_test(template, context, output)
