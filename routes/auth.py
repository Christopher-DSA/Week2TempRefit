from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
# from models import User, get_session
from models import User,get_session, CRUDMixin
auth = Blueprint('auth', __name__)

# Hard-coded user data
users = {'admin': 'admin'}

@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            # just a placeholder - replace with  logic to check if user exists in database
            if username == 'admin' and password == 'password':
                return redirect(url_for('auth.home'))
            else:
                print('Invalid username or password')
    return render_template("auth/login.html")




@auth.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('username')
        new_password = request.form.get('new_password')
        
        if email and new_password:
            # Use a query to find the user by email
            
            # user = CRUDMixin.get_user_by_email(email)
            users = CRUDMixin.read(User, email=email)
           
            if users:
                user=users[0]
                
            #     # Use the CRUDMixin update method to change the password
                updated_user = CRUDMixin.update(User, user.user_id, password=new_password)
                return jsonify({'message': 'Password changed successfully'})
            else:
                return jsonify({'error': 'User not found'})

    return render_template("auth/forgot_password.html")



@auth.route("/home", methods=["GET"])
def home():
    return render_template("auth/home.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        license = request.form['license']
        if not username or not password or not user_type:
            flash('Please fill out all fields.')
        elif user_type == 'technician' and not license:
            flash('Technicians must enter a license number.')
        else:
            print('Registered successfully.')

            new_user = CRUDMixin.create(User, email=username, password=password, role=user_type, added_date=license)

            users = CRUDMixin.read(User, email=username)            

            new_userid=(users[0].user_id)

            # Redirect to different forms based on user_type
            if user_type == 'contractor':
                return redirect(url_for('contractor.formcontractor',user_id=new_userid))
            elif user_type == 'technician':
                return redirect(url_for('technician.formtechnician',user_id=new_userid))
            elif user_type == 'wholesaler':
                return redirect(url_for('wholesaler.formwholesaler'))
            elif user_type == 'admin':
                return redirect(url_for('auth.formadmin'))
            
            #return redirect(url_for('auth.login'))
    print("******************************* failed to Register ********************************")   
    return render_template("auth/register.html")



