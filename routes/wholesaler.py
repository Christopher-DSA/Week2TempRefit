from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request



wholesaler = Blueprint('wholesaler', __name__)

# @wholesaler.route("/wholesaler/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('wholesaler/dashboard.html')


@wholesaler.route("/formwholesaler", methods=["GET", "POST"])
def formwholesaler():
    if request.method == 'POST':
        # Get data from form
        name = request.form.get('name')
        companyName = request.form.get('companyName')
        branch = request.form.get('branch')
        mailingAddress = request.form.get('mailingAddress')
        mailingCity = request.form.get('mailingCity')
        mailingProvince = request.form.get('mailingProvince')
        mailingPostalCode = request.form.get('mailingPostalCode')
        billingAddress = request.form.get('billingAddress')
        billingCity = request.form.get('billingCity')
        billingProvince = request.form.get('billingProvince')
        billingPostalCode = request.form.get('billingPostalCode')
        phoneNumber = request.form.get('phoneNumber')

        # TODO: Validate the data

        # TODO: Pass data to database
        # create_wholesaler(name, email, password, companyName, branch, 
        #    mailingAddress, mailingCity, mailingProvince, mailingPostalCode, 
        #    billingAddress, billingCity, billingProvince, billingPostalCode, phoneNumber)

        flash('Registered successfully.')
        return redirect(url_for('wholesaler.dashboardwholesaler'))

    return render_template("wholesaler/formwholesaler.html")

@wholesaler.route("/dashboardwholesaler")
def dashboardwholesaler():
    # Render the dashboard
    return render_template("wholesaler/dashboardwholesaler.html")
