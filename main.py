#from dotenv import load_dotenv
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response
from routes.store import store
from routes.admin import admin
from routes.organization import organization
from routes.technician import technician
from routes.wholesaler import wholesaler
from routes.contractor import contractor
from routes.auth import auth
# import datetime


#load_dotenv()
app = Flask(__name__)




# Register blueprints
app.register_blueprint(store)
app.register_blueprint(admin)
app.register_blueprint(organization)
app.register_blueprint(technician)
app.register_blueprint(wholesaler)
app.register_blueprint(contractor)
app.register_blueprint(auth)


@app.route("/", methods=['GET'])
def login():
    return render_template('auth/login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)