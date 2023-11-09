from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD, User,User_Detail,Contractor
from functools import wraps

cylinder = Blueprint('cylinder', __name__)

@cylinder.route("/cylinder", methods=["GET", "POST"])
def formcylinder():
    if request.method == 'POST':
        # Get data from form
        
        
    #redirect to the appropriate page

        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("New Cylinder/cylinder-type.html")