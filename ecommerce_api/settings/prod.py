import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['ecommerce-api-inht.onrender.com']

DATABASES = {
	"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY' : os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET' : os.environ['CLOUDINARY_API_SECRET']
}