"""
Django settings for {{ cookiecutter.project_name }}.
"""
import logging
import os
import platform

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from {{ cookiecutter.project_name }}.envs import (
    get_any,
    get_bool,
    get_int,
    get_string,
)

VERSION = "0.0.0"

SITE_ID = get_int("{{ cookiecutter.project_name|upper }}_SITE_ID", 1)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_string('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool('DEBUG', False)

ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = get_bool('{{ cookiecutter.project_name|upper }}_SECURE_SSL_REDIRECT', True)


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [
            r'.+\.hot-update\.+',
            r'.+\.js\.map'
        ]
    }
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'server_status',
    'raven.contrib.django.raven_compat',
    # Put our apps after this point
    '{{ cookiecutter.project_name }}',
)

DISABLE_WEBPACK_LOADER_STATS = get_bool("DISABLE_WEBPACK_LOADER_STATS", False)
if not DISABLE_WEBPACK_LOADER_STATS:
    INSTALLED_APPS += ('webpack_loader',)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
)

# enable the nplusone profiler only in debug mode
if DEBUG:
    INSTALLED_APPS += (
        'nplusone.ext.django',
    )
    MIDDLEWARE += (
        'nplusone.ext.django.NPlusOneMiddleware',
    )

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGIN_ERROR_URL = '/'

ROOT_URLCONF = '{{ cookiecutter.project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.project_name }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEFAULT_DATABASE_CONFIG = dj_database_url.parse(
    get_string('DATABASE_URL', None)
)
DEFAULT_DATABASE_CONFIG['CONN_MAX_AGE'] = get_int('{{ cookiecutter.project_name|upper }}_DB_CONN_MAX_AGE', 0)

if get_bool('{{ cookiecutter.project_name|upper }}_DB_DISABLE_SSL', False):
    DEFAULT_DATABASE_CONFIG['OPTIONS'] = {}
else:
    DEFAULT_DATABASE_CONFIG['OPTIONS'] = {'sslmode': 'require'}

DATABASES = {
    'default': DEFAULT_DATABASE_CONFIG
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# django-robots
ROBOTS_USE_HOST = False
ROBOTS_CACHE_TIMEOUT = get_int("ROBOTS_CACHE_TIMEOUT", 60 * 60 * 24)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Serve static files with dj-static
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Request files from the webpack dev server
USE_WEBPACK_DEV_SERVER = get_bool('{{ cookiecutter.project_name|upper }}_USE_WEBPACK_DEV_SERVER', False)
WEBPACK_DEV_SERVER_HOST = get_string('WEBPACK_DEV_SERVER_HOST', '')
WEBPACK_DEV_SERVER_PORT = get_int('WEBPACK_DEV_SERVER_PORT', {{ cookiecutter.webpack_dev_port }})

# Important to define this so DEBUG works properly
INTERNAL_IPS = (get_string('HOST_IP', '127.0.0.1'), )

# Configure e-mail settings
EMAIL_BACKEND = get_string('{{ cookiecutter.project_name|upper }}_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_string('{{ cookiecutter.project_name|upper }}_EMAIL_HOST', 'localhost')
EMAIL_PORT = get_int('{{ cookiecutter.project_name|upper }}_EMAIL_PORT', 25)
EMAIL_HOST_USER = get_string('{{ cookiecutter.project_name|upper }}_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = get_string('{{ cookiecutter.project_name|upper }}_EMAIL_PASSWORD', '')
EMAIL_USE_TLS = get_bool('{{ cookiecutter.project_name|upper }}_EMAIL_TLS', False)
EMAIL_SUPPORT = get_string('{{ cookiecutter.project_name|upper }}_SUPPORT_EMAIL', 'support@example.com')
DEFAULT_FROM_EMAIL = get_string('{{ cookiecutter.project_name|upper }}_FROM_EMAIL', 'webmaster@localhost')

MAILGUN_URL = get_string('MAILGUN_URL', None)
MAILGUN_KEY = get_string('MAILGUN_KEY', None)
MAILGUN_BATCH_CHUNK_SIZE = get_int('MAILGUN_BATCH_CHUNK_SIZE', 1000)
MAILGUN_RECIPIENT_OVERRIDE = get_string('MAILGUN_RECIPIENT_OVERRIDE', None)
MAILGUN_FROM_EMAIL = get_string('MAILGUN_FROM_EMAIL', 'no-reply@example.com')
MAILGUN_BCC_TO_EMAIL = get_string('MAILGUN_BCC_TO_EMAIL', 'no-reply@example.com')


# e-mail configurable admins
ADMIN_EMAIL = get_string('{{ cookiecutter.project_name|upper }}_ADMIN_EMAIL', '')
if ADMIN_EMAIL != '':
    ADMINS = (('Admins', ADMIN_EMAIL),)
else:
    ADMINS = ()

# Logging configuration
LOG_LEVEL = get_string('{{ cookiecutter.project_name|upper }}_LOG_LEVEL', 'INFO')
DJANGO_LOG_LEVEL = get_string('DJANGO_LOG_LEVEL', 'INFO')
SENTRY_LOG_LEVEL = get_string('SENTRY_LOG_LEVEL', 'ERROR')

# For logging to a remote syslog host
LOG_HOST = get_string('{{ cookiecutter.project_name|upper }}_LOG_HOST', 'localhost')
LOG_HOST_PORT = get_int('{{ cookiecutter.project_name|upper }}_LOG_HOST_PORT', 514)

HOSTNAME = platform.node().split('.')[0]

# nplusone profiler logger configuration
NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.ERROR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': (
                '[%(asctime)s] %(levelname)s %(process)d [%(name)s] '
                '%(filename)s:%(lineno)d - '
                '[{hostname}] - %(message)s'
            ).format(hostname=HOSTNAME),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'syslog': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'formatter': 'verbose',
            'address': (LOG_HOST, LOG_HOST_PORT)
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': SENTRY_LOG_LEVEL,
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'propagate': True,
            'level': DJANGO_LOG_LEVEL,
            'handlers': ['console', 'syslog', 'sentry'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
        'raven': {
            'level': SENTRY_LOG_LEVEL,
            'handlers': []
        },
        'nplusone': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    },
    'root': {
        'handlers': ['console', 'syslog', 'sentry'],
        'level': LOG_LEVEL,
    },
}

# Sentry
ENVIRONMENT = get_string('{{ cookiecutter.project_name|upper }}_ENVIRONMENT', 'dev')
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
RAVEN_CONFIG = {
    'dsn': get_string('SENTRY_DSN', ''),
    'environment': ENVIRONMENT,
    'release': VERSION
}

# server-status
STATUS_TOKEN = get_string("STATUS_TOKEN", "")
HEALTH_CHECK = ['CELERY', 'REDIS', 'POSTGRES']

GA_TRACKING_ID = get_string("GA_TRACKING_ID", "")
REACT_GA_DEBUG = get_bool("REACT_GA_DEBUG", False)

MEDIA_ROOT = get_string('MEDIA_ROOT', '/var/media/')
MEDIA_URL = '/media/'
{{ cookiecutter.project_name|upper }}_USE_S3 = get_bool('{{ cookiecutter.project_name|upper }}_USE_S3', False)
AWS_ACCESS_KEY_ID = get_string('AWS_ACCESS_KEY_ID', False)
AWS_SECRET_ACCESS_KEY = get_string('AWS_SECRET_ACCESS_KEY', False)
AWS_STORAGE_BUCKET_NAME = get_string('AWS_STORAGE_BUCKET_NAME', False)
AWS_QUERYSTRING_AUTH = get_string('AWS_QUERYSTRING_AUTH', False)
# Provide nice validation of the configuration
if (
        {{cookiecutter.project_name | upper}}_USE_S3 and
        (not AWS_ACCESS_KEY_ID or
         not AWS_SECRET_ACCESS_KEY or
         not AWS_STORAGE_BUCKET_NAME)
):
    raise ImproperlyConfigured(
        'You have enabled S3 support, but are missing one of '
        'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, or '
        'AWS_STORAGE_BUCKET_NAME'
    )
if {{ cookiecutter.project_name|upper }}_USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
else:
    # by default use django.core.files.storage.FileSystemStorage with
    # overwrite feature
    DEFAULT_FILE_STORAGE = 'storages.backends.overwrite.OverwriteStorage'

# Celery
USE_CELERY = True
CELERY_BROKER_URL = get_string("CELERY_BROKER_URL", get_string("REDISCLOUD_URL", None))
CELERY_RESULT_BACKEND = get_string(
    "CELERY_RESULT_BACKEND", get_string("REDISCLOUD_URL", None)
)
CELERY_TASK_ALWAYS_EAGER = get_bool("CELERY_TASK_ALWAYS_EAGER", False)
CELERY_TASK_EAGER_PROPAGATES = get_bool("CELERY_TASK_EAGER_PROPAGATES", True)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'


# django cache back-ends
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'local-in-memory-cache',
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    },
}


