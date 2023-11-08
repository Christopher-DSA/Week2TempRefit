# from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
# from decorators.admin_required import admin_required

# from models import CRUD, User, Tracking, Employee, Person
# from utils.otp import check_otp, qr_generator
# from utils.tokenize import generate_hash, generate_password
# from datetime import datetime
# from email_senders import doEmail

# auth = Blueprint('auth', __name__)

# @auth.route("/login", methods=["GET"])
# def login():
#     return render_template("auth/login.html", current_user={})

# @auth.route('/login', methods=['POST'])
# def login_post():
#     useremail = request.form['useremail']
#     password = request.form['password']

#     hashed_password = generate_hash(password, current_app.secret_key)

#     user = CRUD.read(User, False, email=useremail, password=hashed_password)
#     if user is not None:
#         qr_path = qr_generator(useremail)
#         session['qr_path'] = qr_path
#         session['passed_email'] = useremail
#         return redirect(url_for('auth.validate_otp'))
#     else:
#         flash("Your password or username is incorrect. Please try again!")
#         return render_template("auth/login.html", error=True, error_message="Wrong credentials", qr_path=None)

# @auth.route('/login/validate', methods=['GET', 'POST'])
# def validate_otp():
#     user_email = session.get('passed_email', None)
#     if request.method == 'GET':
#         path = session.get('qr_path', None)
#         otp_qr_path=f'qrcodes/{path}'
#         return render_template("auth/login_validate.html", qr_path=otp_qr_path)
#     elif request.method == 'POST':
#         otp_value = request.form['otp']

#         if check_otp(otp_value):
#             user = CRUD.read(User, False, email = user_email)
#             ip_address = request.remote_addr
#             access_token = create_access_token(identity=user.email, additional_claims= { 'role': user.role })
#             refresh_token = create_refresh_token(identity=user_email, additional_claims= { 'role': user.role })
#             CRUD.create(Tracking,False,
#                         entry_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                         user_code = user.ID,
#                         ip_address = ip_address)
#             if (user.role == 'Company'):
#                 response = make_response(redirect(url_for('company.dashboard')))
#             elif (user.role == 'Admin'):
#                 response = make_response(redirect(url_for('admin.dashboard', company_id = 1)))
#             elif (user.role == 'User'):
#                 response = make_response(redirect(url_for('employee.dashboard')))

#             set_access_cookies(response, access_token)
#             set_refresh_cookies(response, refresh_token)
#             return response
#         else:
#             return render_template("auth/login.html", error=True, error_message="Invalid OTP provided", qr_path=None)


# @auth.route('/logout') # it is working
# @jwt_required()
# def logout():
#     response = make_response(redirect(url_for('auth.login')))
#     unset_jwt_cookies(response)
#     return response


# @auth.route('/refresh', methods=['POST'])
# def refresh():
#     refresh_token = request.cookies.get('refresh_token')
#     if not refresh_token:
#         return jsonify({'message': 'Refresh token is missing'}), 401
#     try:
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity=current_user)
#         resp = jsonify({'message': 'Access token has been refreshed'})
#         set_access_cookies(resp, access_token)
#         return resp, 200
#     except:
#         return jsonify({'message': 'Invalid refresh token'}), 401

# @auth.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#   if request.method == 'GET':
#     return render_template("auth/send_verification_code_form.html", current_user={})
#   elif request.method == 'POST':
#     useremail = request.form['user_email']
#     user = CRUD.read(User, False, email=useremail)
#     if user is not None:
#         employee = CRUD.read(Employee, False, user_code = user.ID)
#         person = CRUD.read(Person, False, ID = employee.person_code)
#         recipient_email = useremail
#         verfi_code = generate_password()
#         message = f'Hi {person.name.title()} {person.last_name.title()}, \n\nThis is the verification code for resetting your password: {verfi_code}. Please do not send it to other people! \n\nThanks, \nMed-I-Well Team'
#         subject = 'Verification Code!'
#         result = doEmail(recipient_email, subject, message)
#         flash(result)
#         # message.html = render_template('email_template/verifi_code.html', name=name, verfi_code=verfi_code)
#         return redirect(url_for('auth.reset_password',verfi_code=verfi_code, email=useremail))
#     else:
#         flash('Please enater a valid email account. Account not found!')
#         return redirect(url_for('auth.forgot_password'))


# @auth.route('/reset_password/<verfi_code>/<email>', methods=['GET','POST'])
# def reset_password(verfi_code, email):
#     if request.method == 'GET':
#         return render_template("auth/forgot_password_form.html", verfi_code=verfi_code, email=email)
#     elif request.method == 'POST':
#         veri_code = request.form.get('veri_code')
#         new_pwd = request.form.get('new_pwd')
#         conf_new_pwd = request.form.get('conf_new_pwd')
#         hashed_password = generate_hash(new_pwd, current_app.config['SECRET_KEY'])
#         if veri_code == verfi_code:
#             useremail = email
#             user = CRUD.read(User, False, email=useremail)
#             if user is not None:
#                 CRUD.update(User, 'password', hashed_password, ID=user.ID)
#                 flash('Your password has been updated successfully!')
#                 return redirect(url_for('auth.login'))
#             else:
#                 flash('The account does not exist. Please try again!')
#                 return redirect(url_for('auth.login'))
#         else:
#             flash('Your verification code was wrong. Please try again!')
#             redirect(url_for('auth.login'))
#     # there should be a link that directs user to the mediwell portal
#     # that has the form to reset their password
#     # the reset url should have a token that could identify that the right email (credential) is reset
