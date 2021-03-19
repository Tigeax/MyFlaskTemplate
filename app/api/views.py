from flask import Blueprint

import database
from database import db, db_conn

api = Blueprint("api", __name__, template_folder="templates", static_folder="static")