import os
# For further info see https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

#get settings for environment
from settings_hostnames import *
# determine which system is running and import appropriate settings file
if node() == DEVELOPMENT_HOST or node() == UEA_DEV:
    from project_copo.settings.settings_dev import *
elif node() == PRODUCTION_HOST:
    from project_copo.settings.settings_prod import *
else:
    raise Exception("Cannot determine execution mode for host '%s'. Please check DEVELOPMENT_HOST and PRODUCTION_HOST in settings_local.py." % node())



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!q)6na7q*xu#24k-2jlt0hf-*dqw2vvgf4!t*_+a@(v=_6w*$t'

# now import other settings
from project_copo.settings.settings_chunked_upload import *

LOGIN_URL = '/copo/login/'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))




ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.web_copo',
    'rest_framework',
    'chunked_upload',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project_copo.urls'

WSGI_APPLICATION = 'project_copo.wsgi.application'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
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
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


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
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}
