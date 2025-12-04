import dj_database_url
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@8^v3!m9f*+!06%n&h#j%2m2!63t09n91_p$v43d0i01d7+u'

# SECURITY WARNING: don't run with debug turned on in production!
# Set to TRUE if testing locally to see errors, FALSE for live Render deployment
DEBUG = False 

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'beautytimes-backend.onrender.com',
    '.onrender.com'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'cloudinary_storage', 
    'cloudinary',
    'corsheaders', # <--- ADDED THIS (Critical Fix)

    # My custom apps
    'inventory', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Needed for files on Render
    'corsheaders.middleware.CorsMiddleware',      # Needed for Frontend connection
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beautytime_project.urls'

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

WSGI_APPLICATION = 'beautytime_project.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images, etc.)
# --- CRITICAL STATIC FILE CONFIGURATION ---

# 1. URL to access static files in the browser
STATIC_URL = 'static/'

# 2. Storage engine for Render (UNCOMMENTED THIS IS CRITICAL)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. Directories where Django should look for static files inside apps
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inventory', 'static'),
]

# 4. Destination for collected static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Configuration (Cloudinary)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CORS Configuration ---
CORS_ALLOW_ALL_ORIGINS = True

# --- Cloudinary Configuration ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dcohh6ywb', 
    'API_KEY': '721365887418313', 
    'API_SECRET': 'DDdZDqXn12_SEwngY_-_xsWk3-Y',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'