import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #Указывает, где будет создана база данных

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        user=os.environ.get('DB_USER'),
        pw=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        db=os.environ.get('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    