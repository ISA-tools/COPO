# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'copo_development',
        'USER': 'root',
        'PASSWORD': 'Apple123',
        'Host': '127.0.0.1',
        'Port': '',
        'init_command' :'SET storage_engine=MyISAM',
    }

}

STATIC_URL = '/static/'
MEDIA_ROOT = '/Users/fshaw/Desktop/test'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
SESSION_COOKIE_SECURE = False