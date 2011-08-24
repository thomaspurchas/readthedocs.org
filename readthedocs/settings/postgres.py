from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'readthedocs',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG
CELERY_ALWAYS_EAGER = False

MEDIA_URL = 'http://172.16.1.131/docs/media/'
#ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
#CACHE_BACKEND = 'memcached://localhost:11211/'
#SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_ENGINE = 'django.contrib.sessions.backends.file'

#HAYSTACK_SEARCH_ENGINE = 'solr'
#HAYSTACK_SOLR_URL = 'http://odin:8983/solr'

CACHE_BACKEND = 'dummy://'


import djcelery
djcelery.setup_loader()

try:
    from local_settings import *
except:
    pass
