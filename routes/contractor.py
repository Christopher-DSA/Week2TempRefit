from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUD, User,User_Detail,Contractor,Technician
from functools import wraps

contractor = Blueprint('contractor', __name__)

# @contractor.route("/contractor/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('contractor/dashboard.html')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

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
    #validate the data and pass data to database

        new_user=CRUD.create(User_Detail, address=address, city=city,province=province, postal_code=postalCode,telephone=phoneNumber)

        new_detail=CRUD.create(Contractor,user_id=session.get('user_id'),name=name,logo='logo', status='active',companyName=companyName,branchId=branchId)
        
    #redirect to the appropriate page

        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("contractor/formcontractor.html")

@contractor.route("/dashboardcontractor")
@login_required
@contractor_required
def dashboardcontractor():
    # Render the dashboard
    user_id =session.get('user_id')
    technicians_table_lookup = CRUD.read(Technician, all = False, contractor_id = user_id)
    return render_template("contractor/dashboardcontractor.html",user=user_id,technicians=technicians_table_lookup)

@contractor.route('/handle_qr_code', methods=['POST'])
@login_required
def handle_qr_code():
    data = request.get_json()
    qr_code_text = data['qrCode']
    print("QR Code Text: ", qr_code_text)
    # You can handle the QR code text here as needed

    # Return a response
    return jsonify({'message': 'QR code received successfully.'}), 200

@contractor.route('/technician_details', methods=['GET', 'POST'])
def technician_managment():
    if request.method == 'GET':
        contractor_user_id =session.get('user_id')
        contractor_data = CRUD.read(Contractor,user_id=contractor_user_id)
        contractor_id = contractor_data.contractor_id
        technician_data = CRUD.read(Technician,contractor_id=contractor_id, all = True)
        print("----------")
        print(technician_data[0].user_id)
        print(technician_data[1].user_id)
        technician_list = []
        for item in technician_data:
            ods_licence_no = item.ods_licence_number
            date_begin = item.date_begin
            date_end = item.date_end
            user_status = item.user_status
            tech_user_id = item.user_id
            contactor_status = item.contractor_status
            user_detail_data = CRUD.read(User_Detail,user_id = tech_user_id )
            tech_firstname = user_detail_data.first_name
            tech_lastname = user_detail_data.last_name
            technician_obj = {
            "ods_licence_no": ods_licence_no,
            "date_begin": date_begin,
            "date_end":date_end,
            "user_status":user_status,
            "tech_user_id":tech_user_id,
            "contactor_status":contactor_status,
            "firstname":tech_firstname,
            "lastname":tech_lastname
            }
            technician_list.append(technician_obj)

        return render_template('contractor/technician_details.html',technician = technician_list)
    return render_template('contractor/technician_details.html')