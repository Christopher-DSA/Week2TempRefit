from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD, Cylinder, Reclaim_Recovery, Refrigerant, Cylinder_Type, Tag, Cylinder_History, Activity_Logs, Technician
from models import CRUD, User, User_Detail, Contractor
from functools import wraps
import UUID_Generate
import pandas as pd
import datetime


cylinder = Blueprint('cylinder', __name__)


def convert_weights_for_display(amount_oz): #Used in Charge Cylinder info and Recovery Cylinder info routes in this module.
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def convert_to_oz(lb, oz):
    '''Converts lb and oz to just oz for storage in the database.'''
    lb = float(lb)
    oz = float(oz)
    total_oz = lb * 16 + oz
    return total_oz


def convert_kg_to_oz(kg, gm):
    kg = float(kg)
    gm = float(gm)
    total_gm = kg * 1000 + gm
    total_oz = total_gm * 0.035274
    return total_oz


@cylinder.route("/cylinder")
@login_required
def cylindertype():
    return render_template('New Cylinder/cylinder-type.html')


# @cylinder.route('/new-cylinder')
# # @login_required
# def new_cylinder():
#     return render_template('New Cylinder/new-cylinder.html')


@cylinder.route('/recover_cylinder_clean')
# @login_required
def cylinder_recovery():
    return render_template('New Cylinder/clean-cylinder.html')


@cylinder.route('/recover_cylinder_burnout')
# @login_required
def cylinder_recovery_newequipment():
    return render_template('New Cylinder/burnout-cylinder.html')


@cylinder.route('/update_cylinder', methods=['GET', 'POST'])
def cylinderform():
    print('not post')
    if request.method == 'POST':
        print('this inside post')
        cylinderTagId = request.form.get('cylinderTagId')
        refrigerantId = request.form.get('refrigerantId')
        technicianId = request.form.get('technicianId')
        cylinderType = request.form.get('cylinderType')
        cylinderSize = request.form.get('cylinderSize')
        createDate = request.form.get('createDate')
        refrigerantWeight = request.form.get('refrigerantWeight')
        refrigerantWeightAfterService = request.form.get(
            'refrigerantWeightAfterService')
        refrigerantWeightAdded = request.form.get('refrigerantWeightAdded')
        addCylinder = request.form.get('addCylinder')
        print("------------------------------")
        print(cylinderTagId)
        print(refrigerantId)
        print(technicianId)
        print(cylinderType)
        print(cylinderSize)
        print(createDate)
        print(refrigerantWeight)
        print(refrigerantWeightAfterService)
        print(refrigerantWeightAdded)
        print(addCylinder)
        return render_template(('technician/dashboardtechnician.html'))
    print(request.method)
    # print('rendering cylinder form')
    return render_template(('cylinder/cylinder.html'))  # for testing


