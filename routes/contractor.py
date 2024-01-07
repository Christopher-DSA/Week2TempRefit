from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD,User,User_Detail,Contractor,Technician,Cylinder,Technician_Offer,Refrigerant, RepairFormUnitView, Repair_form
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import UUID_Generate
import datetime


# Blueprint Configuration
contractor = Blueprint('contractor', __name__)

# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user is a contractor
def contractor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_id in the session is the email of the user.
        user_id= session.get('user_id')

        #user = CRUD.read(User,user_id=user_id
        
        users_row_in_db = CRUD.read(User,user_id=user_id)
        user_role = users_row_in_db.role
        
        if not user_role or user_role != 'contractor':
            # Either user doesn't exist, or the user is not a contractor.
            return "Unauthorized", 403
        
        return f(*args, **kwargs)
    return decorated_function

# Route for when user creates an account as a contractor
@contractor.route("/formcontractor", methods=["GET", "POST"])
def formcontractor():
    if request.method == 'POST':
        # Get data from form
        name = request.form.get('name')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # confirmPassword = request.form.get('confirmPassword')
        companyName = request.form.get('companyName')
        branchId = request.form.get('branchId')
        address = request.form.get('address')
        city = request.form.get('city')
        province = request.form.get('province')
        postalCode = request.form.get('postalCode')
        phoneNumber = request.form.get('phoneNumber')
        print("Contractor data succssfully retrieved.")
        new_user=CRUD.create(User_Detail, address=address, city=city,province=province, postal_code=postalCode,telephone=phoneNumber)
        new_detail=CRUD.create(Contractor,user_id=session.get('user_id'),name=name,logo='logo', status='active',companyName=companyName,branchId=branchId)
        print("Contractor data succssfully added to database.")
        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("contractor/formcontractor.html")

@contractor.route("/dashboardcontractor")
@login_required
@contractor_required
def dashboardcontractor():
    # Render the dashboard
    user_id =session.get('user_id')
    first_name = session.get('user_first_name')
    technicians_table_lookup = CRUD.read(Technician, all = False, contractor_id = user_id)
    return render_template("contractor/chris_ver_contractor_dashboard.html",user=user_id,technicians=technicians_table_lookup,first_name=first_name)

@contractor.route('/handle_qr_code', methods=['POST'])
@login_required
def handle_qr_code():
    data = request.get_json()
    qr_code_text = data['qrCode']
    print("QR Code Text: ", qr_code_text)
    # You can handle the QR code text here as needed
    # Return a response
    return jsonify({'message': 'QR code received successfully.'}), 200


#This is the table with the list of all ods tags a specific technician has
@contractor.route("/view_my_techs_ods_tags", methods=["GET", "POST"])
def view_my_techs_ods_tags():
    if request.method == "GET":
        return render_template("beta/view_all_ods_tags.html")
    elif request.method == "POST":
        #We need to get the technician id from the table
        selected_technician = request.form.get('technician_id')
        data = CRUD.read(RepairFormUnitView, all=True, tech_id=selected_technician)
        
        
        return render_template("beta/view_all_ods_tags.html", data=data)
    
@contractor.route('/technician_details', methods=['GET', 'POST'])
def technician_managment():
        if request.method == 'GET':
            contractor_user_id =session.get('user_id')
            contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
            contractor_id = contractor_data.contractor_id
            technician_data = CRUD.read(Technician,contractor_id=contractor_id,contractor_status="Engaged", all = True)
            print("----------")
            # print(technician_data[0].license_expiry_date)
            # print(technician_data[1].user_id)
            technician_list = []
            for item in technician_data:
                ods_licence_no = item.ods_licence_number
                license_expiry_date = item.license_expiry_date
                date_begin = item.date_begin
                date_end = item.date_end
                user_status = item.user_status
                tech_user_id = item.user_id
                contactor_status = item.contractor_status
                user_detail_data = CRUD.read(User_Detail,user_id = tech_user_id )
                tech_email = CRUD.read(User,user_id = tech_user_id).email
                tech_firstname = user_detail_data.first_name
                tech_lastname = user_detail_data.last_name
                tech_id = item.technician_id
                tech_name = tech_firstname + " " + tech_lastname
                technician_obj = {
                "ods_licence_no": ods_licence_no,
                "date_begin": date_begin,
                "date_end":date_end,
                "user_status":user_status,
                "tech_user_id":tech_user_id,
                "contactor_status":contactor_status,
                "name":tech_name,
                "email":tech_email,
                "license_expiry_date":license_expiry_date,
                "tech_id":tech_id
                # "lastname":tech_lastname
                                        }
                technician_list.append(technician_obj)
            return render_template('contractor/technician_details.html',technicians=technician_list)
        return render_template('contractor/technician_details.html')

    
