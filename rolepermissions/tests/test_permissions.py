
from django.test import TestCase

from rolepermissions.permissions import PermissionsManager, register_object_checker
from rolepermissions.exceptions import CheckerNotRegistered


class PermissionsManagerTests(TestCase):

    def setUp(self):
        PermissionsManager._checkers = {}

    def test_register_checker(self):
        def func():
            pass

        PermissionsManager.register_checker('func_name', func)

        self.assertIn('func_name', PermissionsManager._checkers)
        self.assertEquals(PermissionsManager._checkers['func_name'], func)

    def test_get_checkers(self):
        self.assertEquals(PermissionsManager.get_checkers(), {})

    def test_retrieve_checker(self):
        def func():
            pass

        PermissionsManager.register_checker('func_name', func)

        self.assertEquals(PermissionsManager.retrieve_checker('func_name'), func)

    def test_restore_unregistered_function(self):
        
        with self.assertRaises(CheckerNotRegistered):
            PermissionsManager.retrieve_checker('func_name')


class RegisterObjectCheckerDecoratorTests(TestCase):

    def setUp(self):
        PermissionsManager._checkers = {}

    def test_resgisters_function(self):
        @register_object_checker()
        def function_name(a, b, c):
            return True

        self.assertIn('function_name', PermissionsManager.get_checkers())

        restore_function = PermissionsManager.retrieve_checker('function_name')

        self.assertTrue(restore_function('', '', ''))

    def test_register_function_with_diferent_name(self):
        @register_object_checker('new_name')
        def function_name(a, b, c):
            return True

        self.assertIn('new_name', PermissionsManager.get_checkers())

        restore_function = PermissionsManager.retrieve_checker('new_name')

        self.assertTrue(restore_function('', '', ''))
