from flask import Blueprint,  flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from datetime import datetime , timedelta
from models import User, Store, CRUD, Technician, User_Detail, Contractor
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

#This is just an example function. Not Working.
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
    

#LOGIN PAGE ROUTE
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
        
        details = CRUD.read(User_Detail, user_id=session.get('user_id'))
        
        session['user_first_name'] = details.first_name
        session['user_last_name'] = details.last_name
        
        print("From Auth.py: ", session['user_first_name'])
        print("From Auth.py: ", session['user_last_name'])
        
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

#LOGOUT ROUTE
@auth.route('/logout')
def logout():
    #Clear Session Variables
    session.clear()
    #Send user to login page
    return redirect(url_for('auth.login'))


##NEW DASHBOARD ROUTE
@auth.route('/new-dashboard', methods=['GET', 'POST'])
def new_dashboard():
    if request.method == 'GET':
        first_name = session.get('user_first_name')
        return render_template('technician/new-dashboard.html', user_first_name=first_name)
    elif request.method == 'POST':
        return render_template('technician/new-dashboard.html')

#FORGOT PASSWORD ROUTE
@auth.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    print("In forgot_password()")
    if request.method == "POST":
        print("POST request for forgot_password()")
        current_user_email = request.form.get('Email') # assuming username is the same as email
        print(current_user_email)
        # find user id for reset password token
        #CRUD.read(User, email=current_user_email)
        # token will expire after 24 hours
        #expires = datetime.timedelta(hours=24)
        # generate reset   password token
        access_token = create_access_token(identity=current_user_email) #,expires_delta=
        print(access_token)
        # add access token to user's records 
        
        CRUD.update(User,'jwt_token',new=access_token,email=current_user_email)
        # Embed the token in the reset password link
        #my_link= "http://172.16.224.205:5000/reset_password/{access_token}".format(access_token=access_token)
        url_form = url_for('auth.reset_password', access_token=access_token, _external=True)
        try:

            msg = MIMEMultipart()
            msg['From'] = 'refit_dev@sidneyshapiro.com'
            msg['To'] = 'refit_dev@sidneyshapiro.com'
            msg['Subject'] = 'Forgot Password Test Email'
            body = f'This is a test email for the forgot password feature. If you are receiving this email, it means that the forgot password feature is working.JWT token:{url_form}'
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
    
# route for validating token and redirecting to submit form 
@auth.route("/reset_password/<access_token>", methods=["GET", "POST"])
@jwt_required(optional=True) 
def redirect_to_reset_password(access_token): # access_token
    print("in redirect , decoded token")
    if request.method == "GET":
        token= decode_token(access_token)
        print(token)

        return redirect(url_for("auth.submit_reset_pass"))
    return render_template("Login Flow/reset.html")

