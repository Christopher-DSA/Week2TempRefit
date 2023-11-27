from flask import Blueprint,  flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from datetime import datetime , timedelta
from models import User, Store, CRUD, Technician
from functools import wraps
import pandas as pd
import os
from dotenv import load_dotenv
 
#from main import app  
from utils.tokenize import generate_hash, generate_password
# from flask_login import login_user,login_required,logout_user
#Email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# FLASK_JWT imports for secure reset password tokens
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from flask_jwt_extended import  jwt_required, get_jwt_identity,create_access_token,decode_token


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


#Setup the Flask-JWT-Extended extension
# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# jwt = JWTManager(app)


def email():
    # This is your message.
    message_text = "Hello there!"

    # Using dummy email addresses for testing
    me = "me@example.com"  # Sender's email
    you = "you@example.com"  # Recipient's email

    # Create a text/plain message
    msg = MIMEText(message_text)

    msg['Subject'] = 'A test message, verification email'
    msg['From'] = me
    msg['To'] = you

    # Send the message via a local SMTP server
    s = smtplib.SMTP('localhost', 1025)
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("Received POST request for login.")
        
        #1. Get the data from the form.
        entered_email = request.form["Email"]
        password = request.form["Password"]
        
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
        session['user_email'] = entered_email # Store user email in session
        session['user_id'] = current_user.user_id # Store user ID in session
        print("From Auth.py: ", session['user_email'])
        
        #5. Redirect to the appropriate page based on the user's role.
        print("About to enter if statement for password check")
        if (db_password == result):# hashed and verified password securely. Updated from previous basic check.
            session["user_id"] = current_user.user_id  # Store user ID in session
            if current_user.role=='technician':
                #store tech id in session.
                session['user_role'] = 'technician'
                current_user_id=session.get('user_id')
                current_tech_id = CRUD.read(Technician, user_id=current_user_id).technician_id
                session['tech_id'] = current_tech_id
                print(current_tech_id)
                #A Technician has logged in! This is now functional.
                return redirect(url_for('technician.dashboardtechnician'))
            elif current_user.role=='admin':
                session['user_role'] = 'admin'
                #An admin has logged in! This is now functional.
                return redirect(url_for('admin.user_page'))
            elif current_user.role=='contractor':
                session['user_role'] = 'contractor'                
                #A contractor has logged in! This is now functional.
                return redirect(url_for('contractor.dashboardcontractor'))
            elif current_user.role=='wholesaler':
                session['user_role'] = 'wholesaler'                
                #A wholesaler has logged in! This is now functional.
                return redirect(url_for('wholesaler.dashboardwholesaler'))
        else:
            return flash("Invalid username or password.")
    elif request.method == "GET":
        print('GET request login page')                
        return render_template('Login Flow/login.html')
    else:
        print('Error in login()')
    
@auth.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('auth.login'))



@auth.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    print("In forgot_password()")
    if request.method == "POST":
        print("POST request for forgot_password()")

        


        
        current_user_email = request.form.get('Email') # assuming username is the same as email
        # find user id for reset password token
        #CRUD.read(User, email=current_user_email)
        # token will expire after 24 hours
        #expires = datetime.timedelta(hours=24)
        # generate reset   password token
        access_token = create_access_token(identity=current_user_email) #,expires_delta=
        # add access token to user's records 
        CRUD.update(User,'jwt_token',new=access_token,email=current_user_email)
        # Embed the token in the reset password link
        my_link= "http://172.16.224.205:5000/reset_password/{access_token}".format(access_token=access_token)
        try:

            msg = MIMEMultipart()
            msg['From'] = 'refit_dev@sidneyshapiro.com'
            msg['To'] = 'refit_dev@sidneyshapiro.com'
            msg['Subject'] = 'Forgot Password Test Email'
            body = f'This is a test email for the forgot password feature. If you are receiving this email, it means that the forgot password feature is working.JWT token:{my_link}'
            msg.attach(MIMEText(body, 'plain'))
                
            email_text = msg.as_string()
            #Send an email to the email address typed in the form.
            smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)  # Using SMTP_SSL for secure connection
            smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')  # Log in to the server
            smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
            smtpObj.quit()  # Quitting the connection
            print("Email sent successfully!")
        except Exception as e:
            print("Oops, something went wrong: ", e)

        
        print(email)
        flash("If your email is registered with us, you'll receive a password reset link shortly.")

        session['user_email'] = current_user_email
       
        
        #return render_template('Login Flow/reset.html')
        return render_template("Login Flow/forgot.html")

           
    elif request.method == "GET":
        return render_template("Login Flow/forgot.html")
    

