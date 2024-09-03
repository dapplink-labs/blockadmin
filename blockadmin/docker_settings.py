from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blockadmin",
        "USER": "blockeye",
        "PASSWORD": "9874e0ea9134d!X*314a27e",
        "HOST": "admindb"
    },
}

ALLOWED_HOSTS = ['*']

DEBUG = True
