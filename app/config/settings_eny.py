"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os

import boto3

# boto3를 사용하는 방법
# 1. 환경변수중에서 SecretsManager에 접근할 수 있는 AWS인증값들이 있는지 확인
access_key = os.environ.get('AWS_SECRETS_MANAGER_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY')

region_name = 'ap-northeast-2'
# 2. 환경변수에 인증값들이 존재하면 해당 값들을 사용해서 Session생성
#    환경변수에 인증값들이 존재하지 않는다면, profile을 사용해서 Session생성
session_kwargs = {
    'region_name': region_name,
}
if access_key and secret_key:
    session_kwargs['aws_access_key_id'] = access_key
    session_kwargs['aws_secret_access_key'] = secret_key
else:
    session_kwargs['profile_name'] = 'WPS-secretsManager'
session = boto3.session.Session(**session_kwargs)

# Session을 사용해서 SecretsManager에 접근할 수 있는 Client생성
client = session.client(
    service_name='secretsmanager',
    region_name=region_name,
)
secrets_string = client.get_secret_value(SecretId='wps')['SecretString']
secrets_data = json.loads(secrets_string)
SECRETS = secrets_data['instagram']

# django-secrets-manager
# from django_secrets import SECRETS
#
# AWS_SECRETS_MANAGER_SECRETS_NAME = 'wps'
# AWS_SECRETS_MANAGER_SECRETS_SECTION = 'instagram'
# AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'
# AWS_SECRETS_MANAGER_PROFILE = 'wps-secrets-manager'

# django-secrets-manager의 SECRETS를 사용해서 비밀 값 할당
AWS_ACCESS_KEY_ID = SECRETS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRETS['AWS_SECRET_ACCESS_KEY']

# django-storages | AWS S3
AWS_STORAGE_BUCKET_NAME = 'wps12th-instagram-pjh'
AWS_DEFAULT_ACL = 'private'
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_REGION_NAME = 'ap-northeast-2'

DEBUG = True
SECRET_KEY = 'l4ux!g)8(18*h)02j*j)y-+@cy$_l-q$4%1b_#i3++(#+5nr$l'

# instagram/app/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# instagram/
ROOT_DIR = os.path.dirname(BASE_DIR)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# 정적파일 설정 추가
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_URL = '/static/'

# instagram/.media
# User-uploaded static files의 기본 경로
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

# django-storages
# Django의 FileStorage로 S3Boto3Storage(AWS의 S3)를 사용
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '172.16.1.116',
    '*',
]
AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'members.apps.MembersConfig',
    'posts.apps.PostsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR, 'templates'),
            TEMPLATES_DIR,
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = SECRETS['DATABASES']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True