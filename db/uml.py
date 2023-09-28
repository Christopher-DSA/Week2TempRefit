# Possible problems:  , or " " or data type or the order
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
        user_id SERIAL PRIMARY KEY, 
        email TEXT,
        password TEXT,
        role TEXT,
        added_date String Null,
        user_detail TEXT NULL Null,
        status TEXT NULL
    )
''')

# Create the "User_Detail" table
cursor.execute('''
    CREATE TABLE "User_Detail" (
        user_detail_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        first_name TEXT Null,
        middle_name TEXT Null,
        last_name TEXT Null,
        address TEXT Null,
        province TEXT NULL Null,
        city TEXT NULL Null,
        postal_code TEXT NULL Null,
        telephone TEXT NULL Null,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE "Refrigerant" (
        refrigerant_id SERIAL PRIMARY KEY,
        refrigerant_name TEXT Null,
        list TEXT Null
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE "Contractor" (
        contractor_id SERIAL PRIMARY KEY,
        name TEXT Null,
        user_id INTEGER,
        logo TEXT Null,
        status TEXT Null,
        subscription_id INTEGER Null,
        code_2fa_code TEXT Null,
        employees INTEGER Null,
        are_they_tracking_refrigerant TEXT Null,
        time_basis TEXT Null,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')
               
# Create the "Technician" table
cursor.execute('''
    CREATE TABLE "Technician" (
        technician_id SERIAL PRIMARY KEY,
        ODS_licence_number TEXT,
        user_id INTEGER,
        contractor_id INTEGER Null,
        date_begin String Null,
        date_end String Null,
        user_status TEXT Null,
        contractor_status TEXT Null,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id),
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id)
    )
''')

# Create the "Admin" table
cursor.execute('''
    CREATE TABLE "Admin" (
        admin_id SERIAL PRIMARY KEY,
        name TEXT Null,
        user_id INTEGER,
        status TEXT Null,
        code_2fa_code TEXT Null,
        admin_level INTEGER Null,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Subscription" table
cursor.execute('''
    CREATE TABLE "Subscription" (
        subscription_id SERIAL PRIMARY KEY,
        start_date String,
        end_Date String,
        package_size TEXT,
        compliant TEXT Null
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
        cylinder_size TEXT Null,
        cylinder_type_id INTEGER Null,
        cylinder_weight TEXT Null,
        added_date String Null,
        refrigerant_id INTEGER Null,
        technician_id INTEGER Null,
        purchase_date String Null,
        supplier TEXT Null,
        last_refill_date String Null,
        condition TEXT Null,
        FOREIGN KEY (refrigerant_id) REFERENCES "Refrigerant"(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (cylinder_type_id) REFERENCES "Cylinder_Type"(cylinder_type_id)
    )
''')

# Create the "Wholesaler" table
cursor.execute('''
    CREATE TABLE "Wholesaler" (
        wholesaler_id SERIAL PRIMARY KEY,
        name TEXT Null,
        user_id INTEGER,
        status TEXT Null,
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Invoice" table
cursor.execute('''
    CREATE TABLE "Invoice" (
        invoice_id SERIAL PRIMARY KEY,
        subscription_id INTEGER Null,
        amount REAL Null,
        payment_method TEXT Null,
        tax REAL Null,
        date String Null,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id)
    )
''')

# Create the "Tag" table
cursor.execute('''
    CREATE TABLE "Tag" (
        tag_id SERIAL PRIMARY KEY,
        tag_number TEXT Null,
        tag_url TEXT Null,
        type TEXT Null,
        cylinder_id INTEGER Null,
        wholesaler_id INTEGER Null,
        invoice_id INTEGER Null,
        FOREIGN KEY (cylinder_id) REFERENCES "Cylinder"(cylinder_id),
        FOREIGN KEY (wholesaler_id) REFERENCES "Wholesaler"(wholesaler_id),
        FOREIGN KEY (invoice_id) REFERENCES "Invoice"(invoice_id)
    )
''')



# Create the "Organization/Group" table
cursor.execute('''
    CREATE TABLE "Organization" (
        organization_id SERIAL PRIMARY KEY,
        name TEXT Null,
        user_id INTEGER,
        logo TEXT Null,
        status TEXT Null,
        subscription_id INTEGER Null,
        code_2fa_code TEXT Null,
        FOREIGN KEY (subscription_id) REFERENCES "Subscription"(subscription_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE "Store" (
        store_id SERIAL PRIMARY KEY,
        organization_id INTEGER Null,
        branch TEXT Null,
        name TEXT Null,
        user_id INTEGER,
        address TEXT Null,
        gps_location TEXT Null,
        FOREIGN KEY (organization_id) REFERENCES "Organization"(organization_id),
        FOREIGN KEY (user_id) REFERENCES "User"(user_id)
    )
''')

# Create the "Unit" table
cursor.execute('''
    CREATE TABLE "Unit" (
        unit_id SERIAL PRIMARY KEY,
        technician_id INTEGER Null,
        unit_name TEXT Null,
        tag_id INTEGER Null,
        other_attribute TEXT Null,
        installation_date String Null,
        last_maintenance_date String Null,
        manufacturer TEXT Null,
        model TEXT Null,
        type_of_refrigerant TEXT Null,
        factory_charge_amount INTEGER Null,
        unit_type TEXT Null,
        store_id INTEGER Null,
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
        entry_date String Null,
        ip_address TEXT Null,
        address_gps TEXT Null,
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
        purchase_id INTEGER Null,
        tank_id INTEGER Null,
        unit_id INTEGER Null,    
        gas_type TEXT Null,
        quantity_before_in_lbs REAL Null,
        quantity_after_in_lbs REAL Null,
        technician_id INTEGER Null,
        notes TEXT Null,
        date String Null,
        status TEXT Null,
        refrigerant_id INTEGER Null,
        cylinder_id INTEGER Null,
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
        unit_id INTEGER Null,
        purchase_id INTEGER Null,
        repair_date String Null,
        technician_id INTEGER Null,
        causes TEXT Null,
        status TEXT Null,
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (purchase_id) REFERENCES "Purchase"(purchase_id)
    )
''')

# Create the "ODS_Sheet" table
cursor.execute('''
    CREATE TABLE "ODS_Sheet" (
        ods_id SERIAL PRIMARY KEY,
        contractor_id INTEGER Null,
        technician_id INTEGER Null,
        unit_id INTEGER Null,
        tag_id INTEGER Null,
        repair_id INTEGER Null,
        rec_id INTEGER Null,
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
        contractor_id INTEGER Null,
        technician_id INTEGER Null,
        offer_status TEXT Null,
        email_time_sent TEXT Null,
        FOREIGN KEY (contractor_id) REFERENCES "Contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id)
    )
''')

# Create the "Store_Location" table
cursor.execute('''
    CREATE TABLE "Store_Location" (
        store_location_id SERIAL PRIMARY KEY,
        store_id INTEGER Null,
        gps_location TEXT Null,
        FOREIGN KEY (store_id) REFERENCES "Store"(store_id)
    )
''')

#create "Maintenance" table            
cursor.execute('''
    CREATE TABLE "Maintenance" (
        maintenance_id SERIAL PRIMARY KEY,
        technician_id INTEGER Null,
        unit_id INTEGER Null,
        log TEXT Null,
        last_updated String Null,
        service_history TEXT Null,
        maintenance_date String Null,
        maintenance_type VARCHAR(50) Null,
        parts_used TEXT Null,
        notes TEXT Null,
        FOREIGN KEY (technician_id) REFERENCES "Technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "Unit"(unit_id)
    )
''')

#create "Maintenance_Detail" table               
cursor.execute('''
    CREATE TABLE "Maintenance_Detail" (
        maintenance_detail_id SERIAL PRIMARY KEY,
        maintenance_id INTEGER Null,
        description TEXT Null,
        status VARCHAR(50) Null,
        FOREIGN KEY (maintenance_id) REFERENCES "Maintenance"(maintenance_id)
    )
''')
               





# Commit the changes and close the connection
conn.commit()
conn.close()
