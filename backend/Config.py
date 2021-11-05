import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_SERVER = os.environ['POSTGRES_SERVER']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_SCHEMA = 'social_media'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_BINDS = {
        'postgresql': f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_TIMEOUT = 60  # 1 HOUR
    REFRESH_TOKEN_TIMEOUT = 14400  # 10 days
