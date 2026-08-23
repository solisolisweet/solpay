import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sol-monetization-cbe-direct-key-1000006827539')

# In production set DJANGO_DEBUG=False via Render env vars
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', '')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_ENV.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['*']  # Render injects the real host via ALLOWED_HOSTS env var

# Reverse Proxy & SSL Security Settings
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# In production, enforce HTTPS redirects
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Monetization Apps
    'marketplace',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sol_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'payments.context_processors.cbe_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'sol_project.wsgi.application'

# -------------------------------------------------------------------
# DATABASE — PostgreSQL on Render, SQLite locally
# Render sets the DATABASE_URL environment variable automatically
# when you attach a PostgreSQL database to the service.
# -------------------------------------------------------------------
_db_url = os.environ.get('DATABASE_URL')
if _db_url:
    DATABASES = {
        'default': dj_database_url.parse(_db_url, conn_max_age=600, ssl_require=not DEBUG)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Addis_Ababa'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC FILES — WhiteNoise serves them directly in production
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic destination
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------------------------------------------
# MEDIA FILES — stored under /media/ (local disk only)
# On Render free tier, media is ephemeral. For persistent uploads,
# connect an external storage (e.g., Cloudinary, AWS S3).
# -------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# Bank of Abyssinia (BOA) Payout & Payment Configuration
# -------------------------------------------------------------------
BOA_ACCOUNT_NUMBER = os.environ.get('BOA_ACCOUNT_NUMBER', '96072775')
BOA_ACCOUNT_NAME = os.environ.get('BOA_ACCOUNT_NAME', 'Sol Merchant Account')
BOA_BANK_NAME = os.environ.get('BOA_BANK_NAME', 'Bank of Abyssinia (BOA)')

# Legacy / Alias compatibility
CBE_ACCOUNT_NUMBER = BOA_ACCOUNT_NUMBER
CBE_ACCOUNT_NAME = BOA_ACCOUNT_NAME
CBE_BANK_NAME = BOA_BANK_NAME

# -------------------------------------------------------------------
# DASHBOARD SECRET PASSWORD
# Set DASHBOARD_PASSWORD env var on Render to protect your dashboard.
# Default is 'admin1234' — change it!
# -------------------------------------------------------------------
DASHBOARD_PASSWORD = os.environ.get('DASHBOARD_PASSWORD', 'admin1234')
