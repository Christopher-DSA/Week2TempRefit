from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
# from models import User, get_session
from models import User,Store,get_session, CRUD
from functools import wraps
import pandas as pd
import os
# from main import app

# from flask_login import login_user,login_required,logout_user
auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = User.get_user_by_email(email)
        
        if user and user.password == password:  # A basic check, but you should hash and verify passwords securely.
            session['user_id'] = user.user_id  # Store user ID in session
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
            
        return "Invalid credentials", 401
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
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
@login_required
def home():
    user=session.get('user_id')
    return render_template("auth/home.html",user=user)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        print(username)
        print(password)
        print(user_type)
        if not username or not password or not user_type:
            flash('Please fill out all fields.')
        
        else:
            new_user = CRUD.create(User, email=username, password=password, role=user_type)
            new_user = User.get_user_by_email(username)
            session['user_id'] = new_user.user_id

            print(session)
            print(new_user.role)
            

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




