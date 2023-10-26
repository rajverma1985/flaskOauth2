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
        server_metadata_url=config_class.CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    from app.main import bp
    app.register_blueprint(bp)

    return app
