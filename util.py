from flask import session, redirect, url_for


# Function for the login_required decorator
# Check if the user is logged in. If not send them to the login page
def login_required(func):
    def secure_function():
        if "loggedin" not in session or session["loggedin"] is False:
            return redirect(url_for("auth.login"))
        return func()

    return secure_function
