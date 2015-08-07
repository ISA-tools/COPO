__author__ = 'felix.shaw@tgac.ac.uk - 05/08/15'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'test',
        'USER': 'fshaw',
        'PASSWORD': '',
        'Host': '127.0.0.1',
        'Port': '',
        'init_command' :'SET storage_engine=MyISAM',
    }

}


MONGO_DB = 'copo_mongo_test'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '127.0.0.1'
SESSION_REDIS_PORT = 6379

SITE_ID = 2

STATIC_URL = '/static/'
MEDIA_ROOT = '/var/www/copo_media'
# MEDIA_ROOT = '/Users/etuka/COPOIrodsMount'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
SESSION_COOKIE_SECURE = False