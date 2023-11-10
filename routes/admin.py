from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from functools import wraps

#flask.cli does not have a get_version function so we will comment this out for now. Not sure how this got here.
#from flask.cli import get_version
from models import User, Store, CRUD


admin = Blueprint('admin', __name__)


#this is the decorator that is used to check if user is logged in.
#any page that the user is trying to access and its not available without login, 
#it'll check if user is in a session, and lets you access the page
#the session will also help pass user id and other data among pages 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_email in the session is the email of the user.
        user_email = session.get('user_email')

        user = CRUD.read(User, email = user_email)
        
        if not user or user.role != 'admin':
            # Either user doesn't exist, or the user is not an admin.
            return "Unauthorized", 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin.route("/admin", methods=['GET'])
#admin page access requires login.
@login_required
@admin_required
def user_page():
    user_email = session.get('user_email')
    print("From Admin.py: ", session['user_email'])
    data = CRUD.read(User, all = True, email = user_email)    
    return render_template('admin/admin.html', data=data)
# def dashboard():
#     return render_template('admin/dashboard.html')

#test comment