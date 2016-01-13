
from django.apps import AppConfig

from rolepermissions.loader import load_roles_and_permissions


class RolePermissions(AppConfig):
    name = 'rolepermissions'
    verbose_name = "Django Role Permissions"

    def ready(self):
        load_roles_and_permissions()
