from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from models import User, CRUDMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Update the database URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import Base
db = SQLAlchemy(app)


# Optional: If you have routes, register them here

# from routes import your_blueprint
from routes.store import store
from routes.admin import admin
from routes.organization import organization
from routes.technician import technician
from routes.wholesaler import wholesaler
from routes.contractor import contractor
from routes.auth import auth
# app.register_blueprint(your_blueprint)
app.register_blueprint(store)
app.register_blueprint(admin)
app.register_blueprint(organization)
app.register_blueprint(technician)
app.register_blueprint(wholesaler)
app.register_blueprint(contractor)
app.register_blueprint(auth)


if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)
    app.run(debug=True,port=8080)


