from flask import make_response, session, Blueprint
from flask import (
    Flask,
    render_template,
    redirect,
    current_app,
    url_for,
    flash,
    make_response,
    request,
)
from functools import wraps
from models import Technician, User, CRUD, User_Detail

wholesaler = Blueprint("wholesaler", __name__)


# @wholesaler.route("/wholesaler/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('wholesaler/dashboard.html')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def wholesaler_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming the user_id in the session is the email of the user.
        email = session.get("user_id")

        user = User.get_user_by_email(email)

        if not user or user.role != "wholesaler":
            # Either user doesn't exist, or the user is not an admin.
            return "Unauthorized", 403

        return f(*args, **kwargs)

    return decorated_function


@wholesaler.route("/formwholesaler", methods=["GET", "POST"])
def formwholesaler():
    if request.method == "POST":
        # Get data from form
        name = request.form.get("name")
        companyName = request.form.get("companyName")
        branch = request.form.get("branch")
        mailingAddress = request.form.get("mailingAddress")
        mailingCity = request.form.get("mailingCity")
        mailingProvince = request.form.get("mailingProvince")
        mailingPostalCode = request.form.get("mailingPostalCode")
        billingAddress = request.form.get("billingAddress")
        billingCity = request.form.get("billingCity")
        billingProvince = request.form.get("billingProvince")
        billingPostalCode = request.form.get("billingPostalCode")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        addressLine = request.form.get("addressLine")
        province = request.form.get("province")
        city = request.form.get("city")
        postalCode = request.form.get("postalCode")
        odsLicenseNumber = request.form.get("odsLicenseNumber")
        phoneNumber = request.form.get("phoneNumber")

        # TODO: Validate the data

        # TODO: Pass data to database

        new_detail = CRUD.create(
            User_Detail,
            user_id=session.get("user_id"),
            first_name=firstName,
            last_name=lastName,
            address=addressLine,
            province=province,
            city=city,
            postal_code=postalCode,
            telephone=phoneNumber,
        )
        new_technician_detail = CRUD.create(
            Technician,
            ODS_licence_number=odsLicenseNumber,
            user_id=session.get("user_id"),
        )
        return redirect(url_for("technician.dashboardtechnician"))
        # create_wholesaler(name, email, password, companyName, branch,
        #    mailingAddress, mailingCity, mailingProvince, mailingPostalCode,
        #    billingAddress, billingCity, billingProvince, billingPostalCode, phoneNumber)

        flash("Registered successfully.")
        return redirect(url_for("wholesaler.dashboardwholesaler"))

    return render_template("wholesaler/formwholesaler.html")


@wholesaler.route("/dashboardwholesaler")
@login_required
@wholesaler_required
def dashboardwholesaler():
    # Render the dashboard
    return render_template("wholesaler/dashboardwholesaler.html")
