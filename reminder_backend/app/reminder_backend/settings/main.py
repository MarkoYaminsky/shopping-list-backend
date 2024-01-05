from .base import *

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS: list[str] = []

WSGI_APPLICATION = "app.reminder_backend.wsgi.application"

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = DEBUG
