from functools import wraps
from flask import session, redirect, url_for, g, current_app

def get_db():
    return current_app.config['DATABASE']

# Function for the login_required decorator
# Check if the user is logged in. If not send them to the login page
def login_required(func):
    @wraps(func)
    def secure_function():

        if "loggedin" not in session or session["loggedin"] is False:
            return redirect(url_for("auth.login"))

        return func()

    return secure_function


def getNewChartId():

    numCharts = 0 if 'numCharts' not in g else g.numCharts + 1
    
    g.numCharts = numCharts
    return numCharts