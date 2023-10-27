from flask import redirect, url_for, session, render_template
from app.main import bp
from app import oauth


@bp.route('/')
def homepage():
    user = session.get('user')
    return render_template('index.html', user=user)


@bp.route('/login')
def login():
    redirect_uri = url_for('main.auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')


@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
