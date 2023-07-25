from flask import Blueprint, flash, current_app, jsonify, make_response, redirect, render_template, request, url_for, session



contractor = Blueprint('contractor', __name__)

# @contractor.route("/contractor/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     return render_template('contractor/dashboard.html')


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

    #redirect to the appropriate page

        return redirect(url_for('contractor.dashboardcontractor'))
    return render_template("contractor/formcontractor.html")

@contractor.route("/dashboardcontractor")
def dashboardcontractor():
    # Render the dashboard
    return render_template("contractor/dashboardcontractor.html")

