# Import necessary modules from flask
from flask import make_response, session, Blueprint, jsonify
from flask import session, send_from_directory, send_file
from flask import Flask, render_template, redirect, current_app, url_for, flash, make_response, request
from models import CRUD, User, User_Detail, Technician, Unit, Cylinder, Tag, Technician_Offer, Contractor, Cylinder_History, Equipment_History, RepairFormUnitView, ODP, DetailedEquipmentScanView, Repair_form, Activity_Logs
from functools import wraps
import pint
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import re


# Import other necessary modules
import UUID_Generate
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import send_from_directory, send_file

# Define a blueprint for 'technician'
technician = Blueprint('technician', __name__)

# from pint import UnitRegistry


def convert_weights_for_display(amount_oz): #Used in repair-ods-form, async cylinder transaction route, digitized ods tag and sending contractor email routes in this module.
    # Converting ounces to pounds and ounces
    amount_lbs = int(amount_oz // 16)
    remaining_ounces = round(amount_oz % 16)

    # Converting ounces to kilograms and grams
    # 1 ounce is approximately 0.0283495 kilograms
    amount_kg = amount_oz * 0.0283495
    # Extracting the whole kilograms
    whole_kg = int(amount_kg)
    # Converting the fractional part of the kilograms into grams and rounding it
    remaining_g = round((amount_kg - whole_kg) * 1000)

    # Formatting for display
    display_lbs_oz = f"{amount_lbs}lbs {remaining_ounces}oz"
    display_kg_g = f"{whole_kg}kg {remaining_g}g"

    return display_lbs_oz, display_kg_g



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
        current_user = CRUD.read(User, user_id=current_user_id)

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
            new_detail = CRUD.create(User_Detail, user_id=session.get('user_id'), first_name=first_name, last_name=last_name,
                                     address=address_line, province=province, city=city, postal_code=postal_code, telephone=phone_number)
            new_technician_detail = CRUD.create(
                Technician, ODS_licence_number=ods_license_number, user_id=session.get('user_id'))
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
    user_current = session.get('user_id')
    return render_template("technician/dashboardtechnician.html", user=user_current)


# Register new equipment QR tag equipment create
@technician.route('/equipment/equipment_create', methods=['GET', 'POST'])
def equipment_create_QR():
    print("inside equipment_create")
    if request.method == 'POST':
        print("inside post for equipment_create")

        # Get data from form
        # Tab 1
        createDate = request.form.get('createDate')  # 1 YES
        equipmentType = request.form.get('equipmentType')  # 2 YES
        equipmentUnitNumber = request.form.get('equipmentUnitNumber')  # 3 YES
        manufacturerName = request.form.get('manufacturerName')  # 4 YES
        modelNumber = request.form.get('modelNumber')  # 5 YES
        serialNumber = request.form.get('serialNumber')  # 6 YES
        equipmentUnitAddress = request.form.get(
            'equipmentUnitAddress')  # 7 YES
        organizationName = request.form.get('organizationName')  # 8 YES
        equipmentLocation = request.form.get('equipmentLocation')  # 9 YES

        # Tab 2
        refrigerantType = request.form.get('refrigerantType')
        currentRefrigerantWeight_1 = request.form.get(
            'currentRefrigerantWeight1')  # bigger unit
        currentRefrigerantWeight_2 = request.form.get(
            'currentRefrigerantWeight2')  # smaller unit
        currentRefrigerantWeightUnit = request.form.get(
            'currentRefrigerantWeightUnit')
        
        additionalRefrigerantWeight_1 = request.form.get(
            'additionalRefrigerantWeight1')  # bigger unit for additional charge
        additionalRefrigerantWeight_2 = request.form.get(
            'additionalRefrigerantWeight2') # smaller unit for additional charge
        additionalRefrigerantWeightUnit = request.form.get(
            'additionalRefrigerantWeightUnit') # unit type for additional charge
        
        
        additionalNotes = request.form.get('additionalNotes')  # 10 YES
        customLabel = request.form.get('customLabel')  # 11 YES

        # STILL NEED TO ADD
        # unitLabel/unit_name

        # For database
        amount_of_refrigerant_kg = 0
        amount_of_refrigerant_lbs = 0
        amount_of_refrigerant_in_unit_oz = 0
        
        
        #Factory Charge
        if currentRefrigerantWeight_1 == "" or currentRefrigerantWeight_1 == None:
            currentRefrigerantWeight_1 = 0
        if currentRefrigerantWeight_2 == "" or currentRefrigerantWeight_2 == None:
            currentRefrigerantWeight_2 = 0

        #Additional Charge
        if additionalRefrigerantWeight_1 == "" or additionalRefrigerantWeight_1 == None:
            additionalRefrigerantWeight_1 = 0
        if additionalRefrigerantWeight_2 == "" or additionalRefrigerantWeight_2 == None:
            additionalRefrigerantWeight_2 = 0


        # Metric or Imperial
        if currentRefrigerantWeightUnit == 'metric':
            print("Using Metric KG/G")
            amount_of_refrigerant_kg = float(
                currentRefrigerantWeight_1) + (float(currentRefrigerantWeight_2) * 0.001)
            amount_of_refrigerant_lbs = float(
                amount_of_refrigerant_kg) * 2.20462
            # rounding
            amount_of_refrigerant_lbs = round(amount_of_refrigerant_lbs, 2)
            amount_of_refrigerant_kg = round(amount_of_refrigerant_kg, 2)
            amount_of_refrigerant_in_unit_oz = float(currentRefrigerantWeight_1) * 35.274 + float(
                currentRefrigerantWeight_2) * 0.035274
        else:
            print("Using Imperial LBS/OZ")
            amount_of_refrigerant_lbs = float(
                currentRefrigerantWeight_1) + (float(currentRefrigerantWeight_2) * 0.0625)
            amount_of_refrigerant_kg = amount_of_refrigerant_lbs * 0.453592
            # rounding
            amount_of_refrigerant_kg = round(amount_of_refrigerant_kg, 2)
            amount_of_refrigerant_lbs = round(amount_of_refrigerant_lbs, 2)
            amount_of_refrigerant_in_unit_oz = float(currentRefrigerantWeight_1) * 16 + float(currentRefrigerantWeight_2)
        
        
        additional_amount_of_refrigerant_in_unit_oz = 0
        
        # Metric or Imperial for additional charge
        if additionalRefrigerantWeightUnit == 'metric':
            additional_amount_of_refrigerant_in_unit_oz = float(additionalRefrigerantWeight_1) * 35.274 + float(
                additionalRefrigerantWeight_2) * 0.035274
        else: #Imperial
            additional_amount_of_refrigerant_in_unit_oz = float(additionalRefrigerantWeight_1) * 16 + float(additionalRefrigerantWeight_2)

        # Serial Number is Optional
        if serialNumber == "":
            serialNumber = "N/A"

        # Making sure strings do not have special characters
        manufacturerName = re.sub('[^A-Za-z0-9 &]+', '', manufacturerName)
        equipmentType = re.sub('[^A-Za-z0-9 ]+', '', equipmentType)
        refrigerantType = re.sub('[^A-Za-z0-9 ]+', '', refrigerantType)
        serialNumber = re.sub('[^A-Za-z0-9 ]+', '', serialNumber)
        
        #amount_of_refrigerant_in_unit_oz is the factory charge <-
        #additional_amount_of_refrigerant_in_unit_oz is the additional charge <-
        #total_amount_refrigerant is the factory charge + additional charge <-
        
        total_amount_refrigerant = amount_of_refrigerant_in_unit_oz + additional_amount_of_refrigerant_in_unit_oz

        ###################################################
        ########### Add new unit to the database############
        ###################################################
        # 0.Get Technician ID from session.
        tech_id = session.get('tech_id')
        current_user_id = session.get('user_id')
        # 1.Add new unit to the database
        unit_data = {
            "type_of_refrigerant": refrigerantType,
            "installation_date": createDate,
            "manufacturer": manufacturerName,
            "unit_type": equipmentType,
            "serial_number": serialNumber,
            "technician_id": tech_id,
            "amount_of_refrigerant_kg": amount_of_refrigerant_kg,
            "amount_of_refrigerant_lbs": amount_of_refrigerant_lbs,
            "model_number": modelNumber,  # This is your database column 'model'
            "equipment_unit_address": equipmentUnitAddress,
            "organization_name": organizationName,
            "equipment_location": equipmentLocation,
            "equipment_unit_number": equipmentUnitNumber,
            "additional_notes": additionalNotes,
            "unit_name": customLabel,
            "amount_of_refrigerant_in_unit_oz": amount_of_refrigerant_in_unit_oz, #Factory Charge
            "user_id": current_user_id,
            "total_amount_refrigerant": total_amount_refrigerant, #Factory Charge + Additional Charge
            "additional_charge": additional_amount_of_refrigerant_in_unit_oz #Additional Charge
        } 

        my_unit = CRUD.create(model=Unit, **unit_data)
        my_equipment_id = my_unit.unit_id
        # 2.Get the Unique URL for the unit from the QR code.
        unique_equipment_token = session.get('QR_unique_token')
        # 3.Add the tag to the database "Tag" table.
        CRUD.create(Tag, tag_url=unique_equipment_token,
                    unit_id=my_equipment_id, type="equipment", user_id=current_user_id, technician_id=tech_id)
        # 4. Record the activity in the Activity_Logs table.
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_user_role = session.get('user_role')
        # This will either be the contractor the user works for or the id of the contractor that is logged in depending on the user role.
        current_contractor_id = session.get('contractor_id')
        current_user_id = session.get('user_id')

        current_user_first_name = session.get('user_first_name')
        current_user_last_name = session.get('user_last_name')
        combined_name = current_user_first_name + " " + current_user_last_name

        if current_user_role == 'technician':
            CRUD.create(Activity_Logs, technician_id=tech_id, activity_type='NEW-EQUIPMENT-REGISTERED', date_logged=current_date,
                        user_role=current_user_role, contractor_id=current_contractor_id, user_id=current_user_id, name=combined_name)
        elif current_user_role == 'contractor':
            CRUD.create(Activity_Logs, activity_type='NEW-EQUIPMENT-REGISTERED', date_logged=current_date,
                        user_role=current_user_role, contractor_id=current_contractor_id, user_id=current_user_id, name=combined_name)

        # 5.Render Success page
        return render_template('equipment/equipment-linked.html', unique_url=unique_equipment_token, tech_id=tech_id)

    elif request.method == 'GET':
        current_tech_id = session.get('tech_id')
        return render_template('equipment/equipment_create.html', tech_id=current_tech_id)


@technician.route('/equipment-tag-linked')
def successful_add():
    print("inside successful_add")
    return render_template('equipment/equipment-linked.html')


@technician.route('/choose-qr-type', methods=['POST'])
def my_choose_qr_type():
    if request.method == 'POST':
        print("inside choose-qr-type")
        # Check if qr is already in the system:
        # get token from post request
        unique_token = request.form.get('unique_token')
        print("unique_token IN QR TYPE: ", unique_token)
        if unique_token:  # always will have this after a qr scan.
            print("going to read tag in database")
            print("unique_token AGAIN: ", unique_token)
            token_without_uuid = unique_token.split('-')[0]
            x = CRUD.read(Tag, all=False, tag_url=str(token_without_uuid))

            if x != None:  # qr is registered in the system
                if x.type == "equipment":
                    print("this is an equipment qr tag")
                    url = 'equipment-info/' + str(token_without_uuid)
                    return redirect(url)
                elif x.type == "cylinder":
                    url = 'cylinder_info/' + str(token_without_uuid)
                    return redirect(url)
            else:  # go to register a new tag page
                uuid4_pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
                if "UNT" in unique_token and uuid4_pattern.search(unique_token):
                    print("Unregistered equipment tag scanned")
                    session['QR_unique_token'] = token_without_uuid
                    return redirect('/equipment/equipment_create')
                elif "CYL" in unique_token and uuid4_pattern.search(unique_token):
                    print("Unregistered cylinder tag scanned")
                        # Split the unique_token at the hyphen and take the first part
                    token_without_uuid = unique_token.split('-')[0]
                    session['QR_unique_token'] = token_without_uuid
                    return redirect('/new_cylinder')
                elif "TST" in unique_token and uuid4_pattern.search(unique_token):
                    print("Unregistered test tag scanned")
                    token_without_uuid = unique_token.split('-')[0]
                    session['QR_unique_token'] = token_without_uuid
                    return render_template('Equipment Common/choose-qr-type.html')
                else:  # Not a REFit QR Tag
                    print("Not a REFit QR Tag")
                    return render_template('Equipment Common/qr-scan.html')

# Need this one


@technician.route('/for-ods-form-choose-qr-type', methods=['POST'])
def ods_form_qr_type_old():
    # Get the JSON data sent from the client
    data = request.get_json()

    print(data)
    unique_token = data.get('unique_token')

    bigUnitAdded = data.get('bigUnitAdded')
    smallUnitAdded = data.get('smallUnitAdded')
    bigUnitRemoved = data.get('bigUnitRemoved')
    smallUnitRemoved = data.get('smallUnitRemoved')

    AddedMetricOrImperial = data.get('AddedMetricOrImperial')
    RemovedMetricOrImperial = data.get('RemovedMetricOrImperial')

    print("bigUnitAdded: ", bigUnitAdded)
    print("smallUnitAdded: ", smallUnitAdded)
    print("bigUnitRemoved: ", bigUnitRemoved)
    print("smallUnitRemoved: ", smallUnitRemoved)
    print("AddedMetricOrImperial: ", AddedMetricOrImperial)
    print("RemovedMetricOrImperial: ", RemovedMetricOrImperial)

    total_refrigerant_added_oz = 0
    total_refrigerant_removed_oz = 0

    print("unique_token IN QR TYPE: ", unique_token)

    # converting to 0 if ''
    if bigUnitAdded == "" or bigUnitAdded == None:
        bigUnitAdded = float(0)
    if smallUnitAdded == "" or smallUnitAdded == None:
        smallUnitAdded = float(0)
    if bigUnitRemoved == "" or bigUnitRemoved == None:
        bigUnitRemoved = float(0)
    if smallUnitRemoved == "" or smallUnitRemoved == None:
        smallUnitRemoved = float(0)

    if unique_token:
        short_unique_token = unique_token.split('-')[0]
        x = CRUD.read(Tag, all=False, tag_url=short_unique_token)
        if x:
            if x.type == "equipment":
                print("this is an equipment qr tag")
                return jsonify({"error": "Oops, this is an equipment QR tag. Try again with a cylinder QR tag."})
            elif x.type == "cylinder":
                if (float(bigUnitAdded) == 0 and float(smallUnitAdded) == 0 and float(bigUnitRemoved) == 0 and float(smallUnitRemoved) == 0):
                    return jsonify({"error": "Oops, you need to fill out atleast one of the fields."})
                else:
                    print("adding or removing refrigerant from cylinder")
                    # Convert pounds to ounces (1 lb = 16 oz) and add to existing ounces (add try catch here if there are problems)
                    if AddedMetricOrImperial == 'imperial':
                        total_refrigerant_added_oz = (
                            float(bigUnitAdded) * 16) + float(smallUnitAdded)
                    elif AddedMetricOrImperial == 'metric':  # convert kg + g to oz
                        total_refrigerant_added_oz = (
                            float(bigUnitAdded) * 35.274) + (float(smallUnitAdded) * 0.035274)

                    if RemovedMetricOrImperial == 'imperial':
                        total_refrigerant_removed_oz = (
                            float(bigUnitRemoved) * 16) + float(smallUnitRemoved)
                    elif RemovedMetricOrImperial == 'metric':  # convert kg + g to oz
                        total_refrigerant_removed_oz = (
                            float(bigUnitRemoved) * 35.274) + (float(smallUnitRemoved) * 0.035274)

                    # Update Cylinder Refrigerant Amount
                    new_amount_difference = total_refrigerant_added_oz - total_refrigerant_removed_oz
                    print("new_amount_difference: ", new_amount_difference)
                    cylinder_data = CRUD.read(
                        Cylinder, all=False, cylinder_id=x.cylinder_id)
                    calculated_amount = float(CRUD.read(
                        Cylinder, all=False, cylinder_id=x.cylinder_id).current_refrigerant_weight) + (new_amount_difference * -1)
                    CRUD.update(Cylinder, cylinder_id=x.cylinder_id,
                                attr="current_refrigerant_weight", new=calculated_amount)

                    AddedOrRemoved = ""
                    if new_amount_difference > 0:
                        AddedOrRemoved = "Added Refrigerant to Unit"
                    elif new_amount_difference < 0:
                        AddedOrRemoved = "Removed Refrigerant from Unit"

                    refrigerant_type = cylinder_data.refrigerant_type

                    
                    display_lbs_oz, display_kg_g = convert_weights_for_display(float(calculated_amount))

                    return jsonify({"calculated_amount": calculated_amount, "display_lbs_oz": display_lbs_oz, "display_kg_g": display_kg_g, "refrigerant_type": refrigerant_type, "AddedOrRemoved": AddedOrRemoved, "new_amount_difference": new_amount_difference, "short_unique_token": short_unique_token})
        else:
            return jsonify({"error": "This tag needs to be registered before you can add refrigerant to it."})
    else:
        return jsonify({"error": "No unique token provided."})


@technician.route('/for-ods-form-choose-qr-type-oldDoNotUseThisOneItIsOldWay', methods=['POST'])
def ods_form_qr_type():
    # Get the JSON data sent from the client
    data = request.get_json()
    unique_token = data.get('unique_token')
    lbs_added = data.get('refrigerant_lbs_added', 0)
    kg_added = data.get('refrigerant_kg_added', 0)
    lbs_removed = data.get('refrigerant_lbs_removed', 0)
    kg_removed = data.get('refrigerant_kg_removed', 0)

    if lbs_added == "" or lbs_added == None:
        lbs_added = float(0)
    if kg_added == "" or kg_added == None:
        kg_added = float(0)
    if lbs_removed == "" or lbs_removed == None:
        lbs_removed = float(0)
    if kg_removed == "" or kg_removed == None:
        kg_removed = float(0)

    print("kg_added: ", kg_added)
    print("kg_removed: ", kg_removed)
    print("lbs_added: ", lbs_added)
    print("lbs_removed: ", lbs_removed)

    # Conversion factors
    lbs_to_kg = 0.453592
    kg_to_lbs = 2.20462

    # Check for valid token and cylinder
    if unique_token:
        x = CRUD.read(Tag, all=False, tag_url=unique_token)
        if x:
            if x.type == "cylinder":
                cylinder_record = CRUD.read(
                    Cylinder, all=False, cylinder_id=x.cylinder_id)
                # Convert all to a common unit (lbs in this case)
                total_added_lbs = (float(kg_added) *
                                   kg_to_lbs) + float(lbs_added)
                total_removed_lbs = (float(kg_removed) *
                                     kg_to_lbs) + float(lbs_removed)

                # Calculate new total weights of the cylinder not the unit.
                # Removed = refrigerant reclaimed, Added = refrigerant trasnferred to unit.
                new_weight_lbs = float(
                    cylinder_record.current_refrigerant_weight_lbs) - total_added_lbs + total_removed_lbs
                new_weight_kg = new_weight_lbs * lbs_to_kg

                new_weight_kg = round(new_weight_kg, 2)
                new_weight_lbs = round(new_weight_lbs, 2)

                CRUD.update(Cylinder, cylinder_id=x.cylinder_id,
                            attr="current_refrigerant_weight_lbs", new=new_weight_lbs)
                CRUD.update(Cylinder, cylinder_id=x.cylinder_id,
                            attr="current_refrigerant_weight_kg", new=new_weight_kg)

                return jsonify({"success": "Refrigerant updated successfully.", "calculated_amount_lbs": new_weight_lbs, "calculated_amount_kg": new_weight_kg})
            else:
                return jsonify({"error": "This QR code is not for a cylinder."})
        else:
            return jsonify({"error": "Cylinder not found."})
    else:
        return jsonify({"error": "No unique token provided."})


@technician.route('/New Cylinder/tag-linked')
def add_qr():
    return render_template('New Cylinder/tag-linked.html')


@technician.route('/remove-qrtag')
def remove_qr():
    return render_template('Equipment Common/qr-remove.html')

# REPAIR MAINTENANCE LOG FOR EQUIPMENT. Repair Ods

# Need this one


@technician.route('/equipment/repair_ODS_Sheet', methods=['GET', 'POST'])
def repair_ODS_Sheet_New():
    if request.method == 'GET':
        # Get data about unit to pass on to placeholder fields on the next page.
        current_scan_date = today_date = datetime.now().strftime("%Y-%m-%d")
        # Get today's date and format it to "yyyy-mm-dd"

        print("Today's date is:", current_scan_date)
        current_tag_url = session.get('unique_equipment_token')
        tag_data = CRUD.read(Tag, all=False, tag_url=str(current_tag_url))
        x = tag_data.unit_id
        print("x: ", x)
        data = CRUD.read(Unit, all=False, unit_id=x)
        my_dict = {
            'type_of_refrigerant': data.type_of_refrigerant,
        }
        print("my_dict: ", my_dict)
        return render_template('equipment/repair_ODS_Sheet.html', data=my_dict, date=str(current_scan_date))

    elif request.method == 'POST':  # This is the repair form post.
        # # Retrieving values from the 'Added Refrigerant' section
        # refrigerant_weight_unit_added = request.form.get(
        #     'currentRefrigerantWeightUnitAdded')
        # refrigerant_weight1_added = request.form.get(
        #     'currentRefrigerantWeight1Added')
        # refrigerant_weight2_added = request.form.get(
        #     'currentRefrigerantWeight2Added')

        # # Retrieving values from the 'Removed Refrigerant' section
        # refrigerant_weight_unit_removed = request.form.get(
        #     'currentRefrigerantWeightUnitRemoved')
        # refrigerant_weight1_removed = request.form.get(
        #     'currentRefrigerantWeight1Removed')
        # refrigerant_weight2_removed = request.form.get(
        #     'currentRefrigerantWeight2Removed')

        ods_form_names = [
            'current_date',
            'refrigerant_type_send',
            'leakDetectedRadio',
            'repairStatusRadio',
            'noLongerContainsRefrigerant',
            'vacuumTest',
            'compressorOil',
            'pressureTest',
            'psigResult',
            'currentRefrigerantWeightUnitAdded',  # Updated
            'currentRefrigerantWeight1Added',     # Updated
            'currentRefrigerantWeight2Added',     # Updated
            'currentRefrigerantWeightUnitRemoved',  # Updated
            'currentRefrigerantWeight1Removed',   # Updated
            'currentRefrigerantWeight2Removed',   # Updated
            'additionalNotes',
            'TotalOzAdded',  # Reclaim Amount for Form
            'TotalOzRemoved'  # Charge Amount for Form
        ]

        form_data_dictionary = {}
        for x in ods_form_names:
            form_data_dictionary[x] = request.form.get(x)

        # Type Conversions
        psig_result = form_data_dictionary.get('psigResult')
        if psig_result is None or psig_result == '':
            psig_result = 0  # or any default value you prefer
        else:
            psig_result = float(psig_result)

        # Conversion factors
        lbs_to_oz = 16  # 1 lb = 16 oz
        kg_to_g = 1000  # 1 kg = 1000 g
        g_to_oz = 0.035274  # 1 g = 0.035274 oz
        kg_to_lbs = 2.20462  # 1 kg = 2.20462 lbs
        oz_to_g = 28.3495  # 1 oz = 28.3495 g
        lbs_to_kg = 0.453592  # 1 lb = 0.453592 kg
        kg_to_oz = 35.274  # 1 kg = 35.274 oz
        g_to_lbs = 0.00220462  # 1 g = 0.00220462 lbs

        # Retrieving and processing values from the 'Added Refrigerant' section
        # added_lbs = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight1Added', 0))
        # added_oz = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight2Added', 0))
        # added_kg = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight1Added', 0))
        # added_g = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight2Added', 0))

        # # Retrieving and processing values from the 'Removed Refrigerant' section
        # removed_lbs = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight1Removed', 0))
        # removed_oz = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight2Removed', 0))
        # removed_kg = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight1Removed', 0))
        # removed_g = float(form_data_dictionary.get(
        #     'currentRefrigerantWeight2Removed', 0))

        total_added_kg = 0
        total_added_lbs = 0
        total_added_g = 0

        total_removed_kg = 0
        total_removed_lbs = 0
        total_removed_g = 0
        total_removed_oz = 0

        total_added_lbs_form_ver = 0
        total_added_oz_form_ver = 0
        total_added_kg_form_ver = 0
        total_added_g_form_ver = 0

        total_removed_lbs_form_ver = 0
        total_removed_oz_form_ver = 0
        total_removed_kg_form_ver = 0
        total_removed_g_form_ver = 0

        total_added_oz = 0
        # For added
        # if form_data_dictionary.get('currentRefrigerantWeightUnitAdded') == 'metric':
        #     total_added_kg_form_ver = added_kg
        #     total_added_g_form_ver = added_g

        #     total_added_oz = (added_kg * kg_to_oz) + (added_g * g_to_oz)
        # else:  # Imperial
        #     total_added_lbs_form_ver = added_lbs
        #     total_added_oz_form_ver = added_oz

        #     total_added_oz = (added_lbs * lbs_to_oz) + total_added_oz_form_ver

        reclaimed_total_for_forms = form_data_dictionary.get(
            'TotalOzAdded')  # Reclaim Amount for Form
        charge_total_for_forms = form_data_dictionary.get(
            'TotalOzRemoved')  # Charge Amount for Form
        print("Total Refrigerant Added in oz: ", total_added_oz)

        total_removed_oz = 0
        # For removed
        # if form_data_dictionary.get('currentRefrigerantWeightUnitRemoved') == 'metric':
        #     total_removed_kg_form_ver = removed_kg
        #     total_removed_g_form_ver = removed_g

        #     total_removed_oz = (removed_kg * kg_to_oz) + (removed_g * g_to_oz)
        # else:  # Imperial
        #     total_removed_lbs_form_ver = removed_lbs
        #     total_removed_oz_form_ver = removed_oz

        #     total_removed_oz = (removed_lbs * lbs_to_oz) + \
        #         total_removed_oz_form_ver

        print("Total Refrigerant Removed in oz: ", total_removed_oz)

        def convert_radio_to_boolean(form_value):
            if form_value == 'on':
                return True
            elif form_value == '':
                return None
            else:
                return False
        form_data_dictionary['leakDetectedRadio'] = convert_radio_to_boolean(
            form_data_dictionary.get('leakDetectedRadio'))

        # repairStatusRadio

        if form_data_dictionary.get('repairStatusRadio') == 'leakRepaired':
            form_data_dictionary['repairStatusRadio'] = True
        elif form_data_dictionary.get('repairStatusRadio') == 'leakNotRepaired':
            form_data_dictionary['repairStatusRadio'] = False
        else:
            form_data_dictionary['repairStatusRadio'] = None

        def convert_check_to_boolean(form_value):
            if form_value == '':
                return True
            else:
                return False
        form_data_dictionary['vacuumTest'] = convert_check_to_boolean(
            form_data_dictionary.get('vacuumTest'))
        form_data_dictionary['compressorOil'] = convert_check_to_boolean(
            form_data_dictionary.get('compressorOil'))
        form_data_dictionary['pressureTest'] = convert_check_to_boolean(
            form_data_dictionary.get('pressureTest'))
        form_data_dictionary['noLongerContainsRefrigerant'] = convert_check_to_boolean(
            form_data_dictionary.get('noLongerContainsRefrigerant'))

        
        current_user_first_name = session.get('user_first_name')
        current_user_last_name = session.get('user_last_name')
        combined_name = current_user_first_name + " " + current_user_last_name
        # Mapping form data to model attributes
        model_data = {
            # Assuming it's in the correct date format
            'repair_date': form_data_dictionary.get('current_date'),
            'refrigerant_type': form_data_dictionary.get('refrigerant_type_send'),
            # Assuming 'true' or 'false' strings
            'leak_test_result': form_data_dictionary.get('leakDetectedRadio'),
            # Similar assumption
            'is_leak_repaired': form_data_dictionary.get('repairStatusRadio'),
            'no_longer_contains_refrigerant': form_data_dictionary.get('noLongerContainsRefrigerant'),
            'vacuum_test_performed': form_data_dictionary.get('vacuumTest'),
            'compressor_oil_removed': form_data_dictionary.get('compressorOil'),
            'pressure_test_performed': form_data_dictionary.get('pressureTest'),
            'additional_notes': form_data_dictionary.get('additionalNotes'),
            'psig_result': psig_result,
            'tech_id': session.get('tech_id'),
            'unit_id': session.get('unit_id'),
            'refrigerant_added_total_oz': charge_total_for_forms,  # Amount added to unit
            'refrigerant_removed_total_oz': reclaimed_total_for_forms,  # Amount removed from unit
            'refrigerant_added_lbs_form_ver': total_added_lbs_form_ver,
            'refrigerant_removed_lbs_form_ver': total_removed_lbs_form_ver,
            'refrigerant_removed_kg_form_ver': total_removed_kg_form_ver,
            'refrigerant_added_kg_form_ver': total_added_kg_form_ver,
            'refrigerant_added_g_form_ver': total_added_g_form_ver,
            'refrigerant_removed_g_form_ver': total_removed_g_form_ver,
            'refrigerant_added_oz_form_ver': total_added_oz_form_ver,
            'refrigerant_removed_oz_form_ver': total_removed_oz_form_ver,
            "technician_name": combined_name
        }

        # Save to database before sending email.
        CRUD.create(Repair_form, **model_data)
        # Update unit table with new data.
        CRUD.update(Unit, unit_id=session.get('unit_id'),
                    attr="last_maintenance_date", new=model_data['repair_date'])

        # Math for new amount of refrigerant in unit table in database.
        previous_unit_data = CRUD.read(
            Unit, all=False, unit_id=session.get('unit_id'))

        previous_amount_oz = previous_unit_data.amount_of_refrigerant_in_unit_oz

        #Keeping track of refrigerant in unit, saving to database.
        new_amount_oz = float(
            previous_amount_oz) + float(charge_total_for_forms) - float(reclaimed_total_for_forms)    

        ###################################################
        # Update amount of refrigerant inside Unit.
        CRUD.update(Unit, unit_id=session.get('unit_id'),
                    attr="amount_of_refrigerant_in_unit_oz", new=new_amount_oz)
        ###################################################

        # Conversion factors
        oz_to_lbs = 1 / 16  # 1 oz = 1/16 lb
        g_to_kg = 1 / 1000  # 1 g = 1/1000 kg

        ##############################################
        ##############################################

        display_lbs_oz_charge, display_kg_g_charge = convert_weights_for_display(float(charge_total_for_forms))
        display_lbs_oz_reclaim, display_kg_g_reclaim = convert_weights_for_display(float(reclaimed_total_for_forms))
        
        
        # Assuming the model_data dictionary and conversion factors are already defined
        # Prepare the email data dictionary
        email_data = {
            'refrigerant_added_lbs': total_added_lbs_form_ver,
            'refrigerant_added_oz': total_added_oz_form_ver,
            'refrigerant_added_kg': total_added_kg_form_ver,
            'refrigerant_added_g': total_added_g_form_ver,
            'refrigerant_removed_lbs': total_removed_lbs_form_ver,
            'refrigerant_removed_oz': total_removed_oz_form_ver,
            'refrigerant_removed_kg': total_removed_kg_form_ver,
            'refrigerant_removed_g': total_removed_g_form_ver,
            'display_lbs_oz_charge': display_lbs_oz_charge,
            'display_kg_g_charge': display_kg_g_charge,
            'display_lbs_oz_reclaim': display_lbs_oz_reclaim,
            'display_kg_g_reclaim': display_kg_g_reclaim,
        }

        # Now you can pass this dictionary to your render_template function
        # return render_template('your_template.html', email_data=email_data)

        # Now you can pass these variables to your Jinja template

        # record activity in activity logs table
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_user_role = session.get('user_role')
        # This will either be the contractor the user works for or the id of the contractor that is logged in depending on the user role.
        current_contractor_id = session.get('contractor_id')
        current_user_id = session.get('user_id')
        # Only technicians can fill out this form so it's ok to do this.
        tech_id = session.get('tech_id')

        current_user_first_name = session.get('user_first_name')
        current_user_last_name = session.get('user_last_name')
        combined_name = current_user_first_name + " " + current_user_last_name
        CRUD.create(Activity_Logs, technician_id=tech_id, activity_type='ODS-TAG', date_logged=current_date,
                    user_role=current_user_role, contractor_id=current_contractor_id, user_id=current_user_id, name=combined_name)

        # Send email to contractor
        try:
            print("start of try")
            # Set up Jinja2 environment
            env = Environment(loader=FileSystemLoader('templates/email'))
            template = env.get_template(
                'contractor-copy-of-ods-tag-email.html')

            current_tech_id = session.get('tech_id')
            # data for email
            tech_data = CRUD.read(Technician, all=False,
                                  technician_id=current_tech_id)
            user_detail_data = CRUD.read(
                User_Detail, all=False, user_id=tech_data.user_id)
            company_data = CRUD.read(
                Contractor, all=False, contractor_id=tech_data.contractor_id)
            unit_data = CRUD.read(
                Unit, all=False, unit_id=model_data['unit_id'])

            # Render the template with your data
            html_content = template.render(data=model_data, tech_data=tech_data,
                                           user_data=user_detail_data, company_data=company_data, unit_data=unit_data, email_data=email_data)

            # This needs to be dynamic based on the contractor's email we have in the database.
            msg = MIMEMultipart()
            msg['From'] = 'refit_dev@sidneyshapiro.com'
            msg['To'] = 'refit_dev@sidneyshapiro.com'
            msg['Subject'] = ("New ODS Tag Submitted by " + str(
                user_detail_data.first_name) + " " + str(user_detail_data.last_name))

            # Attach the HTML part to the email
            part = MIMEText(html_content, "html")
            msg.attach(part)

            email_text = msg.as_string()
            # Send an email to the email address typed in the form.
            # Using SMTP_SSL for secure connection
            smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)
            smtpObj.login('refit_dev@sidneyshapiro.com',
                          'P7*XVEf1&V#Q')  # Log in to the server
            smtpObj.sendmail('refit_dev@sidneyshapiro.com',
                             'refit_dev@sidneyshapiro.com', email_text)
            smtpObj.quit()  # Quitting the connection
            print("Email sent successfully!")
        except Exception as e:
            print("Oops, something went wrong: ", e)

        return redirect('/back-by-role')


