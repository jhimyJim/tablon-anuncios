import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = 'clave_secreta_tablon_anuncios'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'bd_anuncios.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False