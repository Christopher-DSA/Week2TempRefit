from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD,Cylinder,Reclaim_Recovery
from models import CRUD, User,User_Detail,Contractor
from functools import wraps

cylinder = Blueprint('cylinder', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def convert_to_oz(lb, oz):
    lb = lb
    oz = oz
    total_oz = lb * 16 + oz
    return total_oz

def convert_kg_to_oz(kg, gm):
    kg = kg
    gm = gm
    total_gm = kg * 1000 + gm
    total_oz = total_gm * 0.035
    return total_oz


@cylinder.route("/cylinder")
@login_required
def cylindertype():
    return render_template('New Cylinder/cylinder-type.html')

@cylinder.route('/new-cylinder')
# @login_required
def new_cylinder():
    return render_template('New Cylinder/new-cylinder.html')

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

@cylinder.route("/new_cylinder", methods=["GET", "POST"])
def formcylinder():
    if request.method == 'POST':

        # Get data from form
        createDate = request.form.get('createDate')
        name = request.form.get('wholeSaler')

            # Cylinder information
        cylinderTareWeightUnit = request.form.get('tareWeightUnit')

        # if cylinderTareWeightUnit == 12:
        #     tareWeight = convert_to_oz(request.form.get('tareWeight1'), request.form.get('tareWeight2'))
        #     # return str(tareWeight)
        # else:
        #     tareWeight = convert_kg_to_oz(request.form.get('tareWeight1'), request.form.get('tareWeight2'))
        #     # return str(tareWeight)
  


            #Refrigerant information
        refrigerantType = request.form.get('refrigerantType')
        currentRefrigerantweightUnit = request.form.get('currentRefrigerantWeightUnit')

                                                    
        # if currentRefrigerantweightUnit == 12:
        #     currentRefrigerantweight = convert_to_oz(request.form.get('currentRefrigerantweight1'), request.form.get('currentRefrigerantWeight2'))
        #     # return str(currentRefrigerantweight)
        # else:
        #     currentRefrigerantweight = convert_kg_to_oz(request.form.get('currentRefrigerantweight1'), request.form.get('currentRefrigerantWeight2'))
        #     # return str(currentRefrigerantweight)

        print("New cylinder data succssfully retrieved.")

        #validate the data and pass data to database
        #new_cylinder=CRUD.create(Cylinder_Type, type_name=type_name)
        #new_cylinder=CRUD.create(Cylinder, 
                                 #create_date=createDate, cylinder_tare_weight=cylinderTareWeight) 

        #new_wholesaler=CRUD.create(Wholesaler,
                                   # name=name)

        # new_refrigerant=CRUD.create(Refrigerant, 
        #                             currentRefrigerantWeight=currentRefrigerantWeight)                             
        # new_unit=CRUD.create(Unit, 
        #                      type_of_refrigerant=refrigerantType)

        print(createDate)
        print(name)
        print(cylinderTareWeightUnit)
        # print(cylinderTareWeight1)
        # print(cylinderTareWeight2)
        # print(cylinderTareWeight)
        print(refrigerantType)
        print(currentRefrigerantweightUnit)
        # print(currentRefrigerantweight1)
        # print(currentRefrigerantweight2)
        # print(currentRefrigerantweight)
        print(request.method)
        print(type((request.form.get('tareWeight1'))))
        print(type((request.form.get('currentRefrigerantweight1'))))
        

        return render_template ("cylinder/cylinder.html") #redirect(url_for('cylinder.cylinder'))

    return render_template("New Cylinder/new-cylinder.html")






#end