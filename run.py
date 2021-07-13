import dotenv

# Load the environmental variables from the .env file
dotenv.load_dotenv()

import os
from flask import Flask, redirect, url_for

import app.common.database as database
import app.common.util as util

from app.api.views import api
from app.auth.views import auth
from app.dashboard.views import dashboard

# Create the instance of our web application
app = Flask(__name__)

db = database.Sqlite3Database()

# Register blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(dashboard, url_prefix="/dashboard")


# Close the database after a request has finished
app.teardown_appcontext(db._close_database)

# Flask configuration
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEVELOPMENT")
app.config['DATABASE'] = db

app.jinja_env.globals.update(db=db, util=util)


@app.route('/')
def landing_page():
    return redirect(url_for('dashboard.home'))


if __name__ == "__main__":
    app.run()
