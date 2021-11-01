import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = "SWOOP"
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
