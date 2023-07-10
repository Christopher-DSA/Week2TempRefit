from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response



contractor = Blueprint('contractor', __name__)

# @contractor.route("/contractor/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('contractor/dashboard.html')