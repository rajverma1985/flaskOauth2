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
        client_id=config_class.CLIENT_ID,
        client_secret=config_class.CLIENT_SECRET,
        server_metadata_url=config_class.CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
