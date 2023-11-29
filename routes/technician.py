from flask import make_response, session, Blueprint
from flask import session
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician, Unit, Cylinder, Tag,Technician_Offer,Contractor
from functools import wraps
import UUID_Generate
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
technician = Blueprint('technician', __name__)

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

@technician.route("/dashboardtechnician")
@login_required
@technician_required
def dashboardtechnician():
    # Render the dashboard
    print("Rendering dashboard")
    user_current=session.get('user_id')
    user_first_name=CRUD.read(User_Detail,user_id=user_current).first_name
    return render_template("technician/dashboardtechnician.html", user=user_current,user_first_name = user_first_name)

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
    else:
        return render_template("technician/formtechnician.html")
    
<<<<<<< HEAD
@technician.route("/dashboardtechnician")
@login_required
@technician_required
def dashboardtechnician_two():
    # Render the dashboard
    print("Rendering dashboard")
    user_current=session.get('user_id')
    return render_template("technician/dashboardtechnician.html", user=user_current)
=======








>>>>>>> ab9f62c934d4fb93c7779f04d0ed85276d55b4c0

    
@technician.route('/equipment/equipment_create', methods = ['GET', 'POST'])
def equipment_create():
    print("inside equipment_create")
    if request.method == 'POST':
        print("inside post")
        
        #Get data from form
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
        
        #Sometimes these fields are empty
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
        #0.Get Technician ID from session.
        tech_id = session.get('tech_id')
        #1.Add new unit to the database        
        my_unit=CRUD.create(Unit, type_of_refrigerant = refrigerantType, installation_date = createDate, manufacturer = manufacturerName, unit_type = equipmentType, factory_charge_amount = factoryCharge, serial_number = serialNumber, technician_id = tech_id)    
        my_equipment_id = my_unit.unit_id
        #2.Get the Unique URL for the unit from the QR code.
        unique_equipment_token = session.get('QR_unique_token')
        #3.Add the tag to the database "Tag" table.
        CRUD.create(Tag, tag_url = unique_equipment_token, unit_id = my_equipment_id, type = "equipment")
        #5.Render Success page
        return render_template('equipment/equipment-linked.html', unique_url = unique_equipment_token, tech_id = tech_id)
    
    elif request.method == 'GET':
        current_tech_id = session.get('tech_id')
        return render_template('equipment/equipment_create.html', tech_id = current_tech_id)

@technician.route('/equipment-tag-linked')
def successful_add():
    print("inside successful_add")
    return render_template('equipment/equipment-linked.html')
   
@technician.route('/choose-qr-type', methods = ['GET'])
def my_choose_qr_type():
    print("inside choose-qr-type")
    #Check if qr is already in the system:
    unique_token = request.args.get('unique_token') #get token from url
    x = None
    print("unique_token IN QR TYPE: ", unique_token)   
    if unique_token != None: #always will have this after a qr scan.
        x = CRUD.read(Tag, all = False, tag_url = unique_token)
        if x != None: #qr is registered in the system
            if x.type == "equipment":
                print("this is an equipment qr tag")
                url = 'equipment-info/' + str(unique_token)
                return redirect(url)
            elif x.type == "cylinder":
                url = 'cylinder_info/' + str(unique_token)
                return redirect(url)
        else: #go to register a new tag page
            print("error in qr scan, this qr tag needs to be registered.")
            session['QR_unique_token'] = unique_token
            return render_template('Equipment Common/choose-qr-type.html')    
        

@technician.route('/New Cylinder/tag-linked')
def add_qr():
    return render_template('New Cylinder/tag-linked.html')

@technician.route('/remove-qrtag')
def remove_qr():
    return render_template('Equipment Common/qr-remove.html')

@technician.route('/charge-equipment')
def charge():
    return render_template('equipment/charge-equipment.html')

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


##################################################
#View History/Logs of Equipment/Cylinder Routes###
##################################################
#Make a selection between unit and cylinder
@technician.route('/choose-equipment-history-type', methods = ['GET', 'POST'])
def choose_equipment_type():
        if request.method == 'GET':
            return render_template('technician/select-history-type.html')
        else:
            print('error')
            return render_template('technician/select-history-type.html')