@auth.route("/reset_password/<access_token>.<access_token2>.<access_token3>", methods=["GET", "POST"])
#@jwt_required()

#def protected():
    # Access the identity of the current user with get_jwt_identity
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
# requests.get(reset_password_link, headers=headers)
# headers = {
#     'Authorization': 'Bearer <token>',
# }

def reset_password(access_token,access_token2,access_token3):


 
   

    print('1234')
    if request.method == "GET" :
        full_token = access_token + '.' + access_token2 + '.' + access_token3
        print(full_token)
           
        
        x =CRUD.read(User,'jwt_token',jwt_token=full_token)
        if x == None:
            return render_template("Account Setup/create.html")
        else:
            session['user_token'] = full_token
            print("found token", access_token)
       
        print('post method')

    
        return render_template("Login Flow/reset.html")

        # get submitted form data
        # password1 = request.form['Password1']
        # password2 = request.form['Password2']
        # check if passwords match
        # if password1 == password2:
        #     print('pass matches')
        #     # pull user email from session
        #     current_user_email = session['user_email']

        #     # hash password
        #     message ={'password' :password1}
           
        #     hashed_pass =  generate_hash(message,secret_key)
        #     print(hashed_pass)
        #     # update password in database
        #     CRUD.update(User,'password',new=hashed_pass,email=current_user_email)
        #     return redirect(url_for('auth.login'))

        # else:
        #     print('passwords do not match')

        #     return redirect(url_for('auth.login'))
       

        
        

@auth.route("/success",methods=["GET","POST"])
def success_pass(): 
    #get submitted form data
    password1 = request.form['Password1']
    password2 = request.form['Password2']
    #check if passwords match
    if password1 == password2:
        
        print('pass matches')
        # pull user email from session
        current_user_email = session['user_email']

        # hash password
        message ={'password' :password1}
    
        hashed_pass =  generate_hash(message,secret_key)
        print(hashed_pass)
        # update password in database
        CRUD.update(User,'password',new=hashed_pass,email=current_user_email)
        return redirect(url_for('auth.login'))

    else:
        print('passwords do not match')

        return redirect(url_for('auth.login'))







@auth.route("/home", methods=["GET"])

def home():
    user=session.get('user_id')
    return render_template("auth/home.html",user=user)

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
        #is_email_already_in_use = CRUD.read(User, email=user_email)
        is_email_already_in_use = False
        # print(is_email_already_in_use)
        # if is_email_already_in_use == None:
        #     #USER DOES NOT EXIST IN DATABASE
        #     pass
        # else:
        #     CRUD.create(User, False, email=user_email, password=result, role='not_selected', added_date=added_date, is_email_verified=False)
        
        #print(user_email,password_1,password_confirmation_2,added_date)
        
        #4. Move on to verify email page
        #return render_template('/Login Flow/verify.html')
        
        #5. Move on to the select role page (Technician, Admin, Contractor, Wholesaler)
        return render_template('/Account Setup/setup.html')
    
    elif request.method == 'GET':
        print("In Get")
        return render_template('Account Setup/create.html')
        #Call the send email function.
        #email() Uncomment this function when you want to send an email. You must have a local SMTP server running. Port 1025.
        

@auth.route('/role', methods=['POST'])
def handle_role():
    data = request.get_json()  # This will get the JSON data sent by the fetch call
    role_name = data['role']
    print(role_name)  # This will print the role name to the console
    # You can add additional logic here based on the role_name if needed
    return jsonify({'message': 'Successfully received the role name!'}), 200

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



