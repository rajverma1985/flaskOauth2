import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template, flash
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

oauth = OAuth()
oauth.init_app(app)

# Configuration for Oauth provider
app.config['providers'] = {
    'google': {'client_id': os.environ.get('client_id'),
               'client_secret': os.environ.get('client_secret'),
               'authorize_url': os.environ.get('authorize_url'),
               'access_token_url': os.environ.get('access_token_url'),
               'client_kwargs': {'scope': 'openid profile email'}
               },
    'test':{
        'client_id': None
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return 'test'


@app.route('/callback/<provider>')
def callback():
    return 'You are now logged in.'


@app.route('/logout')
def logout():
    # logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
