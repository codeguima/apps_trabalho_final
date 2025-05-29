import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+mysqlconnector://positivo:root@db/sistemademensagem'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://rabbitmq:6379/0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
