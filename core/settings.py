
import os
from pathlib import Path
from django.contrib import messages
from datetime import timedelta
from django.utils.functional import LazyObject, empty
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR,".env") )

ABS_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
DEBUG = os.getenv("DJANGO_DEBUG") != "False"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATICFILES_DIR = os.path.join(BASE_DIR, "staticfiles")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_DIR = os.path.join(BASE_DIR, "static")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY",)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')


INSTALLED_APPS = [
    # 'admin_volt.apps.AdminVoltConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # local APP
    'core',
    'account',
    'app',

    #extra apps
    'corsheaders',
    'ckeditor',
    #for swagger ui
    'drf_yasg',
    'rest_framework_swagger',
    'djoser',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
USE_TZ = True
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'core.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME':  os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER':  os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST':  os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}  

AUTH_PASSWORD_VALIDATORS = [    {        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    },]

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'auth/login/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 	#MEDIA_DIR
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#access DRF features
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

CORS_ALLOWED_ORIGINS= os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS

AUTH_USER_MODEL = 'account.user'  #'app.User'

#authentication
DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    'ACTIVATION_URL':'auth/activation/{uid}/{token}', 
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password-reset/{uid}/{token}', 
    'LOGOUT_ON_PASSWORD_CHANGE': False,
    'SERIALIZERS': {
        'user_create': 'account.serializers.UserCreateSerializer',
        'current_user': 'account.serializers.UserSerializer',
    },
    'EMAIL':{
     'password_reset':'account.views.PasswordResetEmail'
    }
}
class MyTokenObtainPairViewLazy(LazyObject):
    def _setup(self):
        from account.views import MyTokenObtainPairView
        self._wrapped = MyTokenObtainPairView()

MyTokenObtainPairView = MyTokenObtainPairViewLazy
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,

    # use the custom token serializer
    'TOKEN_SERIALIZER': MyTokenObtainPairView,

    # add the custom claims to the token
    'CLAIMS': {
        'name': 'auth.name',
        'role': 'auth.role',
        'email': 'auth.email',
        'username' : 'auth.username'
    },
}




CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



#thumbnail settings
THUMBNAIL_ALIASES = {
    '': {
        'optimized': {
            'quality': 75,
            'format': 'JPEG',
        },
    },
}

SWAGGER_SETTINGS = {
     'LOGIN_URL': 'auth/login/',
       # Other Swagger settings
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}



CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
AUTH_TOKEN_VALIDITY = timedelta(days=1)


