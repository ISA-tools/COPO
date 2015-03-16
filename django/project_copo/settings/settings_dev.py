# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#mysql.connector.django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'copo_development',
        'USER': 'fshaw',
        'PASSWORD': 'Apple123',
        'Host': '127.0.0.1',
        'Port': '',
        'init_command' :'SET storage_engine=MyISAM',
    }
}

MONGO_DB = 'copo_mongo'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '127.0.0.1'
SESSION_REDIS_PORT = 6379

STATIC_URL = '/static/'
MEDIA_ROOT = '/Users/fshaw/Desktop/test'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
SESSION_COOKIE_SECURE = False