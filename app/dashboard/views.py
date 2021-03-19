from requests_oauthlib import OAuth2Session
from flask import Blueprint, render_template, session

import database
from database import db, db_conn
from util import login_required


dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

client_id = r'822507064684314675' # Get from https://discordapp.com/developers/applications
base_discord_api_url = 'https://discordapp.com/api'


@dashboard.route('/')
@login_required
def home():
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me')

    print(response.json())

    name = response.json()['username']

    return render_template('home.html', name=name)