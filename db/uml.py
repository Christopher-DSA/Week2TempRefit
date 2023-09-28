# Possible problems: , or " " or data type or the order
# 1. psycopg2.errors.UndefinedTable: relation "Repairs" does not exist (Order matters)
# 2. psycopg2.errors.UndefinedObject: type "datetime" does not exist
#    LINE 7: last_updated DATETIME, (change it to String)

# What is this file for? 
# Modify this file to manage the db

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get database connection information from environment variables
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database=database_name,
    user=database_user,
    password=database_password,
    host=database_host,
    port=database_port
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Drop the tables if they already exist

cursor.execute('DROP TABLE IF EXISTS "User"')
cursor.execute('DROP TABLE IF EXISTS "Contractor"')
cursor.execute('DROP TABLE IF EXISTS "Technician"')
cursor.execute('DROP TABLE IF EXISTS "Admin"')
cursor.execute('DROP TABLE IF EXISTS "Wholesaler"')
cursor.execute('DROP TABLE IF EXISTS "Invoice"')
cursor.execute('DROP TABLE IF EXISTS "Subscription"')
cursor.execute('DROP TABLE IF EXISTS "Tag"')
cursor.execute('DROP TABLE IF EXISTS "User_Logging"')
cursor.execute('DROP TABLE IF EXISTS "User_Detail"')
cursor.execute('DROP TABLE IF EXISTS "Unit"')
cursor.execute('DROP TABLE IF EXISTS "Organization"')
cursor.execute('DROP TABLE IF EXISTS "Store"')
cursor.execute('DROP TABLE IF EXISTS "Store_Location"')
cursor.execute('DROP TABLE IF EXISTS "ODS_Sheet"')
cursor.execute('DROP TABLE IF EXISTS "Technician_Offer"')
cursor.execute('DROP TABLE IF EXISTS "Cylinder"')
cursor.execute('DROP TABLE IF EXISTS "Repair"')
cursor.execute('DROP TABLE IF EXISTS "Reclaim_Recovery"')
cursor.execute('DROP TABLE IF EXISTS "Refrigerant"')
cursor.execute('DROP TABLE IF EXISTS "Maintenance"')
cursor.execute('DROP TABLE IF EXISTS "Maintenance_Detail"')
cursor.execute('DROP TABLE IF EXISTS "Cylinder_Type"')
cursor.execute('DROP TABLE IF EXISTS "Purchase"')
cursor.execute('DROP TABLE IF EXISTS "Tank"')


# Create the "User" table
cursor.execute('''

    CREATE TABLE "User"(
        user_id INTEGER PRIMARY KEY, 
        email TEXT,
        password TEXT,
        role TEXT,
        added_date String,
        user_detail TEXT,
        status TEXT
    )
''')

# Create the "User_Detail" table
cursor.execute('''
    CREATE TABLE "User_Detail" (
        user_detail_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        address TEXT,
        province TEXT,
        city TEXT,
        postal_code TEXT,
        telephone TEXT,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE "Refrigerant" (
        refrigerant_id INTEGER PRIMARY KEY,
        refrigerant_name TEXT,
        list TEXT
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE "Contractor" (
        contractor_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        employees INTEGER,
        are_they_tracking_refrigerant TEXT,
        time_basis TEXT,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')
               
# Create the "Technician" table
cursor.execute('''
    CREATE TABLE "Technician" (
        technician_id INTEGER PRIMARY KEY,
        ODS_licence_number TEXT,
        user_id INTEGER,
        contractor_id INTEGER,
        date_begin String,
        date_end String,
        user_status TEXT,
        contractor_status TEXT,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id),
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id)
    )
