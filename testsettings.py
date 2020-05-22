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

SECRET_KEY = 'abcde12345'

if dj_version >= LooseVersion('2.0'):
    MIDDLEWARE = (
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
    )

if dj_version >= LooseVersion('3.0'):
    MIDDLEWARE = MIDDLEWARE + (
        'django.contrib.sessions.middleware.SessionMiddleware',
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
