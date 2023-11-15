from flask import Blueprint, redirect, render_template, request, url_for
from models import CRUD, Cylinder,Wholesaler,Refrigerant,Unit
#from datetime import datetime

new_cylinder = Blueprint('new_cylinder', __name__)

@new_cylinder.route("/new_cylinder", methods=["GET", "POST"])
def formcylinder():
    if request.method == 'POST':

        # Get data from form
        createDate = request.form.get('createDate')
        name = request.form.get('wholeSaler')

            # Cylinder information
        cylinderTareWeightUnit = request.form.get('tareWeightUnit')
  
        cylinderTareWeight=f"{request.form.get('tareWeight1')}, {request.form.get('tareWeight2')}"

            #Refrigerant information
        refrigerantType = request.form.get('refrigerantType')
        currentRefrigerantweightUnit = request.form.get('currentRefrigerantWeightUnit')
        #currentrefrigerantweightinlb = request.form.get('currentRefrigerantWeightLb')
        #currentrefrigerantweightinoz = request.form.get('currentRefrigerantWeightOz')
        currentRefrigerantWeight=f"{request.form.get('currentRefrigerantWeight1')}, {request.form.get('currentRefrigerantWeight2')}"

        print("New cylinder data succssfully retrieved.")

        #validate the data and pass data to database
        #new_cylinder=CRUD.create(Cylinder_Type, type_name=type_name)
        new_cylinder=CRUD.create(Cylinder, 
                                 create_date=createDate, cylinder_tare_weight=cylinderTareWeight) 

        new_wholesaler=CRUD.create(Wholesaler,
                                    name=name)

        new_refrigerant=CRUD.create(Refrigerant, 
                                    #refrigerant_name=refrigerantType, currentRefrigerantWeight=currentRefrigerantWeight)                             
        new_unit=CRUD.create(Unit, 
                             type_of_refrigerant=refrigerantType)

        #redirect to the appropriate page
        return redirect(url_for('cylinder.html'))

    return render_template("New Cylinder/new-cylinder.html")