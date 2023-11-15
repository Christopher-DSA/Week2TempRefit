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
        # return redirect(url_for('technician.dashboardtechnician'))
        return render_template(('technician/dashboardtechnician.html'))
    print(request.method)
    print('rendering cylinder form')
    return render_template(('cylinder/cylinder.html')) #for testing

#Temp routing to create/update cylinder
@cylinder.route('/create_cylinder', methods=['GET', 'POST'])
def cylinderform():
    if request.method == 'POST':
        cylinderTagId       = request.form.get('cylinderTagId')
        refrigerantId       = request.form.get('refrigerantId')
        technicianId        = request.form.get('technicianId')
        cylinderType        = request.form.get('cylinderType')
        cylinderSize        = request.form.get('cylinderSize')
        createDate          = request.form.get('createDate')
        refrigerantWeight   = request.form.get('refrigerantWeight')
        refrigerantWeightAfterService = request.form.get('refrigerantWeightAfterService')
        refrigerantWeightAdded        = request.form.get('refrigerantWeightAdded')
        addCylinder                  = request.form.get('addcylinder')
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

    return render_template(('cylinder/cylinder.html')) #for testing

# @cylinder.route("/cylinder", methods=["GET", "POST"])
# def formcylinder():
#     if request.method == 'POST':
#         # Get data from form
        
        
    #redirect to the appropriate page

    #     return redirect(url_for('contractor.dashboardcontractor'))
    # return render_template("New Cylinder/cylinder-type.html")