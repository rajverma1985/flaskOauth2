import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID'),
    CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    CONF_URL = os.environ.get('CONF_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