@cylinder.route("/new_cylinder", methods=["GET", "POST"])
def new_cylinder_view():
    if request.method == 'POST':
        ########### Get data from form############
        createDate = request.form.get('createDate')
        metricOrImperial = request.form.get('currentRefrigerantWeightUnit')
        useCase = request.form.get('useCase')
        cleanOrBurnout = request.form.get('gasQuality')
        refrigerantType = request.form.get('refrigerantType')
        wholesaler = request.form.get('wholesaler')
        
        
        # current_refrigerant_weight_lbs and current_refrigerant_weight_kg
        bigUnit = request.form.get('currentRefrigerantWeight1')  # kg or lbs
        smallUnit = request.form.get('currentRefrigerantWeight2')  # oz or gm

        ############ Process Data#################
        # Conversion factors
        oz_to_lbs = 16
        g_to_kg = 1000

        lbs_to_kg = 0.453592
        kg_to_lbs = 2.20462

        # Unit Conversions for Database Storage
        current_refrigerant_weight_lbs = 0
        current_refrigerant_weight_kg = 0
        current_refrigerant_weight = 0 #oz only
        # if the user selected "imperial" for the current refrigerant weight unit.
        if metricOrImperial == "imperial":
            current_refrigerant_weight_lbs = float(
                bigUnit) + float(smallUnit) / oz_to_lbs
            current_refrigerant_weight_kg = current_refrigerant_weight_lbs * lbs_to_kg
            current_refrigerant_weight_kg = round(
                current_refrigerant_weight_kg, 2)
            current_refrigerant_weight_lbs = round(
                current_refrigerant_weight_lbs, 2)
            current_refrigerant_weight = float(bigUnit) * 16 + float(smallUnit)
        else:  # if the user selected "metric" for the current refrigerant weight unit.
            current_refrigerant_weight_kg = float(
                bigUnit) + float(smallUnit) / g_to_kg
            current_refrigerant_weight_lbs = current_refrigerant_weight_kg * kg_to_lbs
            current_refrigerant_weight_kg = round(
                current_refrigerant_weight_kg, 2)
            current_refrigerant_weight_lbs = round(
                current_refrigerant_weight_lbs, 2)
            current_refrigerant_weight = float(bigUnit) * 35.274 + float(smallUnit) * 0.035274


        # Cylinder Use Case Conversion to Cylinder Type ID
        cyl_type_id = 17
        if useCase == "charge":
            cyl_type_id = 3
        elif useCase == "recovery":
            cyl_type_id = 1
        else:
            cyl_type_id = 17

        # clean_or_burnout Conversion to clean_or_burnout
        cleanOrBurnout = cleanOrBurnout.lower()
        if cleanOrBurnout == "clean":
            cleanOrBurnout = "clean"
        else:
            cleanOrBurnout = "burnout"

        
        current_user_id = session.get('user_id')
        current_tech_id = session.get('tech_id')

        # data to be passed on to crud create for Cylinder table.
        my_dictionary = {
            # the date the cylinder was added to the database. Comes from the form.
            'added_date': createDate,
            # the id of the cylinder type based on the cylinder_type table.
            'cylinder_type_id': cyl_type_id,
            'clean_or_burnout': cleanOrBurnout,  # the string "clean" or "burnout"
            # the string of the refrigerant type. Example: "R-22", "R-134a", "R-410a", etc.
            'refrigerant_type': refrigerantType,
            # the current refrigerant weight in lbs.
            'current_refrigerant_weight_lbs': current_refrigerant_weight_lbs,
            # the current refrigerant weight in kg.
            'current_refrigerant_weight_kg': current_refrigerant_weight_kg,
            # the current refrigerant weight in oz.
            'current_refrigerant_weight': current_refrigerant_weight,
            'supplier': wholesaler,
            # the id of the user who added the cylinder to the database.
            'user_id': current_user_id,
            # the id of the technician who added the cylinder to the database.
            'technician_id': current_tech_id
        }

        ############ CRUD Create Row for new Cylinder#############
        new_row = CRUD.create(Cylinder, **my_dictionary)

        ############# Create Row in Tag Table###############
        unique_cylinder_token = None
        # If the user got here from the new QR code registration page. Which should be the case.
        if session.get('QR_unique_token') != None:
            # This is comes from when user scans the code in the first place.
            unique_cylinder_token = session.get('QR_unique_token')
            print("Succesfully added new Tag row to database.")

            # New Row in Tag Table
            CRUD.create(Tag, tag_url=unique_cylinder_token,
                        cylinder_id=new_row.cylinder_id, type="cylinder", technician_id=current_tech_id, user_id = current_user_id)

            # 4. Record the activity in the Activity_Logs table.#####################
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            current_user_role = session.get('user_role')
            # This will either be the contractor the user works for or the id of the contractor that is logged in depending on the user role.
            current_contractor_id = session.get('contractor_id')
            current_user_id = session.get('user_id')
            tech_id = session.get('tech_id')
            current_user_first_name = session.get('user_first_name')
            current_user_last_name = session.get('user_last_name')
            combined_name = current_user_first_name + " " + current_user_last_name

            if current_user_role == 'technician':
                CRUD.create(Activity_Logs, technician_id=tech_id, activity_type='NEW-CYLINDER-REGISTERED', date_logged=current_date,
                            user_role=current_user_role, contractor_id=current_contractor_id, user_id=current_user_id, name=combined_name)
            elif current_user_role == 'contractor':
                CRUD.create(Activity_Logs, activity_type='NEW-CYLINDER-REGISTERED', date_logged=current_date,
                            user_role=current_user_role, contractor_id=current_contractor_id, user_id=current_user_id, name=combined_name)

            ############################################
            return render_template("New Cylinder/tag-linked.html", unique_cylinder_token=unique_cylinder_token)
        else:
            print("error adding row to TAG table, Try enabling cookies in your browser for site to function properly.")
            return redirect('back-by-role')
    else:  # should not be a GET request but if somehow it is then...
        print("This route only accepts POST requests.")
        return render_template("New Cylinder/new-cylinder.html")


