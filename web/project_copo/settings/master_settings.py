import sys

import os



# For further info see https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xyzabc123'



LOGIN_URL = '/accounts/login/'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


ALLOWED_HOSTS = ['http://v0514.nbi.ac.uk']

# Application definition
INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_copo',
    'rest_framework',
    'chunked_upload',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.orcid',
    'allauth.socialaccount.providers.google',
)

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } }}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

REST_FRAMEWORK = {
    # Use Django's standard `web.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates/copo'), os.path.join(BASE_DIR, 'templates/account')]

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               'django.core.context_processors.csrf',
                               'django.core.context_processors.request',
                               'django.core.context_processors.static',
                               # processor for base page status template tags
                               "web_copo.context_processors.get_status",
                               # `allauth` specific context processors
                               'allauth.account.context_processors.account',
                               'allauth.socialaccount.context_processors.socialaccount',
                               )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

from settings_logging import *

import platform


if platform.system() == "Darwin":
    from settings_chunked_upload import *
    if 'test' in sys.argv:
        from settings_test import *
    else:
        from settings_dev import *
    from settings_chunked_upload import *
elif platform.system() == "Linux":
    from settings.settings_chunked_upload import *
    if 'test' in sys.argv:
        from settings.settings_test import *
    else:
        from settings.settings_prod import *

else:
    raise Exception(
        "Cannot determine execution mode for host '%s'. Please check DEVELOPMENT_HOST and PRODUCTION_HOST in settings_local.py." % node())


#reference project home
PROJ_HOME = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__ )), os.pardir, os.pardir, os.pardir))

