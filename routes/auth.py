from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session

auth = Blueprint('auth', __name__)

# Hard-coded user data
users = {'admin': 'admin'}

@auth.route("/login", methods=["GET"])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username and password:
        # Check username and password (this is just a placeholder - replace with your actual logic)
        if username == 'admin' and password == 'password':
            return redirect(url_for('auth.home'))
        else:
            flash('Invalid username or password')
    return render_template("auth/login.html")

@auth.route("/forgot_password", methods=["GET"])
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth.route("/home", methods=["GET"])
def home():
    return render_template("auth/home.html")