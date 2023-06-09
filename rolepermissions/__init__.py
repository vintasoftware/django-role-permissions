__version__ = '3.2.0'

import django

if django.VERSION < (3, 2):
    default_app_config = 'rolepermissions.apps.RolePermissions'
