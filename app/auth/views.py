from requests_oauthlib import OAuth2Session
from flask import Flask, request, session, Blueprint, render_template, redirect, url_for, flash
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.local import LocalProxy


from app.common.util import login_required, get_db


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


db = LocalProxy(get_db)


@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'GET':
        # Check if the user is already loggin in. If so redirect them to the dashboard homepage, otherwise return the login page.
        if 'loggedin' in session and session['loggedin']:
            return redirect(url_for('dashboard.home'))
        else:
            return render_template('auth/login.html')


    elif request.method == 'POST':
        # Attempt to login the user in, and return the login page

        email = request.form['email']
        password = request.form['psw']

        userId = dbQuery.get_user_id(email)

        if userId is None:
            flash("No user exists with that email")
            return render_template('auth/login.html')

        userPswHash = dbQuery.get_user_password_hash(userId)

        if check_password_hash(userPswHash, password):
            session['loggedin'] = True
            session['userId'] = userId
        else:
            flash("Invalid password")

        return redirect(url_for('auth.login'))



@auth.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('auth/register.html')


    if request.method == 'POST':
        # Attempt to register an account

        email = request.form['email']
        password1 = request.form['psw']
        password2 = request.form['psw-repeat']

        userId = dbQuery.get_user_id(email)

        if userId is not None:
            flash("A user with that email already exists")
            return render_template('register.html')    

        if password1 != password2:
            flash("Passwords do not match!")
            return render_template('register.html')

        password_hash = generate_password_hash(password1, 'sha256')

        dbQuery.register_user(email, password_hash)
    
        return redirect(url_for('auth.login'))



@auth.route('/logout')
def logout():
    for key in list(session.keys()):
        print(key)
        session.pop(key)

    return redirect(url_for('auth.login'))


# ---------------------------------------------------------
# Discord login
# ---------------------------------------------------------

# Disable SSL requirement
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Settings discord OAuth2 authentification
discordClientId = os.getenv('DISCORD_CLIENT_ID') # Get from https://discordapp.com/developers/applications
discordClientSecret = os.getenv('DISCORD_CLIENT_SECRET')
discordAuthScope = ['identify', 'guilds']
discordAuthRedirectUrl = 'http://www.senthing.com:80/auth/discord_oauth_callback'



@auth.route('/discord_login')
def discord_login():
    oauth = OAuth2Session(discordClientId, redirect_uri=discordAuthRedirectUrl, scope=discordAuthScope)
    discordLoginUrl, state = oauth.authorization_url('https://discordapp.com/api/oauth2/authorize')
    session['discordState'] = state
    return redirect(discordLoginUrl, code=302)


@auth.route("/discord_oauth_callback")
def discord_oauth_callback():
    """
    The callback we specified in our app.
    Processes the code given to us by Discord and sends it back
    to Discord requesting a temporary access token so we can
    make requests on behalf (as if we were) the user.
    e.g. https://discordapp.com/api/users/@me
    The token is stored in a session variable, so it can
    be reused across separate web requests.
    """

    discord = OAuth2Session(discordClientId, redirect_uri=discordAuthRedirectUrl, state=session['discordState'], scope=discordAuthScope)
    token = discord.fetch_token(
        'https://discordapp.com/api/oauth2/token',
        client_secret=discordClientSecret,
        authorization_response=request.url,
    )

    session['discordToken'] = token

    discord = OAuth2Session(discordClientId, token=session['discordToken'])
    response = discord.get('https://discordapp.com/api' + '/users/@me')

    session['loggedin'] = True
    session['userId'] = database.get_user_id_by_discord_id(response.json()['id'])

    return redirect(url_for('auth.login'))
