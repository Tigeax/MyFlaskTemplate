from flask import Blueprint, render_template

import database
from database import db, db_conn

dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")


@dashboard.route('/')
def home():
    return render_template('home.html')