@technician.route('/equipment common/qr-scan')
def qr_scan():
    return render_template('equipment common/qr-scan.html')


@technician.route('/recovery/recovery-ods-sheet')
def recovery_ods_sheet():
    return render_template('recovery/recovery-ods-sheet.html')


@technician.route('/equipment/equipment_pages', methods=['GET', 'POST'])
def equipment_page():
    if request.method == 'GET':
        return render_template('equipment/equipment_pages.html')
    else:
        print('error')
        return render_template('equipment/equipment_pages.html')


##################################################
# View History/Logs of Equipment/Cylinder Routes###
##################################################
# Make a selection between unit and cylinder
@technician.route('/choose-equipment-history-type', methods=['GET', 'POST'])
def choose_equipment_history_type():
    if request.method == 'GET':
        return render_template('technician/select-history-type.html')
    else:
        print('error')
        return render_template('technician/select-history-type.html')

# selected UNIT history


@technician.route('/select-history-type-technician-maintenance', methods=['GET', 'POST'])
def select_history_type_tech():

    if request.method == 'GET':
        return render_template('equipment/maintenance_history.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')

# selected CYLINDER history


@technician.route('/select-history-type-technician-cylinder', methods=['GET', 'POST'])
def select_history_type_tech_cylinder():
    if request.method == 'GET':
        return render_template('equipment/ODS-history.html')
    else:
        print('error')
        return render_template('equipment/ODS-history.html')
