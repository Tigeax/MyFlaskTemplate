import dotenv

# Load the environmental variables from the .env file
dotenv.load_dotenv()

import os
from flask import Flask, redirect

import database
from database import db, db_conn

from app.api.views import api
from app.auth.views import auth
from app.dashboard.views import dashboard


# Create the instance of our web application
app = Flask(__name__)

# Register views
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(dashboard, url_prefix="/dashboard")

# Close the database after a request has closed
app.teardown_appcontext(database.close_db)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def landing_page():
    return redirect('/dashboard')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
