from __future__ import unicode_literals

from django.conf import settings
from importlib import import_module


def load_roles_and_permissions():
    if hasattr(settings, 'ROLEPERMISSIONS_MODULE'):
        import_module(settings.ROLEPERMISSIONS_MODULE)

    for app_name in settings.INSTALLED_APPS:
        if app_name is not 'rolepermissions':
            try:
                import_module('.permissions', app_name)
            except ImportError:
                pass