##################################################
##################################################


@technician.route('/equipment/ODS-history', methods=['GET', 'POST'])
def ODS_history():

    if request.method == 'GET':

        return render_template('equipment/ODS-history.html')
    else:
        print('error')
        return render_template('equipment/ODS-history.html')


@technician.route('/equipment/maintenance_history', methods=['GET', 'POST'])
def maintenance_history():

    if request.method == 'GET':
        return render_template('equipment/maintenance_history.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')


@technician.route('/register_technician/<token>/<int:id>', methods=['GET', 'POST'])
def signup_technician(token, id):
    if request.method == 'GET':
        contractor_id = id
        token = token
        print("Contractor ID: ", contractor_id)
        print("Token: ", token)
    return render_template('beta/register_technician.html', dt=contractor_id, tk=token)


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
                new="Engaged",
                token=token
            )

            tech_obj = CRUD.read(
                Technician_Offer,
                token=token
            )

            technician_id = tech_obj.technician_id

            CRUD.update(
                Technician,
                technician_id=technician_id,
                attr="date_begin",
                new=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            CRUD.update(Technician,
                        technician_id=technician_id,
                        attr="user_status",
                        new="Active")
            CRUD.update(Technician,
                        technician_id=technician_id,
                        attr="contractor_status",
                        new="Engaged")
            contractor = CRUD.read(
                Contractor,
                contractor_id=contractor_id,
            )

            contractor_user_detail_obj = CRUD.read(
                Contractor,
                contractor_id=contractor_id
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
            print(f"technicain_id:{technician_id}")

            technician_user_detail_obj = CRUD.read(
                User_Detail,
                user_id=technician_obj.user_id
            )

            technician_name = technician_user_detail_obj.first_name
            print("begin)")
            print("offer status: ", tech_obj.offer_status)
            send_contractor_email(
                contractor_name, technician_name, contractor_email, 'Engaged')
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
                new="Rejected",
                token=token
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
                contractor_id=contractor_id
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

            send_contractor_email(
                contractor_name, technician_name, contractor_email, "Rejected")

            return render_template('Login Flow/login.html')
    return render_template('Login Flow/login.html')


def send_contractor_email(contractor_name, technician_name, contractor_email, offer_status):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'refit_dev@sidneyshapiro.com'
        msg['To'] = 'refit_dev@sidneyshapiro.com'

        if offer_status == "Engaged":
            msg['Subject'] = "Technician Added Successfully"
            body = f"Hello {contractor_name} technician {
                technician_name} has accepted your offer."
        elif offer_status == "Rejected":
            msg['Subject'] = f"Technician has rejected your offer."
            body = f"Hello {contractor_name} technician {
                technician_name} has rejected your offer."

        msg.attach(MIMEText(body, 'plain'))

        user_obj = CRUD.read(User, email=contractor_email, all=False)
        technician_obj = CRUD.read(
            Technician, user_id=user_obj.user_id, all=False)

        email_text = msg.as_string()

        smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)
        smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')
        smtpObj.sendmail('refit_dev@sidneyshapiro.com',
                         'refit_dev@sidneyshapiro.com', email_text)
        smtpObj.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("Oops, something went wrong: ", e)


