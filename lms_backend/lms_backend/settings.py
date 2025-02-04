"""
Django settings for lms_backend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
STATIC_URL = '/static/'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-knibw$p(m*j9lbu*5b6!)+n%v-p(0l92^zeu7@1=5)$36enj=1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Helps connect the frontend to the backend, accepts requests from the frontend. 
# I think this is to do with cors
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Allows my vite frontend to access.
# How do these tokens actually work? Are they very different to bearer tokens?
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
]

# Just for now to avoid headaches.
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

# Some of this might be redundant I messed around with it a lot.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'core.apps.CoreConfig',
    'django_extensions',
    'webpack_loader',
    'corsheaders',
    'drf_yasg',
]


# Only added corsheaders for frontend connection.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

# I assume this tells the app where to find the urls.
ROOT_URLCONF = 'lms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # API only backend so no need for templates.
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

# Python specific calling convention for the frontend.
# Separates HTTP requests from application logic. 
WSGI_APPLICATION = 'lms_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Locates the database file. 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

## Custom user model as I redefine the user model in the core app. This configures the auth user model to use the custom user model.

AUTH_USER_MODEL = 'core.User' 

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Using the most basic TokenAuthentication. Easy to store, use, and understand.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  
    ],
    # Sets this as default permission. Specific restrictions are set on every view except signin/signup.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  
    ]
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'JSON_EDITOR': True,
}