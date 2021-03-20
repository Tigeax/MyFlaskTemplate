from requests_oauthlib import OAuth2Session
from flask import Blueprint, render_template, session
import os

import database
from database import db, db_conn
from util import login_required


dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

discordClientId = os.getenv('DISCORD_CLIENT_ID') # Get from https://discordapp.com/developers/applications


@dashboard.route('/home')
@login_required
def home():
    discord = OAuth2Session(discordClientId, token=session['discordToken'])
    response = discord.get('https://discordapp.com/api' + '/users/@me')

    print(response.json())

    name = response.json()['username']

    return render_template('home.html', name=name)



@dashboard.route('/')
def landing_page():
    return render_template('home.html')