from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response



admin = Blueprint('admin', __name__)

# @admin.route("/admin/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('admin/dashboard.html')