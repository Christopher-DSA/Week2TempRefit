from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request

from models import CRUDMixin, User, User_detail

technician = Blueprint('technician', __name__)

# @technician.route("/technician/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('technician/dashboard.html')


@technician.route("/formtechnician/<int:user_id>", methods=["GET", "POST"])
def formtechnician(user_id):
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

        new_detail=CRUDMixin.create(User_detail,user_id=user_id,first_name=firstName,last_name=lastName, birthdate=dob,ODS_license_number=odsLicenseNumber,gender=gender, address=addressLine, province=province, city=city,postal_code=postalCode,telephone=phoneNumber)
        # CRUDMixin.create(new_detail)

                    # new_user = CRUDMixin.create(User, email=username, password=password, role=user_type, added_date=license)

        # redirect to the appropriate page


        return redirect(url_for('technician.dashboardtechnician'))
    return render_template("technician/formtechnician.html",user_id=user_id)


@technician.route("/dashboardtechnician")
def dashboardtechnician():
    # Render the dashboard
    return render_template("technician/dashboardtechnician.html")

@technician.route('/equipment/equipment_create')
def equipment_create():
    return render_template('equipment/equipment_create.html')

@technician.route('/equipment/repair')
def repair():
    return render_template('equipment/repair.html')

@technician.route('/equipment/recovery')
def recovery():
    return render_template('equipment/recovery.html')



