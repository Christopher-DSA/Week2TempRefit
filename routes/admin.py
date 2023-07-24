from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response

# from models import User, get_session

from models import User, get_session
admin = Blueprint('admin', __name__)

@admin.route("/admin", methods=['GET'])
def user_page():
    
    data=get_session().query(User).all()

    
    return render_template('admin/admin.html', data=data)
# def dashboard():
#     return render_template('admin/dashboard.html')

#test comment