@technician.route('/equipment-info/<unique_id>', methods=['GET', 'POST'])
def equipment_info_page(unique_id):
    if request.method == 'GET':
        # 1. Get data from database
        print("inside get for /equipment-info")

        # 2 get unique_id from url
        unit_unique_url = unique_id
        tech_id = session.get('tech_id')

        # 3. Get row in database for specific equipment/unit.
        tag_data = CRUD.read(Tag, all=False, tag_url=str(unique_id))
        unit_id = tag_data.unit_id
        data = CRUD.read(Unit, all=False, unit_id=unit_id)

        # Get name of technician who registered equipment.
        tech_data = CRUD.read(Technician, all=False,
                              technician_id=data.technician_id)
        user_detail_data = CRUD.read(
            User_Detail, all=False, user_id=tech_data.user_id)

        session['new_unit_id'] = unit_id
        session['tag'] = unique_id
        session['tech_id'] = tech_id

        # Add scan log to database.
        current_scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        CRUD.create(Equipment_History, date_qr_scanned_eq=current_scan_date,
                    tech_id=tech_id, unit_id=unit_id)

        # remove previous, if any, unique_equipment_token from session.
        session.pop('unique_equipment_token', None)
        # save tag url to session.
        session['unique_equipment_token'] = str(unique_id)
        session['unit_id'] = unit_id

        
        display_lbs_oz, display_kg_g = convert_weights_for_display(float(data.amount_of_refrigerant_in_unit_oz))
        
        additional_lbs_oz, additional_kg_g = convert_weights_for_display(float(data.additional_charge))
        
        total_lbs_oz, total_kg_g = convert_weights_for_display(float(data.total_amount_refrigerant))

        # 3. Render html
        return render_template('beta/equipment_info.html', data=data, tech_id=tech_id, user_detail_data=user_detail_data, display_lbs_oz=display_lbs_oz, display_kg_g=display_kg_g, unit_unique_url=unit_unique_url, unique_id=unique_id, additional_lbs_oz=additional_lbs_oz, additional_kg_g=additional_kg_g, total_lbs_oz=total_lbs_oz, total_kg_g=total_kg_g)

    else:
        print('error')
        return render_template('equipment-info.html')


