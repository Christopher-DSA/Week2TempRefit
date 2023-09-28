# Possible problems:  , or " " or data type or the order
# 1. psycopg2.errors.UndefinedTable: relation "Repairs" does not exist (Order matters)
# 2. psycopg2.errors.UndefinedObject: type "datetime" does not exist
#    LINE 7: last_updated DATETIME, (change it to TEXT)

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
        user_id SERIAL PRIMARY KEY, 
        email TEXT,
        password TEXT,
        role TEXT,
        added_date TEXT NULL,
        user_detail TEXT NULL NULL,
        status TEXT NULL
    )
''')

# Create the "User_Detail" table
cursor.execute('''
    CREATE TABLE "User_Detail" (
        user_detail_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        first_name TEXT NULL,
        middle_name TEXT NULL,
        last_name TEXT NULL,
        address TEXT NULL,
        province TEXT NULL,
        city TEXT NULL,
        postal_code TEXT NULL,
        telephone TEXT NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE "Refrigerant" (
        refrigerant_id SERIAL PRIMARY KEY,
        refrigerant_name TEXT NULL,
        list TEXT NULL
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE "Contractor" (
        contractor_id SERIAL PRIMARY KEY,
        name TEXT NULL,
        user_id INTEGER,
        logo TEXT NULL,
        status TEXT NULL,
        subscription_id INTEGER NULL,
        code_2fa_code TEXT NULL,
        employees INTEGER NULL,
        are_they_tracking_refrigerant TEXT NULL,
        time_basis TEXT NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')
               
# Create the "Technician" table
cursor.execute('''
    CREATE TABLE "Technician" (
        technician_id SERIAL PRIMARY KEY,
        ODS_licence_number TEXT,
        user_id INTEGER,
        contractor_id INTEGER NULL,
        date_begin TEXT NULL,
        date_end TEXT NULL,
        user_status TEXT NULL,
        contractor_status TEXT NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id),
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id)
    )
''')

# Create the "Admin" table
cursor.execute('''
    CREATE TABLE "Admin" (
        admin_id SERIAL PRIMARY KEY,
        name TEXT NULL,
        user_id INTEGER,
        status TEXT NULL,
        code_2fa_code TEXT NULL,
        admin_level INTEGER NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Subscription" table
cursor.execute('''
    CREATE TABLE "Subscription" (
        subscription_id SERIAL PRIMARY KEY,
        start_date TEXT,
        end_Date TEXT,
        package_size TEXT,
        compliant TEXT NULL
    )
''')

#create "Cylinder_Type" table
cursor.execute('''
    CREATE TABLE "Cylinder_Type" (
        cylinder_type_id SERIAL PRIMARY KEY,
        type_name TEXT
    )
''')

# Create the "Cylinder" table
cursor.execute('''
    CREATE TABLE "Cylinder" (
        cylinder_id SERIAL PRIMARY KEY,
        cylinder_size TEXT NULL,
        cylinder_type_id INTEGER NULL,
        cylinder_weight TEXT NULL,
        added_date TEXT NULL,
        refrigerant_id INTEGER NULL,
        technician_id INTEGER NULL,
        purchase_date TEXT NULL,
        supplier TEXT NULL,
        last_refill_date TEXT NULL,
        condition TEXT NULL,
        FOREIGN KEY (refrigerant_id) REFERENCES "Refrigerant"(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (cylinder_type_id) REFERENCES "Cylinder_Type"(cylinder_type_id)
    )
''')

# Create the "Wholesaler" table
cursor.execute('''
    CREATE TABLE "Wholesaler" (
        wholesaler_id SERIAL PRIMARY KEY,
        name TEXT NULL,
        user_id INTEGER,
        status TEXT NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Invoice" table
cursor.execute('''
    CREATE TABLE "Invoice" (
        invoice_id SERIAL PRIMARY KEY,
        subscription_id INTEGER NULL,
        amount REAL NULL,
        payment_method TEXT NULL,
        tax REAL NULL,
        date TEXT NULL,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id)
    )
''')

# Create the "Tag" table
cursor.execute('''
    CREATE TABLE "Tag" (
        tag_id SERIAL PRIMARY KEY,
        tag_number TEXT NULL,
        tag_url TEXT NULL,
        type TEXT NULL,
        cylinder_id INTEGER NULL,
        wholesaler_id INTEGER NULL,
        invoice_id INTEGER NULL,
        FOREIGN KEY (cylinder_id) REFERENCES "Cylinder"(cylinder_id),
        FOREIGN KEY (wholesaler_id) REFERENCES "Wholesaler"(wholesaler_id),
        FOREIGN KEY (invoice_id) REFERENCES "Invoice"(invoice_id)
    )
''')



# Create the "Organization/Group" table
cursor.execute('''
    CREATE TABLE "Organization" (
        organization_id SERIAL PRIMARY KEY,
        name TEXT NULL,
        user_id INTEGER,
        logo TEXT NULL,
        status TEXT NULL,
        subscription_id INTEGER NULL,
        code_2fa_code TEXT NULL,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE "Store" (
        store_id SERIAL PRIMARY KEY,
        organization_id INTEGER NULL,
        branch TEXT NULL,
        name TEXT NULL,
        user_id INTEGER,
        address TEXT NULL,
        gps_location TEXT NULL,
        FOREIGN KEY (organization_id) REFERENCES "Organization"(organization_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Unit" table
cursor.execute('''
    CREATE TABLE "Unit" (
        unit_id SERIAL PRIMARY KEY,
        technician_id INTEGER NULL,
        unit_name TEXT NULL,
        tag_id INTEGER NULL,
        other_attribute TEXT NULL,
        installation_date TEXT NULL,
        last_maintenance_date TEXT NULL,
        manufacturer TEXT NULL,
        model TEXT NULL,
        type_of_refrigerant TEXT NULL,
        factory_charge_amount INTEGER NULL,
        unit_type TEXT NULL,
        store_id INTEGER NULL,
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (tag_id) REFERENCES "Tag"(tag_id),
        FOREIGN KEY (store_id) REFERENCES "Store"(store_id)
    )
''')

# Create the "User_Logging" table
cursor.execute('''
    CREATE TABLE "User_Logging" (
        log_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        entry_date TEXT NULL,
        ip_address TEXT NULL,
        address_gps TEXT NULL,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Purchase" table
cursor.execute('''
    CREATE TABLE "Purchase" (
        purchase_id SERIAL PRIMARY KEY
    )
''')

# Create the "Tank" table
cursor.execute('''
    CREATE TABLE "Tank" (
        tank_id SERIAL PRIMARY KEY
    )
''')

# Create the "Reclaim/Recovery" table
cursor.execute('''
    CREATE TABLE "Reclaim_Recovery" (
        rec_id SERIAL PRIMARY KEY,
        purchase_id INTEGER NULL,
        tank_id INTEGER NULL,
        unit_id INTEGER NULL,    
        gas_type TEXT NULL,
        quantity_before_in_lbs REAL NULL,
        quantity_after_in_lbs REAL NULL,
        technician_id INTEGER NULL,
        notes TEXT NULL,
        date TEXT NULL,
        status TEXT NULL,
        refrigerant_id INTEGER NULL,
        cylinder_id INTEGER NULL,
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
        repair_id SERIAL PRIMARY KEY,
        unit_id INTEGER NULL,
        purchase_id INTEGER NULL,
        repair_date TEXT NULL,
        technician_id INTEGER NULL,
        causes TEXT NULL,
        status TEXT NULL,
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (purchase_id) REFERENCES "Purchase"(purchase_id)
    )
''')

# Create the "ODS_Sheet" table
cursor.execute('''
    CREATE TABLE "ODS_Sheet" (
        ods_id SERIAL PRIMARY KEY,
        contractor_id INTEGER NULL,
        technician_id INTEGER NULL,
        unit_id INTEGER NULL,
        tag_id INTEGER NULL,
        repair_id INTEGER NULL,
        rec_id INTEGER NULL,
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
        technician_offer_id SERIAL PRIMARY KEY,
        contractor_id INTEGER NULL,
        technician_id INTEGER NULL,
        offer_status TEXT NULL,
        email_time_sent TEXT NULL,
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id)
    )
''')

# Create the "Store_Location" table
cursor.execute('''
    CREATE TABLE "Store_Location" (
        store_location_id SERIAL PRIMARY KEY,
        store_id INTEGER NULL,
        gps_location TEXT NULL,
        FOREIGN KEY (store_id) REFERENCES "Store"(store_id)
    )
''')

#create "Maintenance" table            
cursor.execute('''
    CREATE TABLE "Maintenance" (
        maintenance_id SERIAL PRIMARY KEY,
        technician_id INTEGER NULL,
        unit_id INTEGER NULL,
        log TEXT NULL,
        last_updated TEXT NULL,
        service_history TEXT NULL,
        maintenance_date TEXT NULL,
        maintenance_type VARCHAR(50) NULL,
        parts_used TEXT NULL,
        notes TEXT NULL,
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id)
    )
''')

#create "Maintenance_Detail" table               
cursor.execute('''
    CREATE TABLE "Maintenance_Detail" (
        maintenance_detail_id SERIAL PRIMARY KEY,
        maintenance_id INTEGER NULL,
        description TEXT NULL,
        status VARCHAR(50) NULL,
        FOREIGN KEY (maintenance_id) REFERENCES "Maintenance"(maintenance_id)
    )
''')
               





# Commit the changes and close the connection
conn.commit()
conn.close()