''')

# Create the "Admin" table
cursor.execute('''
    CREATE TABLE "Admin" (
        admin_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        code_2fa_code TEXT,
        admin_level INTEGER,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Subscription" table
cursor.execute('''
    CREATE TABLE "Subscription" (
        subscription_id INTEGER PRIMARY KEY,
        start_date String,
        end_Date String,
        package_size TEXT,
        compliant TEXT
    )
''')

#create "Cylinder_Type" table
cursor.execute('''
    CREATE TABLE "Cylinder_Type" (
        cylinder_type_id INTEGER PRIMARY KEY,
        type_name TEXT
    )
''')

# Create the "Cylinder" table
cursor.execute('''
    CREATE TABLE "Cylinder" (
        cylinder_id INTEGER PRIMARY KEY,
        cylinder_size TEXT,
        cylinder_type_id INTEGER,
        cylinder_weight TEXT,
        added_date String,
        refrigerant_id INTEGER,
        technician_id INTEGER,
        purchase_date String,
        supplier TEXT,
        last_refill_date String,
        condition TEXT,
        FOREIGN KEY (refrigerant_id) REFERENCES "Refrigerant"(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (cylinder_type_id) REFERENCES "Cylinder_Type"(cylinder_type_id)
    )
''')

# Create the "Wholesaler" table
cursor.execute('''
    CREATE TABLE "Wholesaler" (
        wholesaler_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Invoice" table
cursor.execute('''
    CREATE TABLE "Invoice" (
        invoice_id INTEGER PRIMARY KEY,
        subscription_id INTEGER,
        amount REAL,
        payment_method TEXT,
        tax REAL,
        date String,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id)
    )
''')

# Create the "Tag" table
cursor.execute('''
    CREATE TABLE "Tag" (
        tag_id INTEGER PRIMARY KEY,
        tag_number TEXT,
        tag_url TEXT,
        type TEXT,
        cylinder_id INTEGER,
        wholesaler_id INTEGER,
        invoice_id INTEGER,
        FOREIGN KEY (cylinder_id) REFERENCES "Cylinder"(cylinder_id),
        FOREIGN KEY (wholesaler_id) REFERENCES "Wholesaler"(wholesaler_id),
        FOREIGN KEY (invoice_id) REFERENCES "Invoice"(invoice_id)
    )
''')



# Create the "Organization/Group" table
cursor.execute('''
    CREATE TABLE "Organization" (
        organization_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE "Store" (
        store_id INTEGER PRIMARY KEY,
        organization_id INTEGER,
        branch TEXT,
        name TEXT,
        user_id INTEGER,
        address TEXT,
        gps_location TEXT,
        FOREIGN KEY (organization_id) REFERENCES "Organization"(organization_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Unit" table
cursor.execute('''
    CREATE TABLE "Unit" (
        unit_id INTEGER PRIMARY KEY,
        technician_id INTEGER,
        unit_name TEXT,
        tag_id INTEGER,
        other_attribute TEXT,
        installation_date String,
        last_maintenance_date String,
        manufacturer TEXT,
        model TEXT,
        type_of_refrigerant TEXT,
        factory_charge_amount INTEGER,
        unit_type TEXT,
        store_id INTEGER,
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (tag_id) REFERENCES "Tag"(tag_id),
        FOREIGN KEY (store_id) REFERENCES "Store"(store_id)
    )
''')

# Create the "User_Logging" table
cursor.execute('''
    CREATE TABLE "User_Logging" (
        log_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        entry_date String,
        ip_address TEXT,
        address_gps TEXT,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Purchase" table
cursor.execute('''
    CREATE TABLE "Purchase" (
        purchase_id INTEGER PRIMARY KEY
    )
''')

# Create the "Tank" table
cursor.execute('''
    CREATE TABLE "Tank" (
        tank_id INTEGER PRIMARY KEY
    )
''')

# Create the "Reclaim/Recovery" table
cursor.execute('''
    CREATE TABLE "Reclaim_Recovery" (
        rec_id INTEGER PRIMARY KEY,
        purchase_id INTEGER,
        tank_id INTEGER,
        unit_id INTEGER,    
        gas_type TEXT,
        quantity_before_in_lbs REAL,
        quantity_after_in_lbs REAL,
        technician_id INTEGER,
        notes TEXT,
        date String,
        status TEXT,
        refrigerant_id INTEGER,
        cylinder_id INTEGER,
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (refrigerant_id) REFERENCES "Refrigerant"(refrigerant_id),
        FOREIGN KEY (cylinder_id) REFERENCES "Cylinder"(cylinder_id),
        FOREIGN KEY (purchase_id) REFERENCES "Purchase"(purchase_id),
        FOREIGN KEY (tank_id) REFERENCES "Tank"(tank_id)
    )
''')

# Create the "Repair" table
cursor.execute('''
    CREATE TABLE "Repair" (
        repair_id INTEGER PRIMARY KEY,
        unit_id INTEGER,
        purchase_id INTEGER,
        repair_date String,
        technician_id INTEGER,
        causes TEXT,
        status TEXT,
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (purchase_id) REFERENCES "Purchase"(purchase_id)
    )
''')

# Create the "ODS_Sheet" table
cursor.execute('''
    CREATE TABLE "ODS_Sheet" (
        ods_id INTEGER PRIMARY KEY,
        contractor_id INTEGER,
        technician_id INTEGER,
        unit_id INTEGER,
        tag_id INTEGER,
        repair_id INTEGER,
        rec_id INTEGER,
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id),
        FOREIGN KEY (repair_id) REFERENCES "Repair"(repair_id),
        FOREIGN KEY (rec_id) REFERENCES  "Reclaim_Recovery"(rec_id),
        FOREIGN KEY (tag_id) REFERENCES "Tag"(tag_id)
    )
''')

# Create the "Technician_Offer" table
cursor.execute('''
    CREATE TABLE "Technician_Offer" (
        technician_offer_id INTEGER PRIMARY KEY,
        contractor_id INTEGER,
        technician_id INTEGER,
        offer_status TEXT,
        email_time_sent TEXT,
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id)
    )
''')

# Create the "Store_Location" table
cursor.execute('''
    CREATE TABLE "Store_Location" (
        store_location_id INTEGER PRIMARY KEY,
        store_id INTEGER,
        gps_location TEXT,
        FOREIGN KEY (store_id) REFERENCES "Store"(store_id)
    )
''')

#create "Maintenance" table            
cursor.execute('''
    CREATE TABLE "Maintenance" (
        maintenance_id INTEGER PRIMARY KEY,
        technician_id INTEGER,
        unit_id INTEGER,
        log TEXT,
        last_updated String,
        service_history TEXT,
        maintenance_date String,
        maintenance_type VARCHAR(50),
        parts_used TEXT,
        notes TEXT,
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id)
    )
''')

#create "Maintenance_Detail" table               
cursor.execute('''
    CREATE TABLE "Maintenance_Detail" (
        maintenance_detail_id INTEGER PRIMARY KEY,
        maintenance_id INTEGER,
        description TEXT,
        status VARCHAR(50),
        FOREIGN KEY (maintenance_id) REFERENCES "Maintenance"(maintenance_id)
    )
''')
               





# Commit the changes and close the connection
conn.commit()
conn.close()
