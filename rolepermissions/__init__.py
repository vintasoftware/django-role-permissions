import django
from distutils.version import StrictVersion


__version__ = '2.0.0'


try:
    dj_version = StrictVersion(django.get_version())
except:
    dj_version = StrictVersion('1.10')


if dj_version < StrictVersion('1.7'):
    from rolepermissions.loader import load_roles_and_permissions
    load_roles_and_permissions()
else:
    default_app_config = 'rolepermissions.apps.RolePermissions'