@technician.route('/buy-qr', methods=['GET', 'POST'])
def buy_qr_page():
    if request.method == 'GET':
        return render_template('Equipment Common/placeholder-buy-qr-tag.html')
    else:
        print('error')
        return render_template('equipment/maintenance_history.html')

# @technician.route('/equipment/repair')
# def repair():
 # return render_template('equipment/repair.html')
# @technician.route('/equipment/recovery')
# def recovery():
   # return render_template('equipment/recovery.html')


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

      # converting to pounds and ounces

        ureg = pint.UnitRegistry()
        factory_charge_amount = 1000
        ounces = factory_charge_amount * ureg.ounces
        pounds = ounces.to(ureg.pounds)

        print(pounds)
        print(ounces)

        return render_template('equipment/charge-equipment.html', type_of_refrigerant=type_of_refrigerant,  factory_charge_amount=factory_charge_amount, pounds=pounds, ounces=ounces, tech_id=tech_id)
    elif request.method == "POST":
        print("Inside Post for charge_equipment")


@technician.route('/RefrigerantTypeLookupData.csv')
def serve_csv():
    return send_file('RefrigerantTypeLookupData.csv', mimetype='text/csv', as_attachment=True, download_name='RefrigerantTypeLookupData.csv')


# ODP Tag Form on Equipment Scan
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
        x = CRUD.read(DetailedEquipmentScanView,
                      all=True, tech_id=current_tech_id)

        for equipment in x:
            print(equipment.tech_id)
            print(equipment.manufacturer)
            print(equipment.unit_type)
            print(equipment.date_qr_scanned_eq)

        return render_template("technician/unit_scan_history.html", equipment_list=x)

    return "Invalid request method"

