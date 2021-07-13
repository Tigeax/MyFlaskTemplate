from requests_oauthlib import OAuth2Session
from flask import Blueprint, render_template, session, url_for, jsonify
from werkzeug.local import LocalProxy

import os, datetime, random

from app.common.util import login_required, get_db


dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

db = LocalProxy(get_db)


@dashboard.route('/')
def home():
    return render_template('dashboard/home.html')



@dashboard.route('/graph_test_data')
def graph_test_data():

    measurementsData = [{'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}, {'x': datetime.datetime.now().strftime('%H:%M:%S'), 'y': random.randint(1,10)}]

    measurements = []

    for measurement in measurementsData:
        info = {'x': measurement['x'], 'y': measurement['y']}
        measurements.append(info)

    data = [{'name': 'testData', 'data': measurements}]

    return jsonify(data)
    





discordClientId = os.getenv('DISCORD_CLIENT_ID') # Get from https://discordapp.com/developers/applications

@dashboard.route('/discord_fetch_example')
@login_required
def discord_fetch_example():
    discord = OAuth2Session(discordClientId, token=session['discordToken'])
    response = discord.get('https://discordapp.com/api' + '/users/@me')

    print(response.json())

    name = response.json()['username']

    return render_template('home.html', name=name)