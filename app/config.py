import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'uma-chave-secreta-muito-segura'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'postgresql://usuario:senha@localhost/nome_do_banco'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

