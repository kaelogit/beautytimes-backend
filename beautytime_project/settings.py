import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. Load environment variables from .env file (for local development)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# This reads from Render environment or your .env file
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
# Set this to False when deploying to Render
DEBUG = False 

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'beautytimes-backend.onrender.com', # Your Render URL
    '.onrender.com' # Allows all Render subdomains
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party Apps (Crucial for Images & Connection)
    'cloudinary_storage',  # Must be above cloudinary
    'cloudinary',
    'corsheaders',         # For frontend connection

    # My Custom Apps
    'inventory', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- Serves CSS/JS on Render
    'corsheaders.middleware.CorsMiddleware',      # <--- Allows Netlify to talk to Django
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
# Automatically handles Neon (on Render) and .env (Locally)
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


# --- STATIC & MEDIA CONFIGURATION (Django 5.0+ Style) ---

# 1. Static Files (CSS, JavaScript) -> Served by Whitenoise
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inventory', 'static'),
]

# 2. Media Files (Images Uploaded by You) -> Served by Cloudinary
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 3. Storage Engine Configuration
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Cloudinary Keys ---
# Replace these with your ACTUAL keys from the Cloudinary Dashboard
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dcohh6ywb', 
    'API_KEY': '721365887418313', 
    'API_SECRET': 'DDdZDqXn12_SEwngY_-_xsWk3-Y',
}


# --- CORS Configuration ---
# Allows your Netlify frontend to access the API
CORS_ALLOW_ALL_ORIGINS = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'