#selected UNIT history
@technician.route('/select-history-type-technician-maintenance', methods = ['GET', 'POST'])
def select_history_type_tech():
    
    if request.method == 'GET':
        return render_template('equipment/maintenance_history.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')

#selected CYLINDER history
@technician.route('/select-history-type-technician-cylinder', methods = ['GET', 'POST'])
def select_history_type_tech_cylinder():
    if request.method == 'GET':
        return render_template('equipment/ODS-history.html')
    else:
        print('error')
        return render_template('equipment/ODS-history.html')
##################################################
##################################################
    
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

        tech_obj = CRUD.read(
            Technician_Offer,
            token = token
        )

        technician_id = tech_obj.technician_id

        CRUD.update(
            Technician,
            technician_id=technician_id,
            attr="date_begin",
            new=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        CRUD.update(Technician,
                    technician_id = technician_id,
                    attr = "user_status",
                    new = "Active")
        CRUD.update(Technician,
                    technician_id = technician_id,
                    attr = "contractor_status",
                    new = "Engaged")
        contractor = CRUD.read(
            Contractor,
            contractor_id = contractor_id,
        )

        contractor_user_detail_obj = CRUD.read(
            User_Detail,
            user_id = contractor.user_id
        )

        contractor_user_obj = CRUD.read(
            User,
            user_id = contractor.user_id
        )

        contractor_name = contractor_user_detail_obj.first_name
        contractor_email = contractor_user_obj.email

        technician_obj = CRUD.read(
            Technician,
            technician_id = technician_id,
        )
        print(f"technicain_id:{technician_id}")

        technician_user_detail_obj = CRUD.read(
            User_Detail,
            user_id = technician_obj.user_id
        )

        technician_name = technician_user_detail_obj.first_name
        
        try:
            msg = MIMEMultipart()
            msg['From'] = 'refit_dev@sidneyshapiro.com'
            msg['To'] = 'refit_dev@sidneyshapiro.com'
            msg['Subject'] = "Technician Added Sucessfully"
            body = f"Hello {contractor_name} technician {technician_name} has accepted your offer."
            msg.attach(MIMEText(body, 'plain'))
            
            user_obj = CRUD.read(User,email = contractor_email, all = False)
            print(f"user_id:")
            print(user_obj)
            print(f"user_id:{user_obj.user_id}")
            technician_obj = CRUD.read(Technician, user_id = user_obj.user_id, all=False)

            email_text = msg.as_string()
            print(f"Message is {email_text}")
            #Send an email to the email address typed in the form.
            smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)  # Using SMTP_SSL for secure connection
            smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')  # Log in to the server
            smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
            smtpObj.quit()  # Quitting the connection
            print("Email sent successfully!")
        except Exception as e:
            print("Oops, something went wrong: ", e)
    return render_template('Login Flow/login.html')

   
           
@technician.route('/equipment-info/<unique_id>', methods = ['GET', 'POST'])
def equipment_info_page(unique_id):
    if request.method == 'GET':
        #1. Get data from database
        print("inside get for /equipment-info")        
        
        #2 get unique_id from url
        unit_unique_url = unique_id
        
        #3. Get row in database for specific equipment/unit.
        tag_data = CRUD.read(Tag, all = False, tag_url = str(unique_id))
        x = tag_data.unit_id
        print("x: ", x)
        data = CRUD.read(Unit, all = False, unit_id = x)
                        
        tech_id = session.get('tech_id')
        #3. Render html
        return render_template('beta/equipment_info.html', data=data, tech_id = tech_id)

    else:
        print('error')
        return render_template('equipment-info.html')
    
@technician.route('/buy-qr', methods = ['GET', 'POST'])
def buy_qr_page():
    if request.method == 'GET':
        return render_template('Equipment Common/placeholder-buy-qr-tag.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')

##@technician.route('/equipment/repair')
##def repair():
 ##   return render_template('equipment/repair.html')
##@technician.route('/equipment/recovery')
##def recovery():
   ## return render_template('equipment/recovery.html')

    