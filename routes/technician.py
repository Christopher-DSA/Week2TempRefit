from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician
from functools import wraps
technician = Blueprint('technician', __name__)

# @technician.route("/technician/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('technician/dashboard.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def technician_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_id in the session is the email of the user.
        user_id = session.get('user_id')

        

        user = CRUD.read(User,user_id=user_id)[0]
        
        if not user or user.role != 'technician':
            # Either user doesn't exist, or the user is not an admin.
            return "Unauthorized", 403
        
        return f(*args, **kwargs)
    return decorated_function

@technician.route("/formtechnician", methods=["GET", "POST"])
def formtechnician():
    if request.method == 'POST':
        # Get data from form
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        companyName = request.form.get('companyName')
        # dob = request.form.get('dob')
        odsLicenseNumber = request.form.get('odsLicenseNumber')
        # gender = request.form.get('gender')
        addressLine = request.form.get('addressLine')
        province = request.form.get('province')
        city = request.form.get('city')
        postalCode = request.form.get('postalCode')
        phoneNumber = request.form.get('phoneNumber')

        print("Technician data successfully retrieved.")
        # validate the data and pass data to database

        new_detail=CRUD.create(User_Detail,user_id=session.get('user_id'),first_name=firstName,last_name=lastName, address=addressLine, province=province, city=city,postal_code=postalCode,telephone=phoneNumber)
        new_technician_detail=CRUD.create(Technician, ODS_licence_number=odsLicenseNumber,user_id=session.get('user_id'))
        return redirect(url_for('technician.dashboardtechnician'))
                    

        
    return render_template("technician/formtechnician.html")


@technician.route("/dashboardtechnician")
@login_required
@technician_required
def dashboardtechnician():
    # Render the dashboard
    user=session.get('user_id')
    return render_template("technician/dashboardtechnician.html", user=user)

@technician.route('/equipment/equipment_create')
def equipment_create():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        print(f"Received coordinates: Latitude {latitude}, Longitude {longitude}")
        return "Location received", 200
    return render_template('equipment/equipment_create.html')

@technician.route('/equipment/repair')
def repair():
    return render_template('equipment/repair.html')

@technician.route('/equipment/recovery')
def recovery():
    return render_template('equipment/recovery.html')