@contractor.route('/add_technician', methods=['GET', 'POST'])
def add_technician():
    # if request.method == 'GET':
    #     contractor_user_id =session.get('user_id')
    #     contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
    #     contractor_id = contractor_data.contractor_id
    #     return render_template('contractor/add_technician.html',contractor=contractor_id)
    if request.method == 'POST':
        email = request.form.get('email')
        print(f"Email address{email}")
        """Get the contractor id from the session so that the technician 
        add page can capture the it to add the new technician under the contractor 
        who sent the invitaiton"""
        contractor_user_id =session.get('user_id')
        contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
        user_data = CRUD.read(User,email=email, all = False)
        user_id = user_data.user_id
        details = CRUD.read(User_Detail,user_id=user_data.user_id, all = False)
        technician_data = CRUD.read(Technician,user_id=user_id, all = False)
        tech_id = technician_data.technician_id
        contractor_id = contractor_data.contractor_id
        contractor_name = contractor_data.name

        sent_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fname = details.first_name
        fname_upper = fname.upper()
        cname_upper = contractor_name.upper()
        print("----------------")
        # print(mname)
        # print(lname)
        print(email)
        print(fname_upper)
        print(cname_upper)
        
        print(user_id)
        print('technician_id: ', tech_id)
        print(sent_time)
        
        print("----------------")
        tech_token=UUID_Generate.technicianQRGenerator.generate_technician_unique_id()
        print(f"http://127.0.0.1:5000/register_technician/{tech_token}/{contractor_id}")
        try:
            msg = MIMEMultipart()
            msg['From'] = 'refit_dev@sidneyshapiro.com'
            msg['To'] = 'refit_dev@sidneyshapiro.com'
            msg['Subject'] = "You've Been invited to work as a Technician"
            body = f"Hello {fname_upper} you have been invited to work as a Technician for {cname_upper}. If you accept the offer please click the link http://127.0.0.1:5000/register_technician/{tech_token}/{contractor_id} and create an account as a technician."
            msg.attach(MIMEText(body, 'plain'))
            email_text = msg.as_string()
            #Send an email to the email address typed in the form.
            smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)  # Using SMTP_SSL for secure connection
            smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')  # Log in to the server
            smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
            smtpObj.quit()  # Quitting the connection
            print("Email sent successfully!")

            # Sending data to Technician_offer table
            tech_offer = CRUD.create(Technician_Offer,contractor_id=contractor_id,technician_id=tech_id,offer_status='pending',email_time_sent=sent_time,token=str(tech_token))
            tech_tbl = CRUD.update(Technician,technician_id=tech_id,attr='user_status', new='Pending')
        except Exception as e:
            print("Oops, something went wrong: ", e)
            return render_template('contractor/dashboardcontractor.html')
        return render_template('contractor/dashboardcontractor.html')
    return render_template('contractor/add_technician.html')

    
@contractor.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'GET':
            dt=[]
            tech_ids = []
            contractor_user_id =session.get('user_id')
            contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
            contractor_id = contractor_data.contractor_id
            technician_data = CRUD.read(Technician,contractor_id=contractor_id,contractor_status="Engaged", all = True)
            for i in technician_data:
                tech_ids.append(i.technician_id)
            
            for i in tech_ids:
                cylinder_data = CRUD.read(Cylinder,all = True,technician_id=i)
                # print(cylinder_data[0].cylinder_id)
                for cy in cylinder_data:
                    c_techId = cy.technician_id
                    c_id = cy.cylinder_id
                    c_size = cy.cylinder_size
                    c_tareWeight = cy.cylinder_tare_weight
                    c_addedDate = cy.added_date
                    c_referigentId = cy.refrigerant_id
                    data_refrigerant=CRUD.read(Refrigerant,refrigerant_id=c_referigentId)
                    c_refrigerant_name=data_refrigerant.refrigerant_name 
                    c_purchasedDate = cy.purchase_date
                    c_supplier = cy.supplier

                    cylinder= {
                        "technician_id": c_techId,
                        "id": c_id,
                        "size": c_size,
                        "tareWeight": c_tareWeight,
                        "addedDate": c_addedDate,
                        "refrigerantId": c_referigentId,
                        "refrigerant_name":c_refrigerant_name,
                        "purchasedDate": c_purchasedDate,
                        "supplier": c_supplier
                        }
                    dt.append(cylinder)
            # print(dt)
    return render_template('contractor/inventory.html',dt=dt)

