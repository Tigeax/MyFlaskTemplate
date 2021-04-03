from flask import Blueprint

import app.common.database as database

api = Blueprint("api", __name__, template_folder="templates", static_folder="static")