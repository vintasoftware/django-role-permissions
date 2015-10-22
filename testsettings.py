DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'rolepermissions',
)

import django
from distutils.version import LooseVersion

if LooseVersion(django.get_version()) >= LooseVersion('1.5') \
    and LooseVersion(django.get_version()) < LooseVersion('1.6'):
    INSTALLED_APPS += ('discover_runner',)
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = 'abcde12345'

if LooseVersion(django.get_version()) >= LooseVersion('1.7'):
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware'
    )
