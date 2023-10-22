import os, secrets
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template, flash, current_app, abort, request
from authlib.integrations.flask_client import OAuth
# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# login = LoginManager(app)
# login.login_view = 'index'

oauth = OAuth()
oauth.init_app(app)

# Configuration for Oauth provider
app.config['providers'] = {
    'google': {'client_id': os.environ.get('client_id'),
               'client_secret': os.environ.get('client_secret'),
               'authorize_url': os.environ.get('authorize_url'),
               'access_token_url': os.environ.get('access_token_url'),
               'client_kwargs': {'scope': 'openid profile email'},
                'userinfo': {
                            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
                            'email': lambda json: json['email'],
                            },
               'scopes': ['https://www.googleapis.com/auth/userinfo.email']
               },
    'test': {
        'client_id': None
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorize/<provider>')
def login(provider):
    provider_data = current_app.config['providers'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@app.route('/callback/<provider>')
def callback(provider):
    provider_data = current_app.config['providers'].get(provider)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['access_token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })

    # log the user in
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
