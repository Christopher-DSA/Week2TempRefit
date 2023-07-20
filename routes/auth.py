from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session

auth = Blueprint('auth', __name__)

# Hard-coded user data
users = {'admin': 'admin'}


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            # just a placeholder - replace with  logic to check if user exists in database
            if username == 'admin' and password == 'password':
                return redirect(url_for('auth.home'))
            else:
                print('Invalid username or password')
    return render_template("auth/login.html")


@auth.route("/forgot_password", methods=["GET"])
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth.route("/home", methods=["GET"])
def home():
    return render_template("auth/home.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        license = request.form.get('license')
        if not username or not password or not user_type:
            flash('Please fill out all fields.')
        elif user_type == 'technician' and not license:
            flash('Technicians must enter a license number.')
        else:
            print('Registered successfully.')
            return redirect(url_for('auth.login'))
    print("******************************* failed to Register ********************************")   
    return render_template("auth/register.html")
