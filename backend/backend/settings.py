"""
Django settings for backend project, using django-environ.
"""

import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['testserver', 'backend', 'localhost']


# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Third-Party Apps
    'rest_framework',
    'rest_framework_gis',

    # Project Apps
    'analysis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Configuration
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'




# SIAR Data Sources & Analysis Parameters
# ---------------------------------------
# Local data paths
PRECIPITATION_DATA_DIR = env('PRECIPITATION_DATA_DIR')

# Web Coverage Service (WCS) endpoints and layer IDs
LAND_COVER_WCS_URL = env('LAND_COVER_WCS_URL')
LAND_COVER_COVERAGE_ID = env('LAND_COVER_COVERAGE_ID')

# REST API endpoint for biodiversity data
GBIF_API_URL = env('GBIF_API_URL')

# API Key for OpenTopography
OPENTOPOGRAPHY_API_KEY = env('OPENTOPOGRAPHY_API_KEY', default=None)

# Analysis algorithm thresholds
SLOPE_THRESHOLD_DEGREES = env.float('SLOPE_THRESHOLD_DEGREES')
ALTITUDE_MIN_METERS = env.float('ALTITUDE_MIN_METERS')
ALTITUDE_MAX_METERS = env.float('ALTITUDE_MAX_METERS')
SOIL_SILT_MIN_PERCENT = env.float('SOIL_SILT_MIN_PERCENT')
SOIL_CLAY_MAX_PERCENT = env.float('SOIL_CLAY_MAX_PERCENT')
SUITABLE_LAND_COVER_IDS = env.list('SUITABLE_LAND_COVER_IDS', cast=int)
PRECIPITATION_MIN_MM = env.float('PRECIPITATION_MIN_MM')
PRECIPITATION_MAX_MM = env.float('PRECIPITATION_MAX_MM')
MAX_AREA_FOR_TILING = env.float('MAX_AREA_FOR_TILING', default=10000)

# Feature Toggles
ENABLE_LAND_COVER_ANALYSIS = env.bool('ENABLE_LAND_COVER_ANALYSIS', default=False)

# Data Provider Configuration
# ---------------------------
DATA_PROVIDERS = {
    'dem': 'analysis.data_acquisition.OpenTopographyDEMProvider',
    'soil': 'analysis.data_acquisition.SoilGridsProvider',
    'precipitation': 'analysis.data_acquisition.LocalFilePrecipitationProvider',
    'species': 'analysis.data_acquisition.GBIFAPIProvider',
    'land_cover': 'analysis.data_acquisition.LandCoverProvider', # New provider
}

# Logging Configuration
# ---------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'analysis': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}