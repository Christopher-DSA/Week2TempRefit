from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from functools import wraps
from models import User

admin = Blueprint('admin', __name__)


#this is the decorator that is used to check if user is logged in.
#any page that the user is trying to access and its not available without login, 
#it'll check if user is in a session, and lets you access the page
#the session will also help pass user id and other data among pages 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_id in the session is the email of the user.
        email = session.get('user_id')

        

        user = User.get_user_by_email(email)
        
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
    

    data=get_session().query(User).all()

    
    return render_template('admin/admin.html', data=data)
# def dashboard():
#     return render_template('admin/dashboard.html')

#test comment