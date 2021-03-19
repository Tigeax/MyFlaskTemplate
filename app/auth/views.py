from requests_oauthlib import OAuth2Session
from flask import Flask, request, session, Blueprint, render_template, redirect, url_for
import os

import database
from database import db, db_conn
from util import login_required


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# Disable SSL requirement
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Settings for your app
base_discord_api_url = 'https://discordapp.com/api'
client_id = r'822507064684314675' # Get from https://discordapp.com/developers/applications
client_secret = 'JIe-4gwCeZjTMcZj5FVlzjJAYjULJQqp'
redirect_uri='http://www.senthing.com:80/auth/discord_oauth_callback'
scope = ['identify', 'guilds']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'


@auth.route('/')
def login():
    if 'loggedin' in session and session['loggedin']:
        return redirect('/')
    else:
        return redirect(url_for('auth.discord_login'))


@auth.route('/discord_login')
def discord_login():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    return redirect(login_url, code=302)


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
    discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
    token = discord.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['loggedin'] = True
    session['discord_token'] = token
    return redirect('/login')


@auth.route('/profile')
@login_required
def profile():
    """
    Example profile page to demonstrate how to pull the user information
    once we have a valid access token after all OAuth negotiation.
    """
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me')
    # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
    return 'Profile: %s' % response.json()['id']