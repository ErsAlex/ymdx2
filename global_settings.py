import environ
from pathlib import Path


env = environ.Env()
environ.Env.read_env()



DB_HOST = env.str('DB_HOST')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_NAME = env.str('DB_NAME')
DB_USERNAME = env.str('DB_USERNAME')
DB_PORT = env.str('DB_PORT')
DB_DSN = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL = env.str('DB_URL')

OWN_EMAIL = env.str('OWN_EMAIL')
OWN_EMAIL_PASSWORD = env.str('OWN_EMAIL_PASSWORD')
SMTP_SSL = env.str('SMTP_SSL')
SMTP_PORT = env.int('SMTP_PORT')

SECRET_KEY = env.str('SECRET_KEY')
ACCESS_TOKEN_EXPIRE = env.int('ACCESS_TOKEN_EXPIRE')
REFRESH_TOKEN_EXPIRE = env.int('REFRESH_TOKEN_EXPIRE')
