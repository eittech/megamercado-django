"""
Django settings for comparagrow project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# BOT_NAME = 'comparagrow'
#
# SPIDER_MODULES = ['dynamic_scraper.spiders', 'comparagrow.scraper',]
# USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')
#
# #Scrapy 0.20+
# ITEM_PIPELINES = {
#     'dynamic_scraper.pipelines.ValidationPipeline': 400,
#     'comparagrow.scraper.pipelines.DjangoWriterPipeline': 800,
# }
#
# #Scrapy up to 0.18
# ITEM_PIPELINES = [
#     'dynamic_scraper.pipelines.ValidationPipeline',
#     'comparagrow.scraper.pipelines.DjangoWriterPipeline',
# ]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r#hc(l2(-+=ih$6d#d&kkkafvr_4n0e%m)@(92qv1kav3259%4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.8','192.168.1.6','192.168.1.5','192.168.1.9','127.0.0.1','35.185.63.218']

#habilitar cuando use postgres
# SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #social django
    'social_django',

    'rest_framework',
    'django_user_agents',
    'mptt',
    'tagging',
    'customers',
    'contracts',
    'services',
    'products'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    #social django
    'social_django.middleware.SocialAuthExceptionMiddleware',

]

ROOT_URLCONF = 'comparagrow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #social django
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'comparagrow.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'comparagrow420@gmail.com'
EMAIL_HOST_PASSWORD = 'Pazverde420'
#EMAIL_HOST_USER = 'teteangarita121194@gmail.com'
#EMAIL_HOST_PASSWORD = '17800074'

EMAIL_PORT = 587

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'comparagrow',
         'USER': 'postgres',
         'PASSWORD': 'hfv5ac1obcBw1P9x',
         'HOST': '104.197.7.8',
         'PORT': '',
     }
 }

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'comparagrow',
#        'USER':	'postgres',
#        'PASSWORD':	'hfv5ac1obcBw1P9x',
#        'HOST': '104.197.7.8',
#    }
# }


AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',


)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_URL = '/static/'
STATIC_ROOT = 'static_admin/'
#STATIC_ROOT = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGOUT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


#credenciales social login
SOCIAL_AUTH_GITHUB_KEY = '356c61a6a045c96b53c1'
SOCIAL_AUTH_GITHUB_SECRET = '10b704f62ebe181f0579b5b9248ca64eb9f70acd'


SOCIAL_AUTH_TWITTER_KEY = 'mYP1Zh0VdqTm301D97twSdlFd'
SOCIAL_AUTH_TWITTER_SECRET = '9uvCC7uX58870992zP0M4cJ8lhPbGXJcT3BAiniaXgOz32onyS'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '361874647317-rfjamk7oeg7jquooa6cov96olaf9vhpk.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'R0E6_UipW7yy8jiduCYifY99'
