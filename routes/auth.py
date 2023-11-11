from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from datetime import datetime
from models import User, Store, CRUD
from functools import wraps
import pandas as pd
import os
from dotenv import load_dotenv
# from main import app
from utils.tokenize import generate_hash, generate_password
# from flask_login import login_user,login_required,logout_user
#Email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Load enviroment variables
load_dotenv()
#Server Email information
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
secret_key = os.getenv('HASH_SECRET')

#Blueprint for auth
auth = Blueprint('auth', __name__)

#Test function for email.
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("Received POST request for login.")
        
        #1. Get the data from the form.
        entered_email = request.form["username"]
        password = request.form["password"]
        
        #Reminds user that they need to fill out all fields.
        if not entered_email or not password:
            flash("Please fill out all fields.")
            return redirect(url_for('login'))  # Redirecting to the login route
    
        #2. Hash the password from the form.
        password_to_hash = password
        message = {'password': password_to_hash}
        result = generate_hash(message, secret_key)
        
        #3. Check if the email exists in the database.
        current_user = CRUD.read(User, email=entered_email)        
        
        # If no user is found with the entered email, redirect to the login page
        if not current_user:
            flash("No account found with that email. Please try again.")
            return redirect(url_for('login'))  # Redirecting to the login route
        
        #4. Check if the password matches the hashed password in the database.
        db_password = current_user.password
        
        #Session Variables
        session['user_email'] = entered_email
        print("From Auth.py: ", session['user_email'])
        
        #5. Redirect to the appropriate page based on the user's role.
        print("About to enter if statement for password check")
        if (db_password == result):# hashed and verified password securely. Updated from previous basic check.
            session["user_id"] = current_user.user_id  # Store user ID in session
            if current_user.role=='technician':
                #A Technician has logged in! This is now functional.
                return redirect(url_for('technician.dashboardtechnician'))
            elif current_user.role=='admin':
                #An admin has logged in! This is now functional.
                return redirect(url_for('admin.user_page'))
            elif current_user.role=='contractor':
                #A contractor has logged in! This is now functional.
                return redirect(url_for('contractor.dashboardcontractor'))
            elif current_user.role=='wholesaler':
                #A wholesaler has logged in! This is now functional.
                return redirect(url_for('wholesaler.dashboardwholesaler'))
        else:
            return flash("Invalid username or password.")
    
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('auth.login'))


@auth.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('username') # assuming username is the same as email
        #new_password = request.form.get('new_password')  # shouldn't this be deleted ? new password only happens in reset link sent after email authenticated
        
        if email :# removed 'and password' - because user forgot password and new password creation page is a link sent by email( if matches db)
           
            
            # user = CRUD.get_user_by_email(email)
            users = CRUD.read(User, email=email)
           

            if users:

                user=users[0]  #assuming each user has a distinct email and multiple users dont share one email
              # add code to email user with password reset link , if it matches account in database 
              # reset link should be a  new , secure page  if email was validated 
              # reset link should be created here and sent in the email if it was validated 
                reset_token = generate_reset_token(user)  # placeholder , need to create function to generate unqiue link
                send_reset_email(user.email, reset_token) 
            #def send_reset_email(email, reset_token):
            ##Create a Flask-Mail message:
            #msg = Message('Password Reset Request', sender='dev_refit@sidneyshapiro.com', recipient=[email])

            ## Customize the email body with the reset link:
            #reset_link = url_fgitor('auth.reset_password', token=reset_token, _external=True)
            #msg.body = f'Click the following link to reset your password: {reset_link}'

            # Send the email
            #mail.send(msg)
            


            #     # Use the CRUD update method to change the password
                updated_user = CRUD.update(User, user.user_id, password=new_password) # shouldn't this be happening in the reset pass page?
                return jsonify({'message': 'Password reset link sent '}) # removed 'Password changed successfully' because pass reset should be on a different page
            else:
                return jsonify({'error': 'User not found'})

    return render_template("auth/forgot_password.html")



@auth.route("/home", methods=["GET"])

def home():
    user=session.get('user_id')
    return render_template("auth/home.html",user=user)


# Replacing this with the new page from the design team.
# @auth.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user_type = request.form['user_type']
#         added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         user_detail = user_type

#         hashed_password = generate_hash(password, current_app.secret_key)

#         if not username or not password or not user_type:
#             flash('Please fill out all fields.')
        
#         else:
#             CRUD.create(User, False, email=username, password=hashed_password, role=user_type, added_date=added_date)    

#             # Redirect to different forms based on user_type
#             if user_type == 'contractor':
#                 return redirect(url_for('contractor.formcontractor'))
#             elif user_type == 'technician':
#                 return redirect(url_for('technician.formtechnician'))
#             elif user_type == 'wholesaler':
#                 return redirect(url_for('wholesaler.formwholesaler'))
#             elif user_type == 'admin':
#                 return redirect(url_for('auth.formadmin'))
            
#             #return redirect(url_for('auth.login'))
#     print("******************************* failed to Register ********************************")   
#     return render_template("auth/register.html")


@auth.route("/create", methods=["GET", "POST"])
def register():
    print("test")
    if request.method == 'POST':
        print("In Post")
        
        #1. Get the data from the form.
        user_email = request.form['Email']
        password_1 = request.form['Password1']
        password_confirmation_2 = request.form['Password2']
        added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        #1.5 Check if the passwords match.
        if password_1 != password_confirmation_2:
            print("Passwords do not match")
        
        #2.Hashed version of the password for the database instead of plain text.
        message = {'password': password_1}
        result = generate_hash(message, secret_key)
        
        #3. Send the data to the database.
        is_email_already_in_use = True
        if is_email_already_in_use:
            pass
        else:
            CRUD.create(User, False, email=user_email, password=result, role='not_selected', added_date=added_date, is_email_verified=False)
        
        #print(user_email,password_1,password_confirmation_2,added_date)
        
        #4. Move on to verify email page
        
        return render_template('/Login Flow/verify.html')
    
    elif request.method == 'GET':
        print("In Get")
        #Send an email
        print("Sending an email")
        #Call the send email function.
        send_email("refit713@gmail.com", "Hello!", "This is a test email from my own SMTP server!")

        return render_template('Account Setup/create.html')
        

@auth.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        file = request.files['file']
        
        
        if file and file.filename.endswith('.csv'):
            filename = os.path.join('/Users/sapnilsharma/sofvie', file.filename)
            file.save(filename)

            data = pd.read_csv(filename)
            for _, row in data.iterrows():
                
                
                entry = CRUD.create(Store,
                    
                    address=row['address'], 
                    
                )
                
            flash('Data successfully stored in the database', 'success')
            return redirect(url_for('auth.upload'))

    return render_template('auth/csv.html')




