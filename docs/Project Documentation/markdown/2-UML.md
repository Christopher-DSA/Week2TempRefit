#Refit Database

##Introduction

This database facilitates the storage and organization of critical data. It acts as a repository for user accounts, content, transactions, and various other essential components of the web application. The database empowers your application to handle high volumes of data and concurrent user interactions.
This documentation provides an overview of the SQLite database used for the web application. It explains the purpose and structure of each table created in the database and outlines the relationships between them.


##Dropped TABLES
By dropping the tables before creating them again, it ensures a clean slate for the database. This can be useful when there is a need to reset the database structure. Dropping tables allows you to start fresh by recreating the tables with the desired structure and relationships.


##Tables

###User:
Stores user information for authentication and access control.
Columns:
    user_id (Primary Key): Unique identifier for the user.
    email: User's email address.
    password: User's password.
    role: User's role in the application.
    added_date: Date the user was added to the system.
    user_detail: Additional details about the user.
    status: User's account status (active, inactive, etc.).
    is_email_verified: Whether a user has verified their email address.
    has_ods_license: Whether has a valid ods_license.

###Technician Table
Purpose: Stores information about technicians associated with contractors.
Columns:
    technician_id (Primary Key): Unique identifier for the technician.
    user_detail: Additional details about the technician.
    ods_licence_number = Users ODS Licence number.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    contractor_id: Foreign key referencing the Contractor table to link with the associated contractor.
    date_begin: Start date of the technician's association with the contractor.
    date_end: End date of the technician's association with the contractor.
    user_status: Status of the technician's user account.
    contractor_status: Status of the technician's association with the contractor.

###Contractor Table
Purpose: Stores information about contractors associated with the application.
Columns:
    contractor_id (Primary Key): Unique identifier for the contractor.
    name: Contractor's name.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    logo: Path or URL to the contractor's logo.
    status: Contractor's status.
    subscription_id: Foreign key referencing the Subscription table to link with the associated subscription.
    code_2fa_code: Two-factor authentication code for the contractor's account.
    employees: Associated employees
    are_they_tracking_refrigerant: Whether or not they are tracking refrigerant in the REFit system.
    time_basis: Basis of time calculation for the contractor (hourly, daily, etc.).
    companyName: The name of the contractor's company
    branchId: ???

###Refit_admin Table
Purpose: Stores information about administrators associated with the application.
Columns:
    admin_id (Primary Key): Unique identifier for the admin.
    name: Admin's name.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    status: Admin's status.
    code_2fa_code: Two-factor authentication code for the admin's account.
    admin_level: Level of administrative access.

###Wholesaler Table
Purpose: Stores information about the associated wholesalers.
Columns:
    wholesaler_id (Primary Key): Unique identifier for the wholesaler.
    name: Wholesaler's name.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    status: Wholesaler's status.

###Invoice Table
Purpose: Stores invoice information related to subscriptions and tags.
Columns:
    invoice_id (Primary Key): Unique identifier for the invoice.
    subscription_id: Foreign key referencing the Subscription table to link with the associated subscription.
    amount: Invoice amount.
    payment_method: Payment method used.
    tax: Tax amount.
    date: Date of the invoice.

###Subscription Table
Purpose: Stores information about subscriptions.
Columns:
    subscription_id (Primary Key): Unique identifier for the subscription.
    Start_date: Start date of the subscription.
    End_Date: End date of the subscription.
    Package_size: Size of the subscription package.
    compliant: Indicates if the subscription is compliant.

###Tags Table
Purpose: Stores information about tags associated with cylinders, and units.
Columns:
    tag_id (Primary Key): Unique identifier for the tag.
    tag_number: Tag number or identifier.
    tag_url: URL or path associated with the tag.
    type: Type of the tag.
    cylinder_id: Foreign key referencing the Cylinder table to link with associated cylinders.
    wholesaler_id: Foreign key referencing the Wholesaler table to link with associated wholesaler who sold the tag.
    invoice_id: Foreign key referencing the Invoice table. 

