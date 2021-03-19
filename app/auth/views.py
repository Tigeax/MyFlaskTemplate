from requests_oauthlib import OAuth2Session
from flask import Flask, request, session, Blueprint, render_template, redirect, url_for
import os

import database
from database import db, db_conn
from util import login_required


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# Disable SSL requirement
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Settings discord OAuth2 authentification
discordClientId = os.getenv('DISCORD_CLIENT_ID') # Get from https://discordapp.com/developers/applications
print(discordClientId)
discordClientSecret = os.getenv('DISCORD_CLIENT_SECRET')
discordAuthScope = ['identify', 'guilds']
discordAuthRedirectUrl = 'http://www.senthing.com:80/auth/discord_oauth_callback'


@auth.route('/')
def login():
    if 'loggedin' in session and session['loggedin']:
        return redirect('/')
    else:
        return redirect(url_for('auth.discord_login'))


@auth.route('/logout')
def logout():
    for key in list(session.keys()):
        print(key)
        session.pop(key)

    return redirect(url_for('auth.login'))


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
