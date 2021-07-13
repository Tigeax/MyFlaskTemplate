from flask import Blueprint
from werkzeug.local import LocalProxy

from app.common.util import get_db


api = Blueprint("api", __name__, template_folder="templates", static_folder="static")

db = LocalProxy(get_db)