from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response



store = Blueprint('store', __name__)

# @store.route("/store/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('store/dashboard.html')