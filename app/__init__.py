import os

from flask import Flask
from config import Config
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        server_metadata_url=app.config['CONF_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
