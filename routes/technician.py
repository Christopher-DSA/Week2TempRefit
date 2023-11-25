from flask import make_response, session, Blueprint
from flask import session
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician, Unit
from functools import wraps
import UUID_Generate
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

#?
@technician.route('/equipment/equipment_create', methods = ['GET', 'POST'])
def equipment_create():
    print("inside equipment_create")
    if request.method == 'POST':
        print("inside post")
        #Get users technician id
        current_user_id=session.get('user_id')
        
        current_tech_id = CRUD.read(Technician, user_id=current_user_id).technician_id
        
        print(current_tech_id)
        
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
        
        ###################################################
        ###########Add new unit to the database############
        ###################################################
        
        #1. Create new row in Unit table
        #removed tag_id = equipmentTagId for testing
        # new_unit=CRUD.create(Unit, manufacturer = manufacturerName, model = modelNumber, 
        #                        type_of_refrigerant = refrigerantType, factory_charge_amount = factoryCharge,
        #                        unit_type = equipmentType, store_id = organizationId)
        
        
        my_unit=CRUD.create(Unit, type_of_refrigerant = refrigerantType, installation_date = createDate, manufacturer = manufacturerName, unit_type = equipmentType, factory_charge_amount = factoryCharge, serial_number = serialNumber, technician_id = current_tech_id)    
        #new_row =CRUD.create(Cylinder, added_date = createDate, cylinder_tare_weight = tareWeight, refrigerant_id = refrigerant_type_id_from_db, current_refrigerant_weight = currentRefrigerantweight, supplier = name, cylinder_size = cylinderSize, cylinder_type_id = 1 )
        
        #2. Generate unique url for the unit
        my_equipment_id = my_unit.unit_id
        unique_url = UUID_Generate.EquipmentQRGenerator.generate_equipment_unique_id(my_equipment_id)
        
        #3. Add unique url to database
        CRUD.update(Unit, 'unique_url_id', new = unique_url, unit_id = my_equipment_id)
        tech_id = session.get('tech_id')
        
        #4. Success page
        return render_template('equipment/equipment-linked.html', unique_url = unique_url, tech_id = tech_id)
    
    elif request.method == 'GET':
        current_tech_id = session.get('tech_id')
        print(current_tech_id)
        
        print("inside get")
        return render_template('equipment/equipment_create.html', tech_id = current_tech_id)

@technician.route('/equipment-tag-linked')
def successful_add():
    print("inside successful_add")
    return render_template('equipment/equipment-linked.html')



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
    
    
@technician.route('/equipment-info/<unique_id>', methods = ['GET', 'POST'])
def equipment_info_page(unique_id):
    if request.method == 'GET':
        #1. Get data from database
        print("inside get for /equipment-info")        
        
        #2 get unique_id from url
        unit_unique_url = unique_id
        
        #3. Get row in database for specific equipment/unit.
        data = CRUD.read(Unit, all = False, unique_url_id = unit_unique_url)
                
        print(data.manufacturer)
        
        tech_id = session.get('tech_id')
        #3. Render html
        return render_template('beta/equipment_info.html', data=data, tech_id = tech_id)
        
        # #Get foreign keys to search other tables.
        # cylinder_refrigerant_id = data.refrigerant_id
        # current_cylinder_type_id = data.cylinder_type_id
        
        # #Get name of refrigerant and the type of cylinder.
        # refrigerant_table_lookup = CRUD.read(Refrigerant, all = False, refrigerant_id = cylinder_refrigerant_id)
        # cylinder_type_lookup = CRUD.read(Cylinder_Type, all = False, cylinder_type_id = current_cylinder_type_id)    
        
        # name_data = {
        #     "refrigerant_name": refrigerant_table_lookup.refrigerant_name,
        #     "cylinder_type": cylinder_type_lookup.type_name
        # }
        
        # return render_template("beta/cylinder_info.html", data=data, name = name_data)
        
        #2. Pass data to html
    else:
        print('error')
        return render_template('equipment-info.html')


        