# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#mysql.connector.django
#django.db.backends.mysql
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'copo_development',
        'USER': 'root',
        'PASSWORD': '',
        'Host': '127.0.0.1',
        'Port': '',
        'init_command' :'SET storage_engine=MyISAM',
    }
}

STATIC_URL = '/static/'
MEDIA_ROOT = '/Users/etuka/Dropbox/Dev/util/iRODS/Vault/home/rods/copo-data'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
SESSION_COOKIE_SECURE = False