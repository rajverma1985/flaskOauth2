import os

from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

oauth = OAuth()
oauth.init_app(app)

# Configuration for Google OAuth
google = oauth.register(
    name='google',
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    authorize_url=os.getenv('authorize_url'),
    authorize_params=None,
    access_token_url=os.getenv('access_token_url'),
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/callback',
    client_kwargs={'scope': 'openid profile email'},
)


# Configuration for GitHub OAuth
# github = oauth.register(
#     name='github',
#     client_id='YOUR_GITHUB_CLIENT_ID',
#     client_secret='YOUR_GITHUB_CLIENT_SECRET',
#     authorize_url='https://github.com/login/oauth/authorize',
#     authorize_params=None,
#     access_token_url='https://github.com/login/oauth/access_token',
#     access_token_params=None,
#     redirect_uri='http://localhost:8000/callback',
#     client_kwargs={'scope': 'user:email'},
# )

@app.route('/')
def welcome():
    return "Welcome click this link to login <a href=login>LOGIN</a>"


@app.route('/login')
def login():
    return google.authorize_redirect()  # or github.authorize_redirect()


@app.route('/callback')
def callback():
    token = google.authorize_access_token()  # or github.authorize_access_token()
    user_info = google.parse_id_token(token)  # or github.get('user')

    # Here, you have user information. You can now authenticate and authorize the user.

    return 'You are now logged in.'


@app.route('/logout')
def logout():
    session.pop('user_info', None)  # Assuming you're using sessions
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
