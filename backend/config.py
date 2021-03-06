from datetime import timedelta

from starlette.config import Config
from starlette.datastructures import Secret


config = Config('.env')

SECRET_KEY = config('SECRET_KEY', cast=Secret)
DATABASE_URL = config('DATABASE_URL', cast=Secret)
ACCESS_TOKEN_LIFETIME = timedelta(hours=12)
