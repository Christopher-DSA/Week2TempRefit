# Import necessary modules from flask
from flask import make_response, session, Blueprint
from flask import session,send_from_directory,send_file
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician, Unit, Cylinder, Tag, Technician_Offer,Contractor, Cylinder_History, Equipment_History, RepairFormUnitView,ODP,DetailedEquipmentScanView,Repair_form
from functools import wraps
import pint
from datetime import datetime



# Import other necessary modules
import UUID_Generate
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import send_from_directory ,send_file

# Define a blueprint for 'technician'
technician = Blueprint('technician', __name__)

#from pint import UnitRegistry



# Define a decorator for routes that require a user to be logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if 'user_id' is in session
        if 'user_id' not in session:
            # If not, redirect to login page
            return render_template('auth/login.html')
        # If 'user_id' is in session, proceed to the requested route
        return f(*args, **kwargs)
    return decorated_function

# Define a decorator for routes that require a user to be a technician
def technician_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the current user's id from the session
        current_user_id = session.get('user_id')

        # Fetch the current user's details from the database
        current_user = CRUD.read(User,user_id=current_user_id)
        
        # Check if the current user exists and if their role is 'technician'
        if not current_user or current_user.role != 'technician':
            # If not, return an 'Unauthorized' response
            return "Unauthorized", 403

        # If the user exists and their role is 'technician', proceed to the requested route
        return f(*args, **kwargs)
    return decorated_function

# Renders the technician dashboard
@technician.route("/dashboardtechnician")
@login_required
@technician_required
def dashboardtechnician():
    current_user_id = session.get('user_id')
    user_detail = CRUD.read(User_Detail, user_id=current_user_id)

    # Check if user detail exists
    if not user_detail:
        return "User detail not found", 404

    user_first_name = user_detail.first_name
    return render_template("technician/new-dashboard.html", user=current_user_id, user_first_name=user_first_name)

@technician.route("/formtechnician", methods=["GET", "POST"])
def formtechnician():
    if request.method == 'POST':
        # Get data from form
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        company_name = request.form.get('companyName')
        ods_license_number = request.form.get('odsLicenseNumber')
        address_line = request.form.get('addressLine')
        province = request.form.get('province')
        city = request.form.get('city')
        postal_code = request.form.get('postalCode')
        phone_number = request.form.get('phoneNumber')

        # Validate the data and pass data to database
        try:
            new_detail = CRUD.create(User_Detail, user_id=session.get('user_id'), first_name=first_name, last_name=last_name, address=address_line, province=province, city=city, postal_code=postal_code, telephone=phone_number)
            new_technician_detail = CRUD.create(Technician, ODS_licence_number=ods_license_number, user_id=session.get('user_id'))
        except Exception as e:
            # Log the error and return an error response
            print(f"Error creating user detail or technician detail: {e}")
            return "Error processing form", 500

        return redirect(url_for('technician.dashboardtechnician'))
    else:
        return render_template("technician/formtechnician.html")
    

@technician.route("/dashboardtechnician")
@login_required
@technician_required
def dashboardtechnician_two():
    # Render the dashboard
    print("Rendering dashboard")
    user_current=session.get('user_id')
    return render_template("technician/dashboardtechnician.html", user=user_current)


#Register new equipment QR tag
@technician.route('/equipment/equipment_create', methods = ['GET', 'POST'])
def equipment_create_QR():
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

