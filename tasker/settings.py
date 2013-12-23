import os

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = ('Anton Philippov', 'PhilippinoPhil@gmail.com')
MANAGERS = ADMINS

try:
    from db_settings import *
except ImportError:
    DATABASE_NAME = 'tasker'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'sorrento'
    DATABASE_ENGINE = 'django.db.backends.mysql'
    HOST = 'localhost'
    PORT_NUMBER = '3306' 

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE, 
        'NAME': DATABASE_NAME,                 
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': HOST,                     
        'PORT': PORT_NUMBER,                    
    }}

ALLOWED_HOSTS = ['*',]

TIME_ZONE = 'Europe/Russia'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ('static/',
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',)

SECRET_KEY = 'w%kv_vhs+=1iv!6a2_5k9e2@p16w7kukt1+@#50x$v9j&ddc0z'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',   
)

ROOT_URLCONF = 'tasker.urls'
WSGI_APPLICATION = 'tasker.wsgi.application'

TEMPLATE_DIRS = ('templates/',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task_viewer',
    'kulcalendar',
    'django.contrib.admin',
    )

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
   }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
