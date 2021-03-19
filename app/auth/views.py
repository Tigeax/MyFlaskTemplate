from flask import Blueprint, render_template

import database
from database import db, db_conn

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route('/')
def landing_page():
    return render_template('login.html')