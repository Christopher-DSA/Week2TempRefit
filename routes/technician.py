from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request



technician = Blueprint('technician', __name__)

# @technician.route("/technician/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('technician/dashboard.html')


@technician.route("/formtechnician", methods=["GET", "POST"])
def formtechnician():
    if request.method == 'POST':
        # Get data from form
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        companyName = request.form.get('companyName')
        dob = request.form.get('dob')
        odsLicenseNumber = request.form.get('odsLicenseNumber')
        gender = request.form.get('gender')
        addressLine = request.form.get('addressLine')
        province = request.form.get('province')
        city = request.form.get('city')
        postalCode = request.form.get('postalCode')
        phoneNumber = request.form.get('phoneNumber')

        print("Technician data successfully retrieved.")
        # validate the data and pass data to database

        # redirect to the appropriate page

        return redirect(url_for('technician.dashboardtechnician'))
    return render_template("technician/formtechnician.html")


@technician.route("/dashboardtechnician")
def dashboardtechnician():
    # Render the dashboard
    return render_template("technician/dashboardtechnician.html")