# This is the digitized ods tag. (Singular Tag)


@technician.route("/ods-tags", methods=["GET", "POST"])
def ods_tags_new():
    if request.method == "GET":
        return render_template("beta/digitized_ods_tag.html")
    else:
        selected_repair_form_id = request.form.get('selected_ods_tag')
        print("selected_repair_form_id: ", selected_repair_form_id)

        # Get data from database
        data = CRUD.read(Repair_form, all=False,
                         repair_form_id=selected_repair_form_id)

        print("my data678", data.refrigerant_added_lbs_form_ver)
        print("step 2")

        current_tech_id = data.tech_id

        tech_data = CRUD.read(Technician, all=False,
                              technician_id=current_tech_id)
        user_detail_data = CRUD.read(
            User_Detail, all=False, user_id=tech_data.user_id)
        company_data = CRUD.read(
            Contractor, all=False, contractor_id=tech_data.contractor_id)
        unit_data = CRUD.read(Unit, all=False, unit_id=data.unit_id)

        #charge amount
        charge_amount = data.refrigerant_added_total_oz
        #reclaim amount
        reclaim_amount = data.refrigerant_removed_total_oz
        #############FOR CHARGE AMOUNT DISPLAY#############
        # For Charge Amount Display
        charge_lbs_oz_display, charge_kg_g_display = convert_weights_for_display(float(charge_amount))
        print(float(charge_amount))
        print(float(reclaim_amount))
        reclaim_lbs_oz_display, reclaim_kg_g_display = convert_weights_for_display(float(reclaim_amount))
        
        
        
        return render_template("beta/digitized_ods_tag.html", data=data, tech_data=tech_data, user_data=user_detail_data, company_data=company_data, unit_data=unit_data, charge_lbs_oz_display=charge_lbs_oz_display, charge_kg_g_display=charge_kg_g_display, reclaim_lbs_oz_display=reclaim_lbs_oz_display, reclaim_kg_g_display=reclaim_kg_g_display)