###USER LOGGING Table
Purpose: Stores logging information for user activities.
Columns:
    log_id (Primary Key): Unique identifier for the log entry.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    entry_date: Date and time of the user activity.
    ip_address: IP address of the user.
    address_gps: GPS coordinates of the user's location.


###User_detail Table
Purpose: Stores additional details about users.
Columns:
    user_detail_id (Primary Key): Unique identifer for the user_detail.
    user_id: Foreign Key referencing the Unique identifier for the user.
    first_name: User's first name.
    middle_name: User's middle name.
    last_name: User's last name.
    birthdate: User's date of birth. # Is not yet in the database.
    gender: User's gender. # Is not yet in the database.
    address: User's address.
    province: User's province.
    city: User's city.
    postal_code: User's postal code.
    telephone: User's telephone number.

###Unit Table
Purpose: Stores information about units that are on record.
Columns:
    unit_id (Primary Key): Unique identifier for the unit.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    unit_name: Name or identifier of the unit.
    address: Address of the unit.
    province: Province of the unit.
    city: City of the unit.
    postal_code: Postal code of the unit.
    telephone: Telephone number of the unit.
    tag_id: Foreign key referencing the Tags table to link with associated tags.
    other_attribute: Other attribute related to the unit.
    installation_date: Date of unit installation.
    last_maintenance_date: Date of the last maintenance performed on the unit.
    manufacturer: Manufacturer of the unit.
    model: Model of the unit.
    type_of_refrigerant: Type of refrigerant used in the unit.
    factory_charge_amount: Amount of refrigerant initially charged in the unit.
    unit_type: Type of the unit.
    store_id: Foreign key referencing the Store table to link with the associated store.


Organizations Table
Purpose: Stores information about organizations/clients(of the contractor).
Columns:
    organization_id (Primary Key): Unique identifier for the organization.
    name: Name of the organization.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    logo: Path or URL to the organization's logo.
    status: Organization's status (active, inactive, etc.).
    subscription_id: Foreign key referencing the Subscription table to link with the associated subscription.
    code_2fa_code: Two-factor authentication code for the organization's account.

Store Table
Purpose: Stores information about stores associated which are under the organizations(clients[of the contractor]).
Columns:
    store_id (Primary Key): Unique identifier for the store.
    organization_id: Foreign key referencing the Organizations table to link with the associated organization.
    branch: Store's branch information.
    name: Store's name.
    user_id: Foreign key referencing the User table to link with the corresponding user.
    address: Store's address.

Store_locations Table
Purpose: Stores GPS locations for stores.
Columns:
    store_id (Primary Key): Unique identifier for the store.
    gps_location: GPS coordinates of the store.

ODS_Sheets Table
Purpose: Stores information about (ODS) sheets associated with various entries.
Columns:
    ods_id (Primary Key): Unique identifier for the ODS sheet.
    contractor_id: Foreign key referencing the Contractor table to link with the associated contractor.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    unit_id: Foreign key referencing the Unit table to link with the associated unit.
    tag_id: Foreign key referencing the Tags table to link with associated tags.
    repair_id: Foreign key referencing the Repairs table to link with the associated repair.
    rec_id: Foreign key referencing the Reclaim_Recovery table to link with the associated reclaim/recovery.


technician_offer Table
Purpose: Stores information about offers made to technicians by contractors.
Columns:
    contractor_id: Foreign key referencing the Contractor table to link with the associated contractor.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    offer_status: Status of the offer made.
    email_time_sent: Date and time when the offer email was sent.

Cylinder Table
Purpose: Stores information about cylinders associated that are tagged.
Columns:
    cylinder_id (Primary Key): Unique identifier for the cylinder.
    cylinder_size: Size of the cylinder.
    cylinder_type: Type of the cylinder.
    cylinder_weight: Weight of the cylinder.
    added_date: Date the cylinder was added.
    refrigerant_id: Foreign key referencing the Refrigerant table to link with the associated refrigerant.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    purchase_date: Date of cylinder purchase.
    supplier: Supplier of the cylinder.
    last_refill_date: Date of the last refill performed on the cylinder.
    condition: Condition of the cylinder.
    tag_id: Foreign key referencing the Tags table to link with associated tags.

