from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD,Cylinder,Reclaim_Recovery, Refrigerant, Cylinder_Type, Tag
from models import CRUD, User,User_Detail,Contractor
from functools import wraps
import UUID_Generate
import pandas as pd

cylinder = Blueprint('cylinder', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def convert_to_oz(lb, oz):
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


@cylinder.route('/update_cylinder',methods=['GET','POST'])
def cylinderform():
    print('not post')
    if request.method == 'POST':
        print('this inside post')
        cylinderTagId       = request.form.get('cylinderTagId')
        refrigerantId       = request.form.get('refrigerantId')
        technicianId        = request.form.get('technicianId')
        cylinderType        = request.form.get('cylinderType')
        cylinderSize        = request.form.get('cylinderSize')
        createDate          = request.form.get('createDate')
        refrigerantWeight   = request.form.get('refrigerantWeight')
        refrigerantWeightAfterService = request.form.get('refrigerantWeightAfterService')
        refrigerantWeightAdded        = request.form.get('refrigerantWeightAdded')
        addCylinder                  = request.form.get('addCylinder')
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
    return render_template(('cylinder/cylinder.html')) #for testing

@cylinder.route('/new_cylinder_new_qr',methods=['GET','POST'])

@cylinder.route("/new_cylinder", methods=["GET", "POST"])
def formcylinder():
    if request.method == 'POST':
        # Get data from form
        createDate = request.form.get('createDate')
        name = request.form.get('wholeSaler')
            # Cylinder information
        cylinderSize = request.form.get('cylinder_size')
        cylinderTareWeightUnit = request.form.get('tareWeightUnit')

        print("cylinderTareWeightUnit:" + cylinderTareWeightUnit)
        print(type(cylinderTareWeightUnit))


        tare_weight_entered_value = request.form.get('tareWeight1')
        tare_weight_second_entered_value = request.form.get('tareWeight2')
        
        if tare_weight_second_entered_value == None:
            tare_weight_second_entered_value = 0
        print("SECOND VALUE:" + tare_weight_second_entered_value)

        entered_lbs = request.form.get('currentRefrigerantWeight1')
        entered_oz = request.form.get('currentRefrigerantWeight2')
        
        print("entered_lbs:" + entered_lbs + "entered_oz:" + entered_oz)

        if cylinderTareWeightUnit == "12":
            print("inside HERE")
            tareWeight = convert_to_oz(tare_weight_entered_value, tare_weight_second_entered_value)
            print("Tare weight in OZ from lb:" + str(tareWeight))
        else:
            print("inside THERE")
            tareWeight = convert_kg_to_oz(request.form.get('tareWeight1'), request.form.get('tareWeight2'))
            print("Tare weight in OZ from kg:" + str(tareWeight))

        #Refrigerant information
        refrigerantType = request.form.get('refrigerantType')
        currentRefrigerantweightUnit = request.form.get('currentRefrigerantWeightUnit')
        print("currentRefrigerantweightUnit:" + cylinderTareWeightUnit)
        
        #My Debugging
        print(request.form.get('currentRefrigerantWeight1'))
        print(request.form.get('currentRefrigerantWeight2'))
        
        if currentRefrigerantweightUnit == "12":
            print("Inside HERE HERE!")
            currentRefrigerantweight = convert_to_oz(entered_lbs, entered_oz)
            print("currentRefrigerantweight from lb: " + str(currentRefrigerantweight))
        else:
            print("Inside THERE THERE!")
            currentRefrigerantweight = convert_kg_to_oz(request.form.get('currentRefrigerantWeight1'), request.form.get('currentRefrigerantWeight2'))
            print("currentRefrigerantweight from kg" + str(currentRefrigerantweight))

        print("currentRefrigerantweight" + str(currentRefrigerantweight))
        print(f"CreateDate is{createDate}")
        print(f"wholeSaler name is {name}")
        print(f"cylinderTareWeightUnit is {cylinderTareWeightUnit}")
        print(f"refrigerantType: {refrigerantType}")
        print(f"Cylinder Weight: {cylinderSize}")
        print(request.method)
#nithin changes
        # data_cylinder = CRUD.create(Cylinder, added_date = createDate, cylinder_type_id = 2, cylinder_size = 50, cylinder_tare_weight = tareWeight,current_refrigerant_weight = 50)
        # return render_template ("New Cylinder/tag-linked.html") #redirect(url_for('cylinder.cylinder'))

    
    
        ##########Adding Cylinder to the database##############
        
        #Step 1. Find out refrigerant_id based on the name typed into the form (auto generated value from the database.) based on refrigerant name.
        df = pd.read_csv("RefrigerantTypeLookupData.csv") #csv file with refrigerant types and their corresponding id's.
        
        #converting to lower case to match csv file where all entries are lowercase.
        refrigerantType = refrigerantType.lower()
        # Using the query method to filter rows
        filtered_rows = df.query("refrigerant_name == @refrigerantType")
        print(filtered_rows)

        refrigerant_type_id_from_db = None
        
        # If you want to get the first occurrence
        if not filtered_rows.empty:
            single_row = filtered_rows.iloc[0]
            refrigerant_type_id_from_db = int(filtered_rows.iloc[0]['refrigerant_id'])
            print(single_row)
        else:
            print("No rows found")
            flash("No matching refrigerant found with name below. (Check list of refrigerants in RefrigerantTypeLookupData.csv)", "error")  # The second argument "error" is an optional category.
            return render_template("New Cylinder/new-cylinder.html")
        
        
        #Step 2: Create a new row in the database for the cylinder
        #Form needs a place for user to type in cylinder_size, right now we are getting the amount of refrigerant in the cylinder which in the case that the cylinder is brand new it would be equal to the size, however in any other case, it will not.
        #The same goes for needing a drop down for cylinder type.
        new_row =CRUD.create(Cylinder, added_date = createDate, cylinder_tare_weight = tareWeight, refrigerant_id = refrigerant_type_id_from_db, current_refrigerant_weight = currentRefrigerantweight, supplier = name, cylinder_size = cylinderSize, cylinder_type_id = 1 )
        print(new_row.cylinder_id)
        PK = new_row.cylinder_id
        print("PK:" + str(PK))
        
        #Step 3. Geneate a unique url token that can be used on the QR Code when they are manufactured.
        #Note in the future this unique url token may directly come from the QR code itself instead of being generated here.
        
        unique_cylinder_token = None
        #either generate a new unique token or use the one that was passed in from the QR code registration page.
        if session.get('QR_unique_token') != None: #if the user got here from the new QR code registration page.
            unique_cylinder_token = session.get('QR_unique_token')
            print("Unique_Cylinder_Token: ", unique_cylinder_token)
            
            #new row in tag table
            CRUD.create(Tag, tag_url = unique_cylinder_token, cylinder_id = PK, type = "cylinder")
            return render_template ("New Cylinder/tag-linked.html",unique_cylinder_token = unique_cylinder_token) #redirect(url_for('cylinder.cylinder'))
            
        else:
            #there was an error, ask user to try scanning again.
            unique_cylinder_token = UUID_Generate.CylinderQRGenerator.generate_cylinder_unique_id(PK)
            
        print("Unique_Cylinder_Token: ", unique_cylinder_token)
        #CRUD.update(Cylinder, 'unique_url_id', new = unique_cylinder_token, cylinder_id = PK)
        return render_template ("New Cylinder/tag-linked.html",unique_cylinder_token = unique_cylinder_token) #redirect(url_for('cylinder.cylinder'))
    else:
        return render_template("New Cylinder/new-cylinder.html")


#Later this will be changed to a dynamic route that will take in the unique cylinder link from the QR code.
@cylinder.route("/cylinder_info/<unique_id>", methods=["GET", "POST"])
def CylinderInfo(unique_id):
    if request.method == 'GET':
        print("inside get for /cylinder_info")
        
        #1. Getting the cylinder id from the database based on the <unique id>.
        print("unique_id: " + unique_id)
        
        #Find cylinder id based on tag_url
        tag_data = CRUD.read(Tag, all = False, tag_url = unique_id)
        
        #get cylinder id from tag table
        cyl_id = tag_data.cylinder_id
        
        #2. Get row in database for specific cylinder.
        data = CRUD.read(Cylinder, all = False, cylinder_id = cyl_id)
        
        print(data.refrigerant_id)
        
        #Get foreign keys to search other tables.
        cylinder_refrigerant_id = data.refrigerant_id
        current_cylinder_type_id = data.cylinder_type_id
        
        #Get name of refrigerant and the type of cylinder.
        refrigerant_table_lookup = CRUD.read(Refrigerant, all = False, refrigerant_id = cylinder_refrigerant_id)
        cylinder_type_lookup = CRUD.read(Cylinder_Type, all = False, cylinder_type_id = current_cylinder_type_id)    
        
        name_data = {
            "refrigerant_name": refrigerant_table_lookup.refrigerant_name,
            "cylinder_type": cylinder_type_lookup.type_name
        }
        
        return render_template("beta/cylinder_info.html", data=data, name = name_data)
    
    
#Technician History Cylinders
@cylinder.route("/technician_history", methods=["GET", "POST"])
def tech_history_history():
    if request.method == 'GET':
        print("inside get for /technician-history")
        current_tech_id = session.get('tech_id')
        
        x = CRUD.read(Cylinder, all = True, technician_id = 84)
                
        counter = 0
        for i in x:
            print(x[counter].cylinder_id)
            print("Weight:", x[counter].current_refrigerant_weight)
            counter += 1
        
        return render_template("technician/technician_history.html")