# This is the table with the list of all ods tags a technician has ever filled out.


@technician.route("/view_all_ods_tags", methods=["GET", "POST"])
def view_all_ods_tags():
    if request.method == "GET":
        tech_id_current = session.get('tech_id')
        data = CRUD.read(RepairFormUnitView, all=True, tech_id=tech_id_current)

        return render_template("beta/view_all_ods_tags.html", data=data)
    else:
        return "Invalid request method (you posted to this route)"


# This is the table with the list of all ods tags a EQUIPMENT HAS attached to it.
@technician.route("/view_unit_ods_tags", methods=["GET", "POST"])
def view_all_unit_ods_tags():
    if request.method == "GET":
        current_unit_id = session.get('unit_id')
        print("current_unit_id: ", current_unit_id)
        data = CRUD.read(RepairFormUnitView, all=True, unit_id=current_unit_id)
        print(data)
        return render_template("beta/view_all_ods_tags.html", data=data)
    else:
        return "Invalid request method (you posted to this route)"
    
@technician.route("/manual-input", methods=["GET", "POST"])
def manual_input():
    if request.method == "GET":
        return render_template("Equipment Common/newest-manual-input.html")
    else:
        return "Invalid request method (you posted to this route)"
    
    
@technician.route("/manual-input-search", methods=["POST"])
def manual_input_search():
    if request.method == "POST":
        print("inside manual-input-search")
        serial_number = request.form.get('EquipmentSerialNumber')
        qr_ref_number = request.form.get('EquipmentQrRef')
        dropdown_selected = request.form.get('dropdown')
        
        print("serial_number: ", serial_number)
        print("qr_ref_number: ", qr_ref_number)
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        print("dropdown_selected: ", dropdown_selected)
        
        if qr_ref_number != '' and dropdown_selected == 'QR':
            print("inside qr ref number is not none")
            current_tag_data = CRUD.read(Tag, all=False, tag_url=qr_ref_number)
            

            if current_tag_data != None:
                print("inside tag is not none")
                print("current_tag_data: ", current_tag_data.type)
                type_of_tag = current_tag_data.type
                
                if type_of_tag == 'cylinder':
                    cylinder_id = current_tag_data.cylinder_id
                    #Get the cylinder data from the cylinder table
                    print("Cylinder id from current tag data: ", cylinder_id)
                    cylinder_data = CRUD.read(Cylinder, all=False, cylinder_id=cylinder_id)
                    if cylinder_data != None:
                        url = 'cylinder_info/' + str(qr_ref_number)
                        return redirect(url)
                    else:
                        #This is not a valid tag number
                        return render_template("Equipment Common/newest-manual-input.html")
                elif type_of_tag == 'equipment':
                    #This is an equipment tag
                    #Get the unit_id from the tag table
                    unit_id = current_tag_data.unit_id
                    #Get the unit data from the unit table
                    unit_data = CRUD.read(Unit, all=False, unit_id=unit_id)
                    if unit_data != None:
                        #Go to equipment info page if unit_data is not None
                        url = 'equipment-info/' + str(qr_ref_number)
                        return redirect(url)
                    else:
                        #This is not a valid tag number
                        return render_template("Equipment Common/newest-manual-input.html")

                else:
                    #This is not a valid tag number
                    return render_template("Equipment Common/newest-manual-input.html")
        elif serial_number != '' and dropdown_selected == 'SERIAL':
            print("inside serial number is not none")
            #Try to get unit data with matching serial number
            unit_data = CRUD.read(Unit, all=False, serial_number=serial_number)
            
            print(unit_data.unit_id)

            if unit_data != None:
                qr_ref_for_unit = CRUD.read(Tag, all=False, unit_id=str(unit_data.unit_id))
                #Go to equipment info page if unit_data is not None
                url = 'equipment-info/' + str(qr_ref_for_unit.tag_url)
                return redirect(url)
            else:
                #This is not a valid serial number
                return render_template("Equipment Common/newest-manual-input.html")
    else:
        return "Invalid request method (you posted to this route)"