# Route for submitting password form 
@auth.route("/submit_reset_pass", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        print("request POST")
        password1 = request.form['Password1']
        password2= request.form['Password2']
        print("got both password1 and password2")
        if password1 == password2:
            print('pass matches')
        	# Pull user email from session
            current_user_email = session.get('user_email')
        
            # Hash password
            message = {'password': password1}
            hashed_password = generate_hash(message, secret_key)
            print(hashed_password)
            # update the password in the database
            CRUD.update(User,'password',new= hashed_password, email=current_user_email)
            # delete the jwt token now that new pass   has been created
            CRUD.delete(User,'jwt_token', email=current_user_email)
            		

            		
            
            return redirect(url_for('auth.login'))
        else:
            return flash("Passwords do not match. PLease try again.")
    return render_template("Login Flow/reset.html")
        
   

    

# @auth.route("/reset_password/<access_token>", methods=["GET", "POST"])
# @jwt_required(optional=True)
# def reset_password(access_token):
    
#     if request.method == "POST":
#         # adding the following line because it redirects to non existent route reset_password/ when user submits
#         #redirect(url_for('auth.reset_password', access_token=access_token))

#         print("entered reset pass function")
#         # This block will be executed when the form is submitted
#         password1 = request.form['Password1']
#         password2 = request.form['Password2']
#         print("got both password1 and password2")

#         # Check if passwords match
#         if password1 == password2:
#             print('pass matches')
#             # Pull user email from session
#             current_user_email = session.get('user_email')

#             # Hash password
#             message = {'password': password1}
#             hashed_pass = generate_hash(message, secret_key)
#             print(hashed_pass)

#             # Update password in the database
#             CRUD.update(User, 'password', new=hashed_pass, email=current_user_email)

#             # Delete the jwt token in the database now that the new password has been set.
#             CRUD.delete(User, 'jwt_token', email=current_user_email)

#             return redirect(url_for('auth.login'))
#         else:
#             print('passwords do not match')
#             return redirect(url_for('auth.login'))
#     else:
#         # This block will be executed when the page is initially loaded
#         decoded_token = decode_token(access_token)
#         print("entered reset_password()")
#         print(decoded_token)

#         user = get_jwt_identity()
#         print(user)
#         return render_template("Login Flow/reset.html")
    



##@auth.route("/reset_password/<access_token>.<access_token2>.<access_token3>", methods=["GET", "POST"])
# @auth.route("/reset_password/<access_token>", methods=["GET", "POST"]) # removed /<access_token>
# @jwt_required(optional=True)   

# def reset_password(access_token):   # amy need to remove access_token
#     #user = get_jwt_identity()  removing because user = None eventho jwt is real , 
#     decoded_token = decode_token(access_token)
#     # print("Decoded Token:", decoded_token)
#     print("entered reset_password()")
#     print(decoded_token)

#     user = get_jwt_identity()
#     print(user)
#     #return redirect(url_for("/reset_password"))
#     return render_template("Login Flow/reset.html")
# pull up user profile

# now that we have the user token decoded , attach function to reset password if possible


 
 # create a separete route and see html reset 
# @auth.route("/reset_password", methods=["POST"])
# def reset_password():
#     password1 = request.form['Password1']
#     password2 = request.form['Password2']
#     print("got both password1 and password2")
#     #check if passwords match
#     if password1 == password2:
        
#         print('pass matches')
#         # pull user email from session
#         current_user_email = session['user_email']

#         # hash password
#         message ={'password' :password1}
    
#         hashed_pass =  generate_hash(message,secret_key)
#         print(hashed_pass)
#         # update password in database
#         CRUD.update(User,'password',new=hashed_pass,email=current_user_email)

#         # delete the jwt token in the database now that new password has been set.
#         CRUD.delete(User,'jwt_token',email=current_user_email)
#         return redirect(url_for('auth.login'))

#     else:
#         print('passwords do not match')

#         return redirect(url_for('auth.login'))


#def protected():
    # Access the identity of the current user with get_jwt_identity
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
# requests.get(reset_password_link, headers=headers)
# headers = {
#     'Authorization': 'Bearer <token>',
# }

# def reset_password(access_token,access_token2,access_token3):


 
   

#     print('1234')
#     if request.method == "GET" :
#         full_token = access_token + '.' + access_token2 + '.' + access_token3
#         print(full_token)
           
        
    #     x =CRUD.read(User,'jwt_token',jwt_token=full_token)
    #     if x == None:
    #         return render_template("Account Setup/create.html")
    #     else:
    #         session['user_token'] = full_token
    #         print("found token", access_token)
       
    #     print('post method')

    
    #     return render_template("Login Flow/reset.html")
################################################################
        # get submitted form data
        # password1 = request.form['Password1']
        # password2 = request.form['Password2']
        # # check if passwords match
        # if password1 == password2:
        #     print('pass matches')
        #     # pull user email from session
        #     current_user_email = session['user_email']

        # # hash password
        # message ={'password' :password1}
    
        # hashed_pass =  generate_hash(message,secret_key)
        # print(hashed_pass)
        # # update password in database
        # CRUD.update(User,'password',new=hashed_pass,email=current_user_email)
        # return redirect(url_for('auth.login'))

        # else:
        #     print('passwords do not match')

        #     return redirect(url_for('auth.login'))
       

#HOME PAGE ROUTE (This doesn't need to be here. It's just an example.)
@auth.route("/home", methods=["GET"])
def home():
    user=session.get('user_id')
    return render_template("auth/home.html",user=user)


#START CREATION OF ACCOUNT ROUTE FOR ALL ROLES.
@auth.route("/create", methods=["GET", "POST"])
def register():
    session.clear()
    print("test")
    if request.method == 'POST': #if user completes this form and decides to not continue, the next time they login they will taken directly to the account_setup page.
        print("In Post")      
        #1. Get the data from the form.
        my_user_email = request.form['Email']
        password_1 = request.form['Password1']
        password_confirmation_2 = request.form['Password2']
        added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        #2 Check if the passwords match.
        if password_1 != password_confirmation_2:
            print("Passwords do not match")
        
        #3.Hashed version of the password for the database instead of plain text.
        message = {'password': password_1}
        result = generate_hash(message, secret_key)
        
        #4. Send the data to the database.
        is_email_already_in_use = CRUD.read(User, email=my_user_email)
        if is_email_already_in_use != None:
            #USER EMAIL ALREADY IN DATABASE
            print("User email already in database")
            return redirect('/')
        else:
            #Create a new user in the database.
            x = CRUD.create(User, False, email=my_user_email, password=result, role='not_selected', added_date=added_date, is_email_verified=False, has_ods_license=False)
            my_user_id = x.user_id
            session['user_id'] = my_user_id
            session['user_email'] = my_user_email
            #5. Move on to the select role page (Technician, Admin, Contractor, Wholesaler)
            return render_template('/Account Setup/setup.html')
                

    
    elif request.method == 'GET':
        print("In Get")
        return render_template('Account Setup/create.html')
        #Call the send email function.
        #email() Uncomment this function when you want to send an email. You must have a local SMTP server running. Port 1025.
        
#CREATE ACCOUNT SETUP ROUTE, ROLE SPECIFIC ACCOUNT SETUP (Technician, Admin, Contractor, Wholesaler)
@auth.route("/create-account-setup", methods=["GET", "POST"])
def account_setup():
    print("In account_setup()")
    #At this point, the user has already created an account and is now setting up their account. They have a row in the database.
    if request.method == 'POST':
        print("In Post for account setup")
        current_user_id = session.get('user_id')
        current_user_email = session.get('user_email')
        #get variables from form
        first_name = request.form['First Name']
        Last_name = request.form['Last Name']
        ODS_License = request.form['License']
        Company_name = request.form['Company Name']
        Company_branch_number = request.form['Branch Number']
        ODS_sheet_recipent_email = request.form['Recipient Email']
        Company_address = request.form['Company Address']
        Apartment_number = request.form['Suite Number']
        City = request.form['Company City']
        Company_province = request.form['Company Province']
        Postal_code = request.form['Postal Code']
        #Drop down menu for role, will add later
        selected_role = request.form['Selected_role']
        
        #Always do these two things.
        CRUD.update(User, 'role', new = selected_role, email = current_user_email)
        CRUD.create(User_Detail, False, first_name=first_name, last_name=Last_name, user_id = current_user_id)

        print("Selected role: ", selected_role)
        if selected_role == 'technician':
            CRUD.create(Technician, False, user_id = current_user_id, ods_licence_number=ODS_License)
        elif selected_role == 'contractor':
            CRUD.create(Contractor, False, user_id = current_user_id, companyName = Company_name, status = 'active', name = first_name, branchId = Company_branch_number)
        elif selected_role == 'wholesaler':
            pass
        elif selected_role == 'admin':
            pass
        else:
            print("Error, no role selected")
            #???? ods_license=ODS_License <- this goes in technician table, company_name=Company_name, company_branch_number=Company_branch_number ods_sheet_recipent_email=ODS_sheet_recipent_email
    
        CRUD.update(User, 'role', new = selected_role, email = current_user_email)
        #Send them back to login page:
        flash("Account created successfully! " + str(selected_role))
        return render_template('Login Flow/login.html')
    elif request.method == 'GET':
        print("In Get for account setup")
        return render_template('Account Setup/setup.html')
        


#ROLE ROUTE? NOT SURE WHAT THIS IS.
@auth.route('/role', methods=['POST'])
def handle_role():
    data = request.get_json()  # This will get the JSON data sent by the fetch call
    role_name = data['role']
    print(role_name)  # This will print the role name to the console
    # You can add additional logic here based on the role_name if needed
    return jsonify({'message': 'Successfully received the role name!'}), 200

#UPLOAD FILES ROUTE
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


#Use this route if you have a page that needs to go back to a role specific dashboard.
@auth.route('/back-by-role', methods=['GET'])
def back_by_role():
    if request.method == 'GET':
        current_user_role = session.get('user_role')
        if current_user_role == 'technician':
            return redirect(url_for('technician.dashboardtechnician'))
        elif current_user_role == 'admin':
            print('admin pressed back button and should be redirected to admin dashboard')
        elif current_user_role == 'contractor':
            return redirect(url_for('contractor.dashboardcontractor'))
        elif current_user_role == 'wholesaler':
            print('wholesaler pressed back button and should be redirected to wholesaler dashboard')
        else:
            print("Error, no role selected")
            return redirect(url_for('auth.login'))
    

#############Only Account Settings Related Routes Below This Line#####################

#Settings Page
@auth.route('/settings', methods=['GET', 'POST'])
def settings_page():
    if request.method == 'GET':
        return render_template('admin/settings.html')
    elif request.method == 'POST':
        return render_template('admin/settings.html')
    
    
#Edit Profile Page
@auth.route('/edit-profile', methods=['GET', 'POST'])
def profile_edit_page():
    if request.method == 'GET':
        first_name = session.get('user_first_name')
        last_name = session.get('user_last_name')
        return render_template('admin/edit-profile.html',first_name=first_name,last_name=last_name)
    elif request.method == 'POST': #User has submitted the form to edit their profile.
        #Get the data from the form.
        # Initialize an empty dictionary to store the filled fields
        filled_fields = {}

        # List of all possible fields
        all_fields = ['first_name', 'last_name', 'telephone', 'ods_licence_number', 'street_address', 'suite_number', 'province', 'postal_code']

        current_user_id = session.get('user_id')
        # Check each field and add it to the dictionary if it's filled
        for field in all_fields:
            if request.form.get(field):
                filled_fields[field] = request.form.get(field)
        
        # Loop through each filled field and update it
        for field, value in filled_fields.items():
            if field == 'ods_licence_number':
                # Update the Technician table for ODS-certification
                CRUD.update(Technician, field, new=value, user_id=current_user_id)
            elif field == 'first_name':
                session['user_first_name']= filled_fields['first_name']
                CRUD.update(User_Detail, field, new=value, user_id=current_user_id)
            elif field == 'last_name':
                session['user_last_name'] = filled_fields['last_name']
                CRUD.update(User_Detail, field, new=value, user_id=current_user_id)
            else:
                # Update the User_Detail table for all other fields
                CRUD.update(User_Detail, field, new=value, user_id=current_user_id)
                
        return redirect('/edit-profile')
    
    
#Edit Acccount Settings Page
@auth.route('/account-settings', methods=['GET', 'POST'])
def account_settings_page():
    if request.method == 'GET':
        first_name = session.get('user_first_name')
        last_name = session.get('user_last_name')
        return render_template('admin/account.html',first_name=first_name,last_name=last_name)
    elif request.method == 'POST':
        return render_template('admin/account.html')
    
#Edit Acccount Settings Page
@auth.route('/membership', methods=['GET', 'POST'])
def membership_settings_page():
    if request.method == 'GET':
        return render_template('admin/membership.html')
    elif request.method == 'POST':
        return render_template('admin/membership.html')
    
#Privacy Policy Page
@auth.route('/privacy-policy', methods=['GET', 'POST'])
def privacy_policy_page():
    if request.method == 'GET':
        return render_template('admin/private-policy.html')
    elif request.method == 'POST':
        return render_template('admin/private-policy.html')
    
#Contact Page
@auth.route('/contact_us', methods=['GET', 'POST'])
def contact_us_page():
    if request.method == 'GET':
        return render_template('admin/contact-us.html')
    elif request.method == 'POST':
        return render_template('admin/contact-us.html')
        



