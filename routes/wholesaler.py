from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response



wholesaler = Blueprint('wholesaler', __name__)

# @wholesaler.route("/wholesaler/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('wholesaler/dashboard.html')