import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #Указывает, где будет создана база данных

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db') #Адаптер + директория
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Чтобы изменения в бд не засоряли консоль

    