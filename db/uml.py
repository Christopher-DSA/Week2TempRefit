# Possible problems: , or " " or data type or the order
# 1. psycopg2.errors.UndefinedTable: relation "Repairs" does not exist (Order matters)
# 2. psycopg2.errors.UndefinedObject: type "datetime" does not exist
#    LINE 7: last_updated DATETIME, (change it to TIMESTAMP)

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

cursor.execute('DROP TABLE IF EXISTS "user"')
cursor.execute('DROP TABLE IF EXISTS "contractor"')
cursor.execute('DROP TABLE IF EXISTS "technician"')
cursor.execute('DROP TABLE IF EXISTS "refit_admin"')
cursor.execute('DROP TABLE IF EXISTS "wholesaler"')
cursor.execute('DROP TABLE IF EXISTS "invoice"')
cursor.execute('DROP TABLE IF EXISTS "subscription"')
cursor.execute('DROP TABLE IF EXISTS "tag"')
cursor.execute('DROP TABLE IF EXISTS "user_logging"')
cursor.execute('DROP TABLE IF EXISTS "user_detail"')
cursor.execute('DROP TABLE IF EXISTS "unit"')
cursor.execute('DROP TABLE IF EXISTS "organization"')
cursor.execute('DROP TABLE IF EXISTS "store"')
cursor.execute('DROP TABLE IF EXISTS "store_location"')
cursor.execute('DROP TABLE IF EXISTS "ods_sheet"')
cursor.execute('DROP TABLE IF EXISTS "technician_offer"')
cursor.execute('DROP TABLE IF EXISTS "cylinder"')
cursor.execute('DROP TABLE IF EXISTS "repair"')
cursor.execute('DROP TABLE IF EXISTS "reclaim_recovery"')
cursor.execute('DROP TABLE IF EXISTS "refrigerant"')
cursor.execute('DROP TABLE IF EXISTS "maintenance"')
cursor.execute('DROP TABLE IF EXISTS "maintenance_detail"')
cursor.execute('DROP TABLE IF EXISTS "cylinder_type"')


# Create the "User" table
cursor.execute('''

    CREATE TABLE "user"(
        user_id INTEGER PRIMARY KEY, 
        email TEXT,
        password TEXT,
        role TEXT,
        added_date TIMESTAMP,
        user_detail TEXT,
        status TEXT
    )''')

