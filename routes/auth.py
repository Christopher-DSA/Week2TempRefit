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
load_dotenv()
auth = Blueprint('auth', __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("Received POST request")
        entered_email = request.form["username"]
        password = request.form["password"]
        
        #Hashing the password to match the hashed password in the database. For security purposes.
        #hashed_password = generate_hash(password, os.getenv('HASH_SECRET'))
        hashed_password = generate_hash(password, current_app.secret_key)

        #Reminds user that they need to fill out all fields.
        if not entered_email or not password:
            flash("Please fill out all fields.")
            return redirect(url_for('login'))  # Redirecting to the login route
        
        #Find matching row in the database user table by email.
        user = CRUD.read(User, email=entered_email)
        print(user.password)
        
        if (user and user.password == hashed_password):# hashed and verified password securely. Updated from previous basic check.
            session["user_id"] = user.user_id  # Store user ID in session
            print(session)
            print(user.role)
            if user.role=='technician':
                return redirect(url_for('technician.dashboardtechnician'))
            elif user.role=='admin':
                return redirect(url_for('admin.user_page'))
            elif user.role=='contractor':
                return redirect(url_for('contractor.dashboardcontractor'))
            elif user.role=='wholesaler':
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
        email = request.form.get('username')
        new_password = request.form.get('new_password')
        
        if email and new_password:
            # Use a query to find the user by email
            
            # user = CRUD.get_user_by_email(email)
            users = CRUD.read(User, email=email)
           
            if users:
                user=users[0]
                
            #     # Use the CRUD update method to change the password
                updated_user = CRUD.update(User, user.user_id, password=new_password)
                return jsonify({'message': 'Password changed successfully'})
            else:
                return jsonify({'error': 'User not found'})

    return render_template("auth/forgot_password.html")



@auth.route("/home", methods=["GET"])

def home():
    user=session.get('user_id')
    return render_template("auth/home.html",user=user)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_detail = user_type

        hashed_password = generate_hash(password, current_app.secret_key)

        if not username or not password or not user_type:
            flash('Please fill out all fields.')
        
        else:
            CRUD.create(User, False, email=username, password=hashed_password, role=user_type, added_date=added_date)    

            # Redirect to different forms based on user_type
            if user_type == 'contractor':
                return redirect(url_for('contractor.formcontractor'))
            elif user_type == 'technician':
                return redirect(url_for('technician.formtechnician'))
            elif user_type == 'wholesaler':
                return redirect(url_for('wholesaler.formwholesaler'))
            elif user_type == 'admin':
                return redirect(url_for('auth.formadmin'))
            
            #return redirect(url_for('auth.login'))
    print("******************************* failed to Register ********************************")   
    return render_template("auth/register.html")


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




