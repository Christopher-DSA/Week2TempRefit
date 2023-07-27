from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
from models import CRUDMixin, User,User_detail,Contractor,Contractor_Detail


contractor = Blueprint('contractor', __name__)

# @contractor.route("/contractor/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('contractor/dashboard.html')


@contractor.route("/formcontractor/<int:user_id>", methods=["GET", "POST"])
def formcontractor(user_id):
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

        new_detail=CRUDMixin.create(Contractor,user_id=user_id,name=name,logo='logo', status='active')
        new_detail=CRUDMixin.create(Contractor_Detail,name=name,phone=phoneNumber,address=address,employees=5,are_they_tracking_refrigerant="yes",time_basis='True')
    #redirect to the appropriate page

        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("contractor/formcontractor.html",user_id=user_id)

@contractor.route("/dashboardcontractor")
def dashboardcontractor():
    # Render the dashboard
    return render_template("contractor/dashboardcontractor.html")

@contractor.route('/handle_qr_code', methods=['POST'])
def handle_qr_code():
    data = request.get_json()
    qr_code_text = data['qrCode']
    print("QR Code Text: ", qr_code_text)
    # You can handle the QR code text here as needed

    # Return a response
    return jsonify({'message': 'QR code received successfully.'}), 200
