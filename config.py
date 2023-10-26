import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CLIENT_ID = os.environ.get('CLIENT_ID'),
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    CONF_URL = os.environ.get('CONF_URL')
