from flask import make_response, session, Blueprint
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician, Unit,Technician_Offer
from functools import wraps
technician = Blueprint('technician', __name__)

# @technician.route("/technician/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('technician/dashboard.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('auth/login.html')
        return f(*args, **kwargs)
    return decorated_function

def technician_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_id in the session is the email of the user.
        current_user_id = session.get('user_id')
        
        current_user = CRUD.read(User,user_id=current_user_id)
        
        if not current_user or current_user.role != 'technician':
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
    print("Rendering dashboard")
    user_current=session.get('user_id')
    return render_template("technician/dashboardtechnician.html", user=user_current)

@technician.route('/equipment/equipment_create', methods = ['GET', 'POST'])
def equipment_create():
    if request.method == 'POST':
        # Get data from form
        equipmentTagId = request.form.get('equipmentTagId')
        technicianId = request.form.get('technicianId')
        createDate = request.form.get('createDate')
        address = request.form.get('address')
        organizationId = request.form.get('organizationId')
        refrigerantType = request.form.get('refrigerantType')
        refrigerantId = request.form.get('refrigerantId')
        factoryCharge = request.form.get('factoryCharge')
        additionalCharge = request.form.get('additionalCharge')
        totalCharge = request.form.get('totalCharge')
        manufacturerName = request.form.get('manufacturerName')
        modelNumber = request.form.get('modelNumber')
        serialNumber = request.form.get('serialNumber')
        equipmentType = request.form.get('equipmentType')
        addRefrigerant = request.form.get('addRefrigerant')
        # sometimes these fields are empty
        if addRefrigerant == "yes":
            additionalRefrigerantAmount = request.form.get('additionalRefrigerantAmount')
            locationDescription = request.form.get('locationDescription')
        additionalNotes = request.form.get('additionalNotes')

        print("Equipment Create data successfully retrieved.")

        # latitude = request.form.get('latitude')
        # longitude = request.form.get('longitude')
        # print(f"Received coordinates: Latitude {latitude}, Longitude {longitude}")
        # return "Location received", 200
    
        # validate the data and pass data to database
        # unsure about some of these fields
        new_unit=CRUD.create(Unit,unit_id = equipmentTagId, technician_id = technicianId,
                               unit_name= serialNumber, tag_id = equipmentTagId, other_attribute = None,
                               installation_date = createDate, last_mainenance_date = createDate,
                               manufacturer = manufacturerName, model = modelNumber, 
                               type_of_refridgerant = refrigerantType, factory_charge_amount = factoryCharge,
                               unit_type = equipmentType, store_id = organizationId)
        
        return redirect(url_for('technician.dashboardtechnician'))
        
    
    return render_template('equipment/equipment_create.html')

##@technician.route('/equipment/repair')
##def repair():
 ##   return render_template('equipment/repair.html')



##@technician.route('/equipment/recovery')

##def recovery():

   ## return render_template('equipment/recovery.html')

@technician.route('/New Cylinder/tag-linked')
def add_qr():


    return render_template('New Cylinder/tag-linked.html')


@technician.route('/equipment/repair_ODS_Sheet')
def repair_ODS_Sheet():


    return render_template('equipment/repair_ODS_Sheet.html')



@technician.route('/equipment common/qr-scan')
def qr_scan():


    return render_template('equipment common/qr-scan.html')

@technician.route('/recovery/recovery-ods-sheet')
def recovery_ods_sheet():


    return render_template('recovery/recovery-ods-sheet.html')

@technician.route('/equipment/equipment_pages', methods = ['GET', 'POST'])
def equipment_page():
    
    if request.method == 'GET':
        return render_template('equipment/equipment_pages.html')
    else:
        print('error')
        return render_template('equipment/equipment_pages.html')
    
@technician.route('/equipment/ODS-history', methods = ['GET', 'POST'])
def ODS_history():

    if request.method == 'GET':
        return render_template('equipment/ODS-history.html')
    else:
        print('error')
        return render_template('equipment/ODS-history.html')
    
@technician.route('/equipment/maintenance_history', methods = ['GET', 'POST'])
def maintenance_history():

    if request.method == 'GET':
        return render_template('equipment/maintenance_history.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')


@technician.route('/register_technician/<token>/<int:id>', methods=['GET', 'POST'])
def signup_technician(token,id):
    if request.method == 'GET':
            contractor_id = id
            token = token
            print("Contractor ID: ", contractor_id)
            print("Token: ", token)
    return render_template('beta/register_technician.html',dt=contractor_id,tk=token)
    
@technician.route('/confirm_technician', methods=['GET', 'POST'])
def confirm_technician():
    if request.method == 'POST':
        contractor_id = request.form['dt']
        token = request.form['tk']
        print("Contractor ID: ", contractor_id)
        print("Token: ", token)
        
        CRUD.update(
            Technician_Offer,
            "offer_status",
            new = "Engaged", 
            token = token
        )
        return render_template('Login Flow/login.html')
       

        