# Create the "User_Detail" table
cursor.execute('''
    CREATE TABLE "user_detail" (
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
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE "contractor" (
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
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')
               
# Create the "technician" table
cursor.execute('''
    CREATE TABLE "technician" (
        technician_id INTEGER PRIMARY KEY,
        ODS_licence_number TEXT,
        user_id INTEGER,
        contractor_id INTEGER,
        date_begin TIMESTAMP,
        date_end TIMESTAMP,
        user_status TEXT,
        contractor_status TEXT,
        FOREIGN KEY (user_id) REFERENCES "user"(user_id),
        FOREIGN KEY (contractor_id) REFERENCES "contractor"(contractor_id)
    )
''')

# Create the "Refit_Admin" table
cursor.execute('''
    CREATE TABLE "refit_admin" (
        admin_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        code_2fa_code TEXT,
        admin_level INTEGER,
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')

# Create the "Subscription" table
cursor.execute('''
    CREATE TABLE "subscription" (
        subscription_id INTEGER PRIMARY KEY,
        start_date TIMESTAMP,
        end_Date TIMESTAMP,
        package_size TEXT,
        compliant TEXT
    )
''')

#create "Cylinder_Type" table
cursor.execute('''
    CREATE TABLE "cylinder_type" (
        cylinder_type_id INTEGER PRIMARY KEY,
        type_name TEXT
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE "refrigerant" (
        refrigerant_id INTEGER PRIMARY KEY,
        refrigerant_name TEXT,
        list TEXT)
''')

# Create the "Cylinder" table
cursor.execute('''
    CREATE TABLE "cylinder" (
        cylinder_id INTEGER PRIMARY KEY,
        cylinder_size TEXT,
        cylinder_type_id INTEGER,
        cylinder_weight TEXT,
        added_date TIMESTAMP,
        refrigerant_id INTEGER,
        technician_id INTEGER,
        purchase_date TIMESTAMP,
        supplier TEXT,
        last_refill_date TIMESTAMP,
        condition TEXT,
        FOREIGN KEY (refrigerant_id) REFERENCES "refrigerant"(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (cylinder_type_id) REFERENCES "cylinder_type"(cylinder_type_id)
    )
''')

# Create the "Tag" table
cursor.execute('''
    CREATE TABLE "tag" (
        tag_id INTEGER PRIMARY KEY,
        tag_number TEXT,
        tag_url TEXT,
        type TEXT,
        cylinder_id INTEGER,
        wholesaler_id INTEGER,
        FOREIGN KEY (cylinder_id) REFERENCES "cylinder"(cylinder_id),
        FOREIGN KEY (wholesaler_id) REFERENCES "wholesaler"(wholesaler_id)  
    )
''')

# Create the "Invoice" table
cursor.execute('''
    CREATE TABLE "invoice" (
        invoice_id INTEGER PRIMARY KEY,
        subscription_id INTEGER,
        tag_id INTEGER,
        amount REAL,
        payment_method TEXT,
        tax REAL,
        date TIMESTAMP,
        FOREIGN KEY (subscription_id) REFERENCES "subscription"(subscription_id),
        FOREIGN KEY (tag_id) REFERENCES "tag"(tag_id)
    )
''')

# Create the "Wholesaler" table
cursor.execute('''
    CREATE TABLE "wholesaler" (
        wholesaler_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        tag_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES "user"(user_id),
        FOREIGN KEY (tag_id) REFERENCES "tag"(tag_id)
    )
''')

# Create the "Organization/Group" table
cursor.execute('''
    CREATE TABLE "organization" (
        organization_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        FOREIGN KEY (subscription_id) REFERENCES "subscription"(subscription_id),
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE "store" (
        store_id INTEGER PRIMARY KEY,
        organization_id INTEGER,
        branch TEXT,
        name TEXT,
        user_id INTEGER,
        address TEXT,
        gps_location TEXT,
        FOREIGN KEY (organization_id) REFERENCES "organization"(organization_id),
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')

# Create the "Unit" table
cursor.execute('''
    CREATE TABLE "unit" (
        unit_id INTEGER PRIMARY KEY,
        technician_id INTEGER,
        unit_name TEXT,
        tag_id INTEGER,
        other_attribute TEXT,
        installation_date TIMESTAMP,
        last_maintenance_date TIMESTAMP,
        manufacturer TEXT,
        model TEXT,
        type_of_refrigerant TEXT,
        factory_charge_amount INTEGER,
        unit_type TEXT,
        store_id INTEGER,
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (tag_id) REFERENCES "tag"(tag_id),
        FOREIGN KEY (store_id) REFERENCES "store"(store_id)
    )
''')

# Create the "User Logging" table
cursor.execute('''
    CREATE TABLE "user_logging" (
        log_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        entry_date TIMESTAMP,
        ip_address TEXT,
        address_gps TEXT,
        FOREIGN KEY (user_id) REFERENCES "user"(user_id)
    )
''')

# Create the "Purchase" table
cursor.execute('''
    CREATE TABLE "purchase" (
        purchase_id INTEGER PRIMARY KEY
    )
''')

# Create the "Tank" table
cursor.execute('''
    CREATE TABLE "tank" (
        tank_id INTEGER PRIMARY KEY
    )
''')

# Create the "Reclaim/Recovery" table
cursor.execute('''
    CREATE TABLE "reclaim_recovery" (
        rec_id INTEGER PRIMARY KEY,
        purchase_id INTEGER,
        tank_id INTEGER,
        unit_id INTEGER,    
        gas_type TEXT,
        quantity_before_in_lbs REAL,
        quantity_after_in_lbs REAL,
        technician_id INTEGER,
        notes TEXT,
        date TIMESTAMP,
        status TEXT,
        refrigerant_id INTEGER,
        cylinder_id INTEGER,
        FOREIGN KEY (unit_id) REFERENCES "unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (refrigerant_id) REFERENCES "refrigerant"(refrigerant_id),
        FOREIGN KEY (cylinder_id) REFERENCES "cylinder"(cylinder_id),
        FOREIGN KEY (purchase_id) REFERENCES "purchase"(purchase_id),
        FOREIGN KEY (tank_id) REFERENCES "tank"(tank_id)
    )
''')

# Create the "Repair" table
cursor.execute('''
    CREATE TABLE "repair" (
        repair_id INTEGER PRIMARY KEY,
        unit_id INTEGER,
        purchase_id INTEGER,
        repair_date TIMESTAMP,
        technician_id INTEGER,
        causes TEXT,
        status TEXT,
        FOREIGN KEY (unit_id) REFERENCES "unit"(unit_id),
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (purchase_id) REFERENCES "purchase"(purchase_id)
    )
''')

# Create the "ODS Sheet" table
cursor.execute('''
    CREATE TABLE "ods_sheet" (
        ods_id INTEGER PRIMARY KEY,
        contractor_id INTEGER,
        technician_id INTEGER,
        unit_id INTEGER,
        tag_id INTEGER,
        repair_id INTEGER,
        rec_id INTEGER,
        FOREIGN KEY (contractor_id) REFERENCES "contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "unit"(unit_id),
        FOREIGN KEY (repair_id) REFERENCES "repair"(repair_id),
        FOREIGN KEY (rec_id) REFERENCES  "reclaim_recovery"(rec_id),
        FOREIGN KEY (tag_id) REFERENCES "tag"(tag_id)
    )
''')

# Create the "Technician_Offer" table
cursor.execute('''
    CREATE TABLE "technician_offer" (
        contractor_id INTEGER,
        technician_id INTEGER,
        offer_status TEXT,
        email_time_sent TEXT,
        FOREIGN KEY (contractor_id) REFERENCES "contractor"(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id)
    )
''')

# Create the "Store_Location" table
cursor.execute('''
    CREATE TABLE "store_location" (
        store_id INTEGER PRIMARY KEY,
        gps_location TEXT,
        FOREIGN KEY (store_id) REFERENCES "store"(store_id)
    )
''')

#create "Maintenance" table            
cursor.execute('''
    CREATE TABLE "maintenance" (
        maintenance_id INT PRIMARY KEY,
        technician_id INT,
        unit_id INT,
        log TEXT,
        last_updated TIMESTAMP,
        service_history TEXT,
        maintenance_date TIMESTAMP,
        maintenance_type VARCHAR(50),
        parts_used TEXT,
        notes TEXT,
        FOREIGN KEY (technician_id) REFERENCES "technician"(technician_id),
        FOREIGN KEY (unit_id) REFERENCES "unit"(unit_id)
    )
''')

#create "Maintenance_Detail" table               
cursor.execute('''
    CREATE TABLE "maintenance_detail" (
        maintenance_detail_id INT PRIMARY KEY,
        maintenance_id INT,
        description TEXT,
        status VARCHAR(50),
        FOREIGN KEY (maintenance_id) REFERENCES "maintenance"(maintenance_id)
    )
''')
               





# Commit the changes and close the connection
conn.commit()
conn.close()
