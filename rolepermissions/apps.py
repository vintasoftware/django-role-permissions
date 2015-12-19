
from django.apps import AppConfig

from rolepermissions.loader import load_roles_and_permissions


class MyAppConfig(AppConfig):
    name = 'rolepermisions'
    verbose_name = "Django Role Permissions"

    def ready(self):
        load_roles_and_permissions()
