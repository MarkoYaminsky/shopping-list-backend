from .base import *

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

WSGI_APPLICATION = "app.shopping_list_backend.wsgi.application"

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = DEBUG

SPECTACULAR_SETTINGS = {
    "TITLE": "Task reminder",
    "DESCRIPTION": "A project which goal is to help organize one's tasks and activities.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