#REPAIR MAINTENANCE LOG FOR EQUIPMENT.
@technician.route('/equipment/repair_ODS_Sheet', methods = ['GET', 'POST'])
def repair_ODS_Sheet_New():
    if request.method == 'GET':
        #Get data about unit to pass on to placeholder fields on the next page.
        current_scan_date = today_date = datetime.now().strftime("%Y-%m-%d")
        # Get today's date and format it to "yyyy-mm-dd"

        print("Today's date is:", current_scan_date)
        current_tag_url = session.get('unique_equipment_token')
        tag_data = CRUD.read(Tag, all = False, tag_url = str(current_tag_url))
        x = tag_data.unit_id
        print("x: ", x)
        data = CRUD.read(Unit, all = False, unit_id = x)
        my_dict = {
            'type_of_refrigerant' : data.type_of_refrigerant,
            'factory_charge_amount' : data.factory_charge_amount
        }
        if (float(my_dict['factory_charge_amount']) % 16 == 0):
            my_dict['factory_charge_lbs'] = float(my_dict['factory_charge_amount']) / 16
            my_dict['factory_charge_oz'] = 0
        else:
            remainder = float(my_dict['factory_charge_amount']) % 16
            my_dict['factory_charge_lbs'] = (float(my_dict['factory_charge_amount']) - remainder) / 16
            my_dict['factory_charge_oz'] = remainder
        print("my_dict: ", my_dict)
        return render_template('equipment/repair_ODS_Sheet.html', data = my_dict, date=str(current_scan_date))
    elif request.method == 'POST': #This is the rpair form post.
        ods_form_names = ['current_date','refrigerant_type_send','leakDetectedRadio','repairStatusRadio','noLongerContainsRefrigerant','vacuumTest','compressorOil','pressureTest','psigResult','refrigerant_added_lbs','refrigerant_added_oz','refrigerant_removed_lbs','refrigerant_removed_oz','additionalNotes']
        form_data_dictionary = {}
        for x in ods_form_names:
            form_data_dictionary[x] = request.form.get(x)
        
        # Type Conversions
        psig_result = form_data_dictionary.get('psigResult')
        if psig_result is None or psig_result == '':
            psig_result = 0  # or any default value you prefer
        else:
            psig_result = float(psig_result)
        
        #Refrigerant Totals in OZ for database storage
        refrigerant_added_lbs = form_data_dictionary.get('refrigerant_added_lbs')
        refrigerant_added_oz = form_data_dictionary.get('refrigerant_added_oz')
        refrigerant_removed_lbs = form_data_dictionary.get('refrigerant_removed_lbs')
        refrigerant_removed_oz = form_data_dictionary.get('refrigerant_removed_oz')
        
        # Convert pounds to ounces (1 lb = 16 oz) and add to existing ounces
        total_refrigerant_added_oz = (float(refrigerant_added_lbs) * 16) + float(refrigerant_added_oz)
        total_refrigerant_removed_oz = (float(refrigerant_removed_lbs) * 16) + float(refrigerant_removed_oz)
    
        # Convert 'on' and '' to True, False, and None for other radio boxes
        def convert_radio_to_boolean(form_value):
            if form_value == 'on':
                return True
            elif form_value == '':
                return None
            else:
                return False
        form_data_dictionary['leakDetectedRadio'] = convert_radio_to_boolean(form_data_dictionary.get('leakDetectedRadio'))
        form_data_dictionary['repairStatusRadio'] = convert_radio_to_boolean(form_data_dictionary.get('repairStatusRadio'))
        
        def convert_check_to_boolean(form_value):
            if form_value == '':
                return True
            else:
                return False
        form_data_dictionary['vacuumTest'] = convert_check_to_boolean(form_data_dictionary.get('vacuumTest'))
        form_data_dictionary['compressorOil'] = convert_check_to_boolean(form_data_dictionary.get('compressorOil'))
        form_data_dictionary['pressureTest'] = convert_check_to_boolean(form_data_dictionary.get('pressureTest'))
            
        # Mapping form data to model attributes
        model_data = {
            'repair_date': form_data_dictionary.get('current_date'),  # Assuming it's in the correct date format
            'refrigerant_type': form_data_dictionary.get('refrigerant_type_send'),
            'leak_test_result': form_data_dictionary.get('leakDetectedRadio'),  # Assuming 'true' or 'false' strings
            'is_leak_repaired': form_data_dictionary.get('repairStatusRadio'),  # Similar assumption
            'no_longer_contains_refrigerant': form_data_dictionary.get('noLongerContainsRefrigerant'),
            'vacuum_test_performed': form_data_dictionary.get('vacuumTest'),
            'compressor_oil_removed': form_data_dictionary.get('compressorOil'),
            'pressure_test_performed': form_data_dictionary.get('pressureTest'),
            'additional_notes': form_data_dictionary.get('additionalNotes'),
            'PSIG_result': psig_result,
            'refrigerant_added_total_oz': total_refrigerant_added_oz,
            'refrigerant_removed_total_oz': total_refrigerant_removed_oz,
            'tech_id': session.get('tech_id')
        }
        
        CRUD.create(Repair_form, **model_data)
        print("model_data: ", model_data)
        return model_data

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
def choose_equipment_history_type():
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
    response = None

    if request.method == 'POST':
        contractor_id = request.form['dt']
        response = request.form['action']
        token = request.form['tk']
        print("Contractor ID: ", contractor_id)
        print("Token: ", token)
        
        if response == 'Accept':
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
                Contractor,
                contractor_id = contractor_id
            )

            contractor_user_obj = CRUD.read(
                User,
                user_id = contractor.user_id
            )

            contractor_name = contractor_user_detail_obj.name
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
            print("begin)")
            print("offer status: ", tech_obj.offer_status)
            send_contractor_email(contractor_name, technician_name, contractor_email, 'Engaged')
            print("end")

        elif response == 'Decline':

            tech_obj = CRUD.read(
            Technician_Offer,
            token=token
        )

            technician_id = tech_obj.technician_id

            CRUD.update(Technician,
                        technician_id=technician_id,
                        attr="user_status",
                        new="Inactive")
            CRUD.update(
                Technician_Offer,
                "offer_status",
                new = "Rejected", 
                token = token
            )
            CRUD.update(Technician,
                        technician_id=technician_id,
                        attr="date_end",
                        new=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            CRUD.update(Technician,
                        technician_id=technician_id,
                        attr="contractor_status",
                        new="Rejected")

            contractor = CRUD.read(
                Contractor,
                contractor_id=contractor_id,
            )

            contractor_user_detail_obj = CRUD.read(
                Contractor,
                contractor_id = contractor_id
            )

            contractor_user_obj = CRUD.read(
                User,
                user_id=contractor.user_id
            )

            contractor_name = contractor_user_detail_obj.name
            contractor_email = contractor_user_obj.email

            technician_obj = CRUD.read(
                Technician,
                technician_id=technician_id,
            )
            print(f"technician_id:{technician_id}")

            technician_user_detail_obj = CRUD.read(
                User_Detail,
                user_id=technician_obj.user_id
            )

            technician_name = technician_user_detail_obj.first_name
            print("offer status: ", tech_obj.offer_status)
        
            send_contractor_email(contractor_name, technician_name, contractor_email, "Rejected")

            return render_template('Login Flow/login.html')
    return render_template('Login Flow/login.html')


def send_contractor_email(contractor_name, technician_name, contractor_email, offer_status):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'refit_dev@sidneyshapiro.com'
        msg['To'] = 'refit_dev@sidneyshapiro.com'
        

        if offer_status == "Engaged":
            msg['Subject'] = "Technician Added Successfully"
            body = f"Hello {contractor_name} technician {technician_name} has accepted your offer."
        elif offer_status == "Rejected":
            msg['Subject'] = f"Technician has rejected your offer."
            body = f"Hello {contractor_name} technician {technician_name} has rejected your offer."

        msg.attach(MIMEText(body, 'plain'))

        user_obj = CRUD.read(User, email=contractor_email, all=False)
        technician_obj = CRUD.read(Technician, user_id=user_obj.user_id, all=False)

        email_text = msg.as_string()

        smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)
        smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')
        smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
        smtpObj.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("Oops, something went wrong: ", e)

           
