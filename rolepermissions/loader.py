
import inspect

from django.conf import settings
from django.utils.importlib import import_module

from rolepermissions.roles import AbstractUserRole, RolesManager
from rolepermissions.permissions import PermissionsManager


def load_roles_and_permissions():
    roles_module = import_module(settings.ROLEPERMISSIONS_MODULE)

    RolesManager._roles = {}
    PermissionsManager._checkers = {}

    for name, cls in roles_module.__dict__.items():
        if inspect.isclass(cls) and issubclass(cls, AbstractUserRole) and cls is not AbstractUserRole:
            RolesManager.register_role(cls)
            # print 'Loading role ' + cls().get_name()

    for app_name in settings.INSTALLED_APPS:
        if app_name is not 'rolepermissions':
            try:
                import_module('.permissions', app_name)
            except ImportError as exc:
                pass