@cylinder.route("/inventory-cylinder-info", methods=["POST"])
def InventoryCylinderInfo():
    if request.method == "POST":
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa837e7dh97832hd9823dh')
        unique_id = request.form.get('unique_id')
        print("GOT IT 1923U891DJS12802DJ:     " + unique_id)
        # 1. Get row in database for specific tag. From Tag Table.
        # Get Technician ID from session
        # get cylinder id from tag table

        # 2. Get row in database for specific cylinder. From Cylinder Table.
        cylinder_data = CRUD.read(Cylinder, all=False, cylinder_id=unique_id)
        if cylinder_data is None:
            return redirect("/")  # cylinder does not exist in the database.
        elif cylinder_data.cylinder_type_id == 1:  # 1 is recovery a recovery cylinder
            my_cylinder_type = 'Recovery Cylinder'
            #Get name of technician who registered equipment.
            print ("Recovry Cylinder")
            tech_data = CRUD.read(Technician, all=False, technician_id=cylinder_data.technician_id)
            user_detail_data = CRUD.read(User_Detail, all=False, user_id=tech_data.user_id)
            return render_template("beta/recovery_cylinder_info.html", data=cylinder_data, tag_data="none", user_detail_data=user_detail_data)
        elif cylinder_data.cylinder_type_id == 3:  # 3 is a charge cylinder
            my_cylinder_type = 'Charge Cylinder'
            print ("Charge Cylinder")
            tech_data = CRUD.read(Technician, all=False, technician_id=cylinder_data.technician_id)
            user_detail_data = CRUD.read(User_Detail, all=False, user_id=tech_data.user_id)
            return render_template("beta/charge_cylinder_info.html", data=cylinder_data, tag_data="none", user_detail_data=user_detail_data)
        

@cylinder.route("/cylinder_info/<unique_id>", methods=["GET", "POST"])
def CylinderInfo(unique_id):
    if request.method == 'GET':
        print("inside get for /cylinder_info")

        # 1. Get row in database for specific tag. From Tag Table.
        # Get Tag Data from Tag Table
        tag_data = CRUD.read(Tag, all=False, tag_url=unique_id)
        # Get Technician ID from session
        tech_id = session.get('tech_id')
        # get cylinder id from tag table
        cyl_id = tag_data.cylinder_id

        # 2. Get row in database for specific cylinder. From Cylinder Table.
        cylinder_data = CRUD.read(Cylinder, all=False, cylinder_id=cyl_id)
        if cylinder_data is None:
            return redirect("/")  # cylinder does not exist in the database.
        elif cylinder_data.cylinder_type_id == 1:  # 1 is recovery a recovery cylinder
            my_cylinder_type = 'Recovery Cylinder'
            print("tech id from cylinder table: ", cylinder_data.technician_id)
            tech_data = CRUD.read(Technician, all=False, technician_id=cylinder_data.technician_id)
            user_detail_data = CRUD.read(User_Detail, all=False, user_id=tech_data.user_id)
            
            # Making string, lbs and oz, and kg and g for display
            display_lbs_oz, display_kg_g = convert_weights_for_display(float(cylinder_data.current_refrigerant_weight))
            
            return render_template("beta/recovery_cylinder_info.html", data=cylinder_data, tag_data=tag_data, my_cylinder_type=my_cylinder_type, user_detail_data=user_detail_data, display_lbs_oz=display_lbs_oz, display_kg_g=display_kg_g)
        elif cylinder_data.cylinder_type_id == 3:  # 3 is a charge cylinder
            my_cylinder_type = 'Charge Cylinder'
            tech_data = CRUD.read(Technician, all=False, technician_id=cylinder_data.technician_id)
            user_detail_data = CRUD.read(User_Detail, all=False, user_id=tech_data.user_id)
            
            
            # Making string, lbs and oz, and kg and g for display            
            display_lbs_oz, display_kg_g = convert_weights_for_display(float(cylinder_data.current_refrigerant_weight))

            return render_template("beta/charge_cylinder_info.html", data=cylinder_data, tag_data=tag_data, my_cylinder_type=my_cylinder_type, user_detail_data=user_detail_data, display_lbs_oz=display_lbs_oz, display_kg_g=display_kg_g)



