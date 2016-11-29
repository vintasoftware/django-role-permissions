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


try:
    dj_version = LooseVersion(django.get_version())
except:
    dj_version = LooseVersion('1.10')

if dj_version >= LooseVersion('1.5') and dj_version < LooseVersion('1.6'):
    INSTALLED_APPS += ('discover_runner',)
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = 'abcde12345'

if dj_version >= LooseVersion('1.7'):
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware'
    )

if dj_version >= LooseVersion('1.8'):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