@technician.route('/equipment-info/<unique_id>', methods = ['GET', 'POST'])
def equipment_info_page(unique_id):
    if request.method == 'GET':
        #1. Get data from database
        print("inside get for /equipment-info")        
        
        #2 get unique_id from url
        unit_unique_url = unique_id
        tech_id = session.get('tech_id')

        #3. Get row in database for specific equipment/unit.
        tag_data = CRUD.read(Tag, all = False, tag_url = str(unique_id))
        unit_id = tag_data.unit_id
        data = CRUD.read(Unit, all = False, unit_id = unit_id)

        session['new_unit_id'] = unit_id
        session['tag']=unique_id
        session['tech_id'] = tech_id

        #Add scan log to database.
        current_scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        CRUD.create(Equipment_History, date_qr_scanned_eq=current_scan_date, tech_id=tech_id, unit_id = unit_id)        
        
        #remove previous, if any, unique_equipment_token from session.
        session.pop('unique_equipment_token', None)
        #save tag url to session.
        session['unique_equipment_token'] = str(unique_id)
                
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


@technician.route('/charge-equipment', methods=['GET', 'POST'])
def charge_equipment_view():
    if request.method == 'GET':
        print("Inside Get for charge_equipment")
        # Get the unique equipment token from the session
        unique_token = session.get('unique_equipment_token')
        
        
        unit_id = session.get('new_unit_id')        
        print("Unit ID: ", unit_id)

        # Fetch data from the Unit table based on the unit_id
        unit_data = CRUD.read(Unit, all=False, unit_id=unit_id)

        tech_id = session.get('tech_id')
        type_of_refrigerant = unit_data.type_of_refrigerant 
        factory_charge_amount = unit_data.factory_charge_amount

        print("Test Test: ", type_of_refrigerant)
        print("Test Test: ", factory_charge_amount)
        # Render the HTML template with the retrieved data


      #### converting to pounds and ounces

        ureg = pint.UnitRegistry()
        factory_charge_amount = 1000
        ounces = factory_charge_amount* ureg.ounces
        pounds = ounces.to(ureg.pounds)

        print (pounds)
        print (ounces)


        return render_template('equipment/charge-equipment.html', type_of_refrigerant=type_of_refrigerant,  factory_charge_amount= factory_charge_amount, pounds = pounds , ounces = ounces, tech_id=tech_id)
    elif request.method == "POST":
        print("Inside Post for charge_equipment")
        

