from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response



store = Blueprint('store', __name__)

# @store.route("/store/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('store/dashboard.html')

@store.route("/store/REFit-Tags", methods=['GET', 'POST'])
def REFit_Tags():
    return render_template('store/tag-shop.html')

@store.route("/store/checkout", methods=['GET', 'POST'])
def Checkout():
    return render_template('store/checkout-example.html')

@store.route("/store/free-tier", methods=['GET', 'POST'])
def free_tier():
    return render_template('store/free-tier.html')