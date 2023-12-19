from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from flask import Flask, request, jsonify
from models import User, CRUD
from routes.store import store
from routes.admin import admin
from routes.organization import organization
from routes.technician import technician
from routes.wholesaler import wholesaler
from routes.contractor import contractor
from routes.cylinder import cylinder
from routes.auth import auth
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager #New package, you will need to pip install flask-jwt-extended.
from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

#Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)


app.register_blueprint(auth)
app.register_blueprint(store)
app.register_blueprint(admin)
app.register_blueprint(organization)
app.register_blueprint(technician)
app.register_blueprint(wholesaler)
app.register_blueprint(contractor)
app.register_blueprint(cylinder)


db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)
