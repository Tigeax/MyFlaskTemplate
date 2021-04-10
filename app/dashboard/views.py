from requests_oauthlib import OAuth2Session
from flask import Blueprint, render_template, session, url_for
import os

import app.common.database as database
import app.common.databaseQueries as dbQuery
from app.common.util import login_required


dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")




@dashboard.route('/')
@login_required
def home():
    return render_template('dashboard/home.html', userId=session['userId'])





discordClientId = os.getenv('DISCORD_CLIENT_ID') # Get from https://discordapp.com/developers/applications

@dashboard.route('/discord_fetch_example')
@login_required
def discord_fetch_example():
    discord = OAuth2Session(discordClientId, token=session['discordToken'])
    response = discord.get('https://discordapp.com/api' + '/users/@me')

    print(response.json())

    name = response.json()['username']

    return render_template('home.html', name=name)