@contractor.route('/delete/technician', methods=['POST'])
def delete_technician():
    if request.method == 'POST':
        user_id = request.form.get('technician_id')
        technician_data = CRUD.read(Technician, user_id=user_id, all=False)

        if technician_data:
            technician_id = technician_data.technician_id
        print(f'techncian_id: {technician_id}')
        print(f'user_id: {user_id}')

        # Update Technician_Offer Table      

        CRUD.update(
            Technician_Offer,
            attr="offer_status",
            new="Removed",
            technician_id=technician_id
        )

        # CRUD.update(
        #     Technician_Offer,
        #     technician_id=technician_id,
        #     attr="contractor_id",
        #     new=0
        # )
        # CRUD.update(
        #     Technician,
        #     technician_id=technician_id,
        #     attr="contractor_id",           
        #     new = 0
        #     )
        # Update Technician Table
        CRUD.update(
            Technician,
            technician_id=technician_id,
            attr="date_end",
            new=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

             
        CRUD.update(
            Technician,
            technician_id=technician_id,
            attr="contractor_status",
            new="Removed"
        )
        
        CRUD.update(
            Technician,
            technician_id=technician_id,
            attr="user_status",
            new="Independent"
        )
    
        flash('Technician deleted successfully!', 'success')

    else:
        flash('Technician not found!', 'error')

        return redirect(url_for('contractor.technician_managment'))

    return render_template('contractor/technician_details.html')


@contractor.route('/refrigerant', methods=['POST','GET'])
def inventory_Refrigerant():
        if request.method == 'GET':
            contractor_user_id =session.get('user_id')
            contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
            contractor_id = contractor_data.contractor_id
            technician_data = CRUD.read(Technician,contractor_id=contractor_id,contractor_status="Engaged", all = True)
            print("----------")
            print(contractor_id)
            tech_ids = []
            dt=[]
            ref_name={}

            for i in technician_data:
                tech_ids.append(i.technician_id)
            
            for i in tech_ids:
                cylinder_data = CRUD.read(Cylinder,all = True,technician_id=i)
                for cy in cylinder_data:
                    c_techId = cy.technician_id
                    c_id = cy.cylinder_id
                    c_size = cy.cylinder_size
                    c_tareWeight = cy.cylinder_tare_weight
                    c_addedDate = cy.added_date
                    c_referigentId = cy.refrigerant_id
                    data_refrigerant=CRUD.read(Refrigerant,refrigerant_id=c_referigentId)
                    c_refrigerant_name=data_refrigerant.refrigerant_name   
                    c_purchasedDate = cy.purchase_date
                    c_supplier = cy.supplier
                    ref_name[c_refrigerant_name] = ref_name.get(c_refrigerant_name, 0) + 1

                    cylinder= {
                        "technician_id": c_techId,
                        "id": c_id,
                        "size": c_size,
                        # "tareWeight": c_tareWeight,
                        # "addedDate": c_addedDate,
                        "refrigerantId": c_referigentId,
                        "refrigerant_name":c_refrigerant_name,
                        # "purchasedDate": c_purchasedDate,
                        "supplier": c_supplier
                        }
                    dt.append(cylinder)
            # print(dt)
            print(f"unique refrigerants:{ref_name} ")
            return render_template('contractor/refrigerant.html',dt=dt,unique_refrigerants_dict=ref_name)

@contractor.route('/reftype/<refrigerant>', methods=['POST','GET'])
def refrigerant_type(refrigerant):
    if request.method == 'GET':
            ref_name = str(refrigerant)
            print(ref_name)
            dt=[]
            tech_ids = []
            contractor_user_id =session.get('user_id')
            contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
            contractor_id = contractor_data.contractor_id
            technician_data = CRUD.read(Technician,contractor_id=contractor_id,contractor_status="Engaged", all = True)
            for i in technician_data:
                tech_ids.append(i.technician_id)
            
            for i in tech_ids:
                cylinder_data = CRUD.read(Cylinder,all = True,technician_id=i)
                
                for cy in cylinder_data:
                    c_techId = cy.technician_id
                    c_id = cy.cylinder_id
                    c_addedDate = cy.added_date
                    c_referigentId = cy.refrigerant_id
                    data_refrigerant=CRUD.read(Refrigerant,refrigerant_id=c_referigentId)
                    c_refrigerant_name=data_refrigerant.refrigerant_name
                    c_supplier = cy.supplier

                    if c_refrigerant_name == ref_name:
                        cylinder= {
                            "technician_id": c_techId,
                            "id": c_id,
                            "addedDate": c_addedDate,
                            "refrigerantId": c_referigentId,
                            "refrigerant_name":c_refrigerant_name,
                            "supplier": c_supplier
                            }
                        dt.append(cylinder)
    return render_template('contractor/refregerant_inventory.html',dt=dt)
