from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from models import User, CRUD, Base
from routes.store import store
from routes.admin import admin
from routes.organization import organization
from routes.technician import technician
from routes.wholesaler import wholesaler
from routes.contractor import contractor
from routes.auth import auth

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Update the database URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

app.register_blueprint(store)
app.register_blueprint(admin)
app.register_blueprint(organization)
app.register_blueprint(technician)
app.register_blueprint(wholesaler)
app.register_blueprint(contractor)
app.register_blueprint(auth)

db = SQLAlchemy(app)



if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)
    app.run(debug=True,port=5053)


