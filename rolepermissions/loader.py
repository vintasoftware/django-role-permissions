from __future__ import unicode_literals

import inspect

from importlib import import_module
from pydoc import locate

from django.conf import settings


def get_app_name(app_name):
    """
    Returns a app name from new app config if is
    a class or the same app name if is not a class.
    """
    type_ = locate(app_name)
    if inspect.isclass(type_):
        return type_.name
    return app_name


def load_roles_and_permissions():
    if hasattr(settings, 'ROLEPERMISSIONS_MODULE'):
        import_module(settings.ROLEPERMISSIONS_MODULE)

    for app_name in settings.INSTALLED_APPS:
        if app_name != 'rolepermissions':
            app_name = get_app_name(app_name)
            try:
                import_module('.permissions', app_name)
            except ImportError:
                pass