Repairs Table
Purpose: Stores information about repairs performed on units.
Columns:
    repair_id (Primary Key): Unique identifier for the repair.
    unit_id: Foreign key referencing the Unit table to link with the associated unit.
    purchase_id: Foreign key referencing the Purchase table to link with the associated purchase.
    repair_date: Date of the repair.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    causes: Causes of the repair.
    status: Status of the repair.


Reclaim_Recovery Table
Purpose: Stores information about reclaim and recovery actions performed on refrigerants.
Columns:
    rec_id (Primary Key): Unique identifier for the reclaim/recovery.
    purchase_id: Foreign key referencing the Purchase table to link with the associated purchase.
    tank_id: Foreign key referencing the Tank table to link with the associated tank.
    unit_id: Foreign key referencing the Unit table to link with the associated unit.
    gas_type: Type of gas reclaimed or recovered.
    quantity_before_in_lbs: Quantity of gas before the reclaim/recovery process in pounds.
    quantity_after_in_lbs: Quantity of gas after the reclaim/recovery process in pounds.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    notes: Additional notes about the reclaim/recovery.
    date: Date of the reclaim/recovery.
    status: Status of the reclaim/recovery.
    refrigerant_id: Foreign key referencing the Refrigerant table to link with the associated refrigerant.
    cylinder_id: Foreign key referencing the Cylinder table to link with the associated cylinder.

Refrigerant Table
Purpose: Stores information about refrigerants.
Columns:
    refrigerant_id (Primary Key): Unique identifier for the refrigerant.
    refrigerant_name: Name of the refrigerant.
    list: Additional information about the refrigerant.

Maintenance Table
Purpose: Stores information about maintenance activities performed on units.
Columns:
    maintenance_id (Primary Key): Unique identifier for the maintenance activity.
    technician_id: Foreign key referencing the Technician table to link with the associated technician.
    unit_id: Foreign key referencing the Unit table to link with the associated unit.
    log: Log of maintenance activity.
    last_updated: Date and time of the last update to the maintenance record.
    service_history: History of maintenance services performed.
    maintenance_date: Date of the maintenance activity.
    maintenance_type: Type of the maintenance activity.
    parts_used: Parts used during the maintenance activity.
    notes: Additional notes about the maintenance activity.

Maintenance_detail Table
Purpose: Stores detailed information about individual maintenance activities.
Columns:
    maintenance_detail_id (Primary Key): Unique identifier for the maintenance detail.
    maintenance_id: Foreign key referencing the Maintenance table to link with the associated maintenance activity.
    description: Description of the maintenance detail.
    status: Status of the maintenance detail.


##ERD Diagram
    After the program is run, and the database is created, the UML diagram is created using DBeaver database tool. 
    Connect to the database (database.db)
    Right-click on the connected database on left-panel.
    Click on view diagram. 


# This table no longer exists in the database.
###Contractor_Detail Table
Purpose: Stores additional details about contractors.
Columns:
    contractor_id (Primary Key): Unique identifier for the contractor.
    name: Contractor's name.
    phone: Contractor's phone number.
    address: Contractor's address.
    employees: Number of employees working for the contractor.
    are_they_tracking_refrigerant: Indicates if the contractor tracks refrigerant.
    time_basis: Basis of time calculation for the contractor (hourly, daily, etc.).

# Old documentation for Invoice Table. There have been changes.
###Invoice Table
Purpose: Stores invoice information related to subscriptions and tags.
Columns:
    invoice_id (Primary Key): Unique identifier for the invoice.
    subscription_id: Foreign key referencing the Subscription table to link with the associated subscription.
    tag_id: Foreign key referencing the Tags table to link with the associated tag.
    amount: Invoice amount.
    payment_method: Payment method used.
    tax: Tax amount.
    date: Date of the invoice.