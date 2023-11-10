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

@cylinder.route("/cylinder", methods=['GET', 'POST'])
def cylinder():
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
        add_cylinder                  = request.form.get('addcylinder')
        print(cylinderTagId)
        return redirect(url_for('cylinder.cylinder_recovery.html')) #for testing
    return redirect(url_for('cylinder.cylinder')) #for testing

@cylinder.route("/cylinder", methods=["GET", "POST"])
def formcylinder():
    if request.method == 'POST':
        # Get data from form
        
        
    #redirect to the appropriate page

        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("New Cylinder/cylinder-type.html")

