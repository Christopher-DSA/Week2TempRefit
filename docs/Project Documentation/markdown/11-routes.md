# Admin Blueprint

The provided code creates an 'admin' blueprint in a Flask web application.

1. The necessary Flask modules and a custom `models` module are imported.
2. The 'admin' blueprint is created using Flask's `Blueprint` function.
3. A route is defined at "/admin" that responds to HTTP GET requests.
4. When the "/admin" route is accessed, the `user_page` function fetches all `User` records from the database.
5. The `user_page` function then renders the 'admin/admin.html' template, passing the fetched User data to it.

# Auth Blueprint

The provided code creates an 'auth' blueprint in a Flask web application, handling user authentication and registration. 

1. The required Flask modules and a custom `models` module are imported. 
2. An 'auth' blueprint is created using Flask's `Blueprint` function.

3. Four routes are defined:

   - The "/" and "/login" routes: These handle both GET and POST requests. When a POST request is sent with a username and password, the application checks if these credentials are correct. If they are, the user is redirected to the home page. Otherwise, an error message is printed.

   - The "/forgot_password" route: This handles both GET and POST requests. When a POST request is sent with an email and a new password, the application searches for a user with the given email. If a user is found, the password is updated.

   - The "/home" route: This handles GET requests and simply renders the home page.

   - The "/register" route: This handles both GET and POST requests. When a POST request is sent with registration details, the application creates a new user with these details and redirects the user to a page based on their user type.

All the routes, except "/home", render a template when a GET request is sent. These templates contain forms where users can enter their details.

# Contractor Blueprint

The provided code creates a 'contractor' blueprint in a Flask web application, handling contractor-specific functionalities. 

1. The required Flask modules and a custom `models` module are imported. 

2. A 'contractor' blueprint is created using Flask's `Blueprint` function.

3. Four routes are defined:

   - The "/formcontractor/<int:user_id>" route: This handles both GET and POST requests. When a POST request is sent with contractor details, the application creates a new contractor and contractor detail record in the database with these details. Then, it redirects the user to the contractor dashboard. When a GET request is sent, it renders the "contractor/formcontractor.html" template.

   - The "/dashboardcontractor" route: This handles GET requests and renders the contractor dashboard via the "contractor/dashboardcontractor.html" template.

   - The "/handle_qr_code" route: This handles POST requests. When a POST request is sent with a JSON object containing a QR code, the application prints the QR code and returns a success message. 

This blueprint essentially allows the application to handle contractor registration, display the contractor dashboard, and process QR codes.


# Technician Blueprint

The provided code creates a 'technician' blueprint in a Flask web application, handling technician-specific functionalities. 

1. The required Flask modules and a custom `models` module are imported. 

2. A 'technician' blueprint is created using Flask's `Blueprint` function.

3. The following routes are defined:

   - The "/formtechnician/<int:user_id>" route: This handles both GET and POST requests. When a POST request is sent with technician details, the application creates a new user detail record in the database with these details and then redirects the user to the technician dashboard. When a GET request is sent, it renders the "technician/formtechnician.html" template.

   - The "/dashboardtechnician" route: This handles GET requests and renders the technician dashboard via the "technician/dashboardtechnician.html" template.

   - The "/equipment/equipment_create" route: This handles GET requests and renders the equipment creation page via the "equipment/equipment_create.html" template.

   - The "/equipment/repair" route: This handles GET requests and renders the repair page via the "equipment/repair.html" template.

   - The "/equipment/recovery" route: This handles GET requests and renders the recovery page via the "equipment/recovery.html" template.

   -  The "New Cylinder/tag-linked" route : This handles GET requests and renders the Add Cylinder tag page via the New Cylinder/tag-linked.html template

   - The "/equipment/repair_ODS_Sheet" route :  This handles GET requests and renders the Repair ODS sheet  page via the "equipment/repair_ODS_Sheet.html" template

   - The "/equipment common/qr-scan" route : This handles GET requests and renders the  QR scan page via the "equipment common/qr-scan.html" template
   
   - The "/recovery/recovery-ods-sheet" route : This handles GET requests and renders the Recovery ODS sheet  page via the "/recovery/recovery-ods-sheet.html" template

   - The "/equipment/equipment_pages" route : This handles GET requests and renders the Equipment  page  with 4 options - via the "equipment/equipment_pages.html" template

   - The "/equipment/ODS-history" route : This handles GET requests and renders the ODS history page  via the "/equipment/ODS-history.html" template
    
   - The "/equipment/maintenance_history" route : This handles GET requests and renders the Maintenance history page  via the "/equipment/maintenance_history.html" template
   

This blueprint essentially allows the application to handle technician registration, display the technician dashboard, and manage equipment-related activities such as creation, repair, and recovery.


# Wholesaler Blueprint

The provided code creates a 'wholesaler' blueprint in a Flask web application, handling wholesaler-specific functionalities.

1. The required Flask modules are imported. 

2. A 'wholesaler' blueprint is created using Flask's `Blueprint` function.

3. The following routes are defined:

   - The "/formwholesaler" route: This handles both GET and POST requests. When a POST request is sent with wholesaler details, these details are retrieved from the form data and then flashed as a success message. The user is then redirected to the wholesaler dashboard. When a GET request is sent, it renders the "wholesaler/formwholesaler.html" template.

   - The "/dashboardwholesaler" route: This handles GET requests and renders the wholesaler dashboard via the "wholesaler/dashboardwholesaler.html" template.

This blueprint essentially allows the application to handle wholesaler registration and display the wholesaler dashboard.