# features flags
def get_all_config_keys():
    """Returns all the configuration keys from both environment and configuration files"""
    return list(os.environ.keys())

{{ cookiecutter.project_name|upper }}_FEATURES_PREFIX = get_string('{{ cookiecutter.project_name|upper }}_FEATURES_PREFIX', 'FEATURE_')
FEATURES = {
    key[len({{ cookiecutter.project_name|upper }}_FEATURES_PREFIX):]: get_any(key, None) for key
    in get_all_config_keys() if key.startswith({{ cookiecutter.project_name|upper }}_FEATURES_PREFIX)
}

MIDDLEWARE_FEATURE_FLAG_QS_PREFIX = get_string("MIDDLEWARE_FEATURE_FLAG_QS_PREFIX", None)
MIDDLEWARE_FEATURE_FLAG_COOKIE_NAME = get_string(
    'MIDDLEWARE_FEATURE_FLAG_COOKIE_NAME',
    '{{ cookiecutter.project_name|upper }}_FEATURE_FLAGS',
)
MIDDLEWARE_FEATURE_FLAG_COOKIE_MAX_AGE_SECONDS = get_int('MIDDLEWARE_FEATURE_FLAG_COOKIE_MAX_AGE_SECONDS', 60 * 60)

if MIDDLEWARE_FEATURE_FLAG_QS_PREFIX:
    MIDDLEWARE = MIDDLEWARE + (
        '{{ cookiecutter.project_name }}.middleware.QueryStringFeatureFlagMiddleware',
        '{{ cookiecutter.project_name }}.middleware.CookieFeatureFlagMiddleware',
    )


# django debug toolbar only in debug mode
if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )
    # it needs to be enabled before other middlewares
    MIDDLEWARE = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE

# List of mandatory settings. If any of these is not set, the app will not start
# and will raise an ImproperlyConfigured exception
MANDATORY_SETTINGS = [
    'MAILGUN_URL',
    'MAILGUN_KEY',
    'SECRET_KEY',
]