@technician.route('/RefrigerantTypeLookupData.csv')
def serve_csv():
     return send_file('RefrigerantTypeLookupData.csv', mimetype='text/csv', as_attachment=True, download_name='RefrigerantTypeLookupData.csv')
    

#ODP Tag Form on Equipment Scan
@technician.route('/ODP-Tag', methods=['GET', 'POST'])
def ODP_Show():
    if request.method == 'GET':
        return render_template('equipment/ODP_Tag.html')
    

@technician.route("/equipment_logs", methods=["GET", "POST"])
def equipment_hist():
    if request.method == "GET":
        print("inside get for /equipment_history")
        current_tech_id = session.get('tech_id')
        # equipment_hist = CRUD.read(Equipment_History, all=True, tech_id=current_tech_id)
        x = CRUD.read(DetailedEquipmentScanView, all=True, tech_id=current_tech_id)

        for equipment in x:
            print(equipment.tech_id)
            print(equipment.manufacturer)
            print(equipment.unit_type)
            print(equipment.date_qr_scanned_eq)
            

        return render_template("technician/unit_scan_history.html", equipment_list=x)

    return "Invalid request method"

#This is the digitized ods tag. (Singular Tag)
@technician.route("/ods-tags", methods=["GET", "POST"])
def ods_tags_new():
    if request.method == "GET":
        return render_template("beta/digitized_ods_tag.html")
    else:
        selected_repair_form_id = request.form.get('selected_ods_tag')
        print("selected_repair_form_id: ", selected_repair_form_id)
        
        current_tech_id = session.get('tech_id')
        
        #Get data from database
        data = CRUD.read(Repair_form, all=False, repair_form_id=selected_repair_form_id)
        tech_data = CRUD.read(Technician, all=False, technician_id=current_tech_id)
        user_detail_data = CRUD.read(User_Detail, all=False, user_id=tech_data.user_id)
        company_data = CRUD.read(Contractor, all=False, contractor_id=tech_data.contractor_id)
        unit_data = CRUD.read(Unit, all=False, unit_id=data.unit_id)
        
        return render_template("beta/digitized_ods_tag.html", data=data, tech_data=tech_data, user_data=user_detail_data, company_data=company_data, unit_data=unit_data)
        
#This is the table with the list of all ods tags a technician has ever filled out.
@technician.route("/view_all_ods_tags", methods=["GET", "POST"])
def view_all_ods_tags():
    if request.method == "GET":
        tech_id_current = session.get('tech_id')
        data = CRUD.read(RepairFormUnitView, all=True, tech_id=tech_id_current)
        
        return render_template("beta/view_all_ods_tags.html", data=data)
    else:
        return "Invalid request method (you posted to this route)"

