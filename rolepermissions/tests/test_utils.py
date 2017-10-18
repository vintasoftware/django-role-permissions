
from django.test import TestCase
from rolepermissions.utils import camelToSnake, snake_to_title, camel_or_snake_to_title


class UtilTests(TestCase):

    def setUp(self):
        pass

    def test_camel_to_snake(self):
        self.assertEqual(camelToSnake('camelCaseString'), 'camel_case_string')
        self.assertEqual(camelToSnake('Snake_Camel_String'), 'snake__camel__string')

    def test_snake_to_title(self):
        self.assertEqual(snake_to_title('snake_case_string'), 'Snake Case String')
        self.assertEqual(snake_to_title('Even_if__itsFunky'), 'Even If  Itsfunky')

    def test_camel_or_snake_to_title(self):
        self.assertEqual(camel_or_snake_to_title('snake_case_string'), 'Snake Case String')
        self.assertEqual(camel_or_snake_to_title('camelCaseString'), 'Camel Case String')
        self.assertEqual(camel_or_snake_to_title('mix_itUp_WhyNot'), 'Mix It Up  Why Not')
