from flask import make_response, session, Blueprint, request
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from functools import wraps
from datetime import datetime

# email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#flask.cli does not have a get_version function so we will comment this out for now. Not sure how this got here.
#from flask.cli import get_version
from models import User, Store, CRUD, User_Support, User_Detail


admin = Blueprint('admin', __name__)


#this is the decorator that is used to check if user is logged in.
#any page that the user is trying to access and its not available without login, 
#it'll check if user is in a session, and lets you access the page
#the session will also help pass user id and other data among pages 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Assuming the user_email in the session is the email of the user.
        If the user_email is not in the session, redirect to login page.
        """
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

@admin.route("/admin/support_tickets", methods=['GET'])
def support_tickets():
    tickets = CRUD.read(User_Support, all = True)
    
    # for each ticket get the email of the user
    # emails = []
    # for ticket in tickets:
    #     email = CRUD.read(User, user_id = ticket.user_id).email
    #     emails.append(email)
    return render_template('admin/support_tickets.html', tickets = tickets)

@admin.route("/admin/email", methods=['POST'])
def new_email():
    if request.method == 'POST':
        #1. Capture message from text area, get ticket ID and user name from session
        reply_to_user = request.form['message']
        ticket_id = session.get('selected_ticket_id')
        user_name = session.get('user_name')
        #2. Get the user email and using user id from table
        selected_user_id = session.get('selected_user_id')
        email = CRUD.read(User, user_id = selected_user_id, all=False).email

        #3. Send the message to the user using the message and email
        msg = MIMEMultipart()
        # From Support
        msg['From'] = 'refit_dev@sidneyshapiro.com'
        # To User
        msg['To'] = email
        # Subject
        msg['Subject'] = f'RE: Support Ticket #{ticket_id}'

        # Attach the HTML content
        msg.attach(MIMEText(reply_to_user, 'html'))

        email_text = msg.as_string()
        # Send an email to the email address typed in the form.
        smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)  # Using SMTP_SSL for secure connection
        smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')  # Log in to the server
        smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
        smtpObj.quit()  # Quitting the connection
        
        return render_template('admin/successful-response.html', email = email, user_name = user_name)

@admin.route("/admin/reply", methods=['POST'])
def reply_to_ticket_page():
    if request.method == 'POST':
        # 1. Retrieve Selected User Id, User Name, and Ticket ID
        selected_user_id = request.form['selected_user_id']
        selected_ticket_id = request.form['selected_ticket_id']

        user_first_name = CRUD.read(User_Detail, user_id = selected_user_id, all=False).first_name
        user_last_name = CRUD.read(User_Detail, user_id = selected_user_id, all=False).last_name
        user_name = user_first_name + " " + user_last_name

        # 2. Store Selected User Id and ticket ID in Session
        session['selected_user_id'] = selected_user_id
        session['selected_ticket_id'] = selected_ticket_id
        session['user_name'] = user_name

        # 3. Render the Response page.
        return render_template('admin/response.html', selected_user_id = selected_user_id, selected_ticket_id = selected_ticket_id, user_name = user_name)
    
@admin.route("/admin/close_ticket", methods=['POST'])
def close_ticket():
    if request.method == 'POST':
        # 1. get current time and selected Ticket ID
        selected_ticket_id = request.form['selected_ticket_id']
        date = datetime.today()

        # 2. update the User Support Model with the current time
        CRUD.update(User_Support, ticket_id = selected_ticket_id, attr = 'date_ticket_closed', new = str(datetime.today()))

        # 3. Send the user an email stating the support ticket has been closed.

        # 4. Render the support_tickets page with the updated ticket closed.
        tickets = CRUD.read(User_Support, all = True)
        return render_template('admin/support_tickets.html', tickets = tickets)