# Refrigerant Recovery Form. Only used for Recovery Type Cylinders.
@cylinder.route("/refrigerant_recovery", methods=["GET", "POST"])
def recover_refrigerant():
    if request.method == 'GET':
        cly_id = session.get('cyl_id')
        refrigerant = session.get('gas_name')
        cylinder_size = session.get('size')
        weight = session.get('weight')
        cylinder_type = session.get('type')
        cylinder_tare_weight = session.get('cylinder_tare_weight')
        tare_weight_before_repair = session.get('tare_weight_before_repair')

        tag_data = CRUD.read(Tag, all=False, cylinder_id=cly_id)
        tag_num = tag_data.tag_number

        cyl_data = CRUD.read(Cylinder, all=False, cylinder_id=cly_id)
        technician_id = cyl_data.technician_id

        current_date = datetime.date.today()

        dt = {
            "tag": tag_num,
            "name": refrigerant,
            "tech_id": technician_id,
            "size": cylinder_size,
            "date": current_date,
            "type": cylinder_type,
            "weight": weight,
            "cylinder_tare_weight": cylinder_tare_weight,
            "tare_weight_before_repair": tare_weight_before_repair
        }
        print(dt)
        return render_template("cylinder/cylinder_recovery_newequipment.html", dt=dt)
    elif request.method == 'POST':
        # 0
        current_cyl_id = session.get('cyl_id')

        # 1. The New Cylinder tare weight BEFORE service is the tare weight of the cylinder AFTER this current service.
        CRUD.update(Cylinder, 'tare_weight_before_repair', new=request.form.get(
            'cylinder_weight_after_service'), cylinder_id=current_cyl_id)
        # 2. Calcuate the new refrigerant weight in the cylinder in oz. (The form calculates this in lbs so we will need to convert)
        calculated_refrigerant = float(
            request.form.get('refrigerantWeightAfterService'))

        converted_refrigerant_amount_oz = convert_to_oz(
            calculated_refrigerant, 0)
        previous_refrigerant_weight_oz = float(session.get('weight'))

        # 3. Update database "current_refrigerant_weight" with the new total amount of refrigerant in the cylinder.
        new_total_refrigerant_weight = converted_refrigerant_amount_oz + \
            previous_refrigerant_weight_oz
        CRUD.update(Cylinder, 'current_refrigerant_weight',
                    new=new_total_refrigerant_weight, cylinder_id=current_cyl_id)

        # 4. Update the tare weight of the cylinder AFT service.

        return render_template("cylinder/recovery_form_successful.html")


@cylinder.route('/recover_ref', methods=['POST'])
def recover_ref():
    cylinderTagId = request.form.get('cylinderTagId')
    refrigerantId = request.form.get('refrigerantId')
    technicianId = request.form.get('technicianId')
    cylinderType = request.form.get('cylinderType')
    cylinderSize = request.form.get('cylinderSize')
    createDate = request.form.get('createDate')
    currentRefrigerantWeight = request.form.get('currentRefrigerantWeight')
    refrigerantWeightReclaimed = request.form.get('refrigerantWeightReclaimed')
    refrigerantWeightAfterService = request.form.get(
        'refrigerantWeightAfterService')

    tag_data = CRUD.read(Tag, all=False, tag_number=cylinderTagId)
    cyl_id = tag_data.cylinder_id

    cyl_data = CRUD.read(Cylinder, all=False, cylinder_id=cyl_id)
    ref_id = cyl_data.refrigerant_id

    print("------------------------------")
    print(f"cylinder id is {cyl_id}")
    print(f"cylindeTagId is {cylinderTagId}")
    print(f"refrigerantId is {refrigerantId}")
    print(f"technicianId is {technicianId}")
    print(f"cylinderType is {cylinderType}")
    print(f"cylinderSize is {cylinderSize}")
    print(f"createDate is {createDate}")
    print(f"currentRefrigerantWeight is {currentRefrigerantWeight}")
    print(f"refrigerantWeightReclaimed is {refrigerantWeightReclaimed}")
    print(f"refrigerantWeightAfterService is {refrigerantWeightAfterService}")
    print("------------------------------")

    reclaim_data = CRUD.read(Reclaim_Recovery, all=False, cylinder_id=cyl_id)

    if reclaim_data is None:
        CRUD.create(
            Reclaim_Recovery,

            gas_type=refrigerantId,
            quantity_before_in_lbs=float(currentRefrigerantWeight),
            quantity_after_in_lbs=float(refrigerantWeightAfterService),
            notes="testing",
            date=createDate,
            status="testing",
            refrigerant_id=ref_id,
            cylinder_id=cyl_id,
        )
    else:
        CRUD.update(
            Reclaim_Recovery,
            cylinder_id=cyl_id,
            attr="quantity_before_in_lbs",
            new=currentRefrigerantWeight

        )
        CRUD.update(
            Reclaim_Recovery,
            cylinder_id=cyl_id,
            attr="quantity_after_in_lbs",
            new=refrigerantWeightAfterService

        )
        CRUD.update(
            Reclaim_Recovery,
            cylinder_id=cyl_id,
            attr="date",
            new=createDate

        )
        # CRUD.update(
        # Reclaim_Recovery,
        # cylinder_id = cyl_id,
        # attr= "gas_type",
        # new = refrigerantId

        # )
        # CRUD.update(
        # Reclaim_Recovery,
        # cylinder_id = cyl_id,
        # attr= "refrigerant_id",
        # new = ref_id

        # )
        CRUD.update(
            Reclaim_Recovery,
            cylinder_id=cyl_id,
            attr="notes",
            new="testing"

        )
        CRUD.update(
            Reclaim_Recovery,
            cylinder_id=cyl_id,
            attr="status",
            new="testing"

        )

    CRUD.update(
        Cylinder,
        cylinder_id=cyl_id,
        attr="current_refrigerant_weight",
        new=refrigerantWeightAfterService

    )

    return redirect(url_for('technician.dashboardtechnician'))


@cylinder.route("/technician_cylinder_history", methods=["GET", "POST"])
def cylinder_hist():
    if request.method == "GET":
        current_tech_id = session.get('tech_id')
        cylinder_hist = CRUD.read(
            Cylinder_History, all=True, technician_id=current_tech_id)

        for cylinder in cylinder_hist:
            print(f"Cylinder ID: {cylinder.cylinder_id}")
            print(f"Refrigerant Weight: {cylinder.refrigerant_weight}")
            print(f"Refrigerant Type: {cylinder.refrigerant_name}")
            print(f"Last Scanned: {cylinder.date_qr_scanned}")

        return render_template("technician/cyl_scan_history.html", cylinders_list=cylinder_hist)

    return "Invalid request method"
