"""
Django settings for gdoapa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'PUT_YOUR_OWN_SECRET_KEY_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True
DEVELOPMENT = False		# custom key. set to True for production
ENABLE_EMAIL = True		# custom key. Enable email notification

if DEVELOPMENT:
	SERVER_LINK = "YOUR_DEVELOPMENT_SERVER_NAME:PORT"	# custom key. Server address to create links#
else:
	SERVER_LINK = "YOUR_SERVER_NAME:PORT"	# custom key. Server address to create links

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "YOUR_DEVELOPMENT_SERVER_NAME", "YOUR_SERVER_NAME"]
CSRF_TRUSTED_ORIGINS = ['https://YOUR_DEVELOPMENT_SERVER_NAME', 'https://YOUR_SERVER_NAME']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'gestione_ordini',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS': {'min_length': 8,}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ROOT_URLCONF = 'gdoapa.urls'

WSGI_APPLICATION = 'gdoapa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if DEVELOPMENT:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'YOUR_DB_NAME',
			'USER': 'YOUR_DB_USER',
			'PASSWORD': 'YOUR_DB_PASSWORD',
			'HOST': 'localhost',
			'PORT': 'YOUR_DB_PORT',
		}
	}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'						# here are placed the static files (es. .js, .css)
LOGIN_REDIRECT_URL = '/gestione_ordini/'
if DEVELOPMENT:
	MEDIA_ROOT = 'C:/django_media/'			# here are placed the files uploaded from users
else:
	MEDIA_ROOT = '/data/django_media/'		# here are placed the files uploaded from users
MEDIA_URL = '/media/'
SESSION_COOKIE_AGE = 36000					# user session expire after 36000 s (10 h)


# Disable autocreate only for database dump and loading!!
ENABLE_AUTOCREATE = True					# custom key. Enable autocreation of some data (es. user profiles)

EMAIL_HOST = 'YOUR_EMAIL_HOST'
EMAIL_PORT = 'YOUR_EMAIL_PORT'
EMAIL_HOST_USER = 'YOUR_EMAIL_HOST_USERNAME'
EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_PASSWORD'
EMAIL_REPLYTO = 'YOUR_REPLYTO_ADDRESS'		# custom key. Replyto address
EMAIL_USE_SSL = False
# EMAIL_USE_TLS = True