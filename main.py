from flask import Flask, redirect, current_user, current_app, url_for, session, abort, urlencode, secrets

app = Flask(__name__)

# Google OAuth 2.0 documentation:
# https://developers.google.com/identity/protocols/oauth2/web-server#httprest
app.config['OAUTH2_IDP'] = {"google":
    {
        "client_id": "796336461457-40a3ffvmju8i24m0ov9b4hs8m2k5bh4p.apps.googleusercontent.com",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_secret": "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",
        "redirect_uris": ["http://localhost:5000/callback/google"],
        "javascript_origins": ["http://localhost:5000"]},
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email']
}


@app.route('/')
def login():
    return "Hello What's up?"


@app.route('/authorize/<idp>')
def oauth2_authorize(idp):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(idp)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=idp,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
