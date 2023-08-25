import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Drop the tables if they already exist

cursor.execute('DROP TABLE IF EXISTS user')
cursor.execute('DROP TABLE IF EXISTS technician')
cursor.execute('DROP TABLE IF EXISTS contractor')
cursor.execute('DROP TABLE IF EXISTS refit_admin')
cursor.execute('DROP TABLE IF EXISTS wholesaler')
cursor.execute('DROP TABLE IF EXISTS invoices')
cursor.execute('DROP TABLE IF EXISTS subscription')
cursor.execute('DROP TABLE IF EXISTS contractor_detail')
cursor.execute('DROP TABLE IF EXISTS tags')
cursor.execute('DROP TABLE IF EXISTS user_logging')
cursor.execute('DROP TABLE IF EXISTS user_detail')
cursor.execute('DROP TABLE IF EXISTS unit')
cursor.execute('DROP TABLE IF EXISTS organizations')
cursor.execute('DROP TABLE IF EXISTS store')
cursor.execute('DROP TABLE IF EXISTS store_locations')
cursor.execute('DROP TABLE IF EXISTS ODS_sheets')
cursor.execute('DROP TABLE IF EXISTS technician_offer')
cursor.execute('DROP TABLE IF EXISTS cylinder')
cursor.execute('DROP TABLE IF EXISTS repairs')
cursor.execute('DROP TABLE IF EXISTS reclaim_Recovery')
cursor.execute('DROP TABLE IF EXISTS refrigerant')
cursor.execute('DROP TABLE IF EXISTS maintenance')
cursor.execute('DROP TABLE IF EXISTS maintenance_detail')
cursor.execute('DROP TABLE IF EXISTS cylinder_type')

# Create the "User" table
cursor.execute('''

    CREATE TABLE user(
        user_id INTEGER PRIMARY KEY, 
        email TEXT,
        password TEXT,
        role TEXT,
        added_date TEXT,
        user_detail TEXT,
        status TEXT
    )''')

# Create the "User_detail" table
cursor.execute('''
    CREATE TABLE user_detail (
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
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')

# Create the "technician" table
cursor.execute('''
    CREATE TABLE technician (
        technician_id INTEGER PRIMARY KEY,
        ODS_licence_number TEXT,
        user_id INTEGER,
        contractor_id INTEGER,
        date_begin TEXT,
        date_end TEXT,
        user_status TEXT,
        contractor_status TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
        FOREIGN KEY (contractor_id) REFERENCES contractor(contractor_id)
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE contractor (
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
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')
               
#                # Create the "Contractor Detail" table
# cursor.execute('''
#     CREATE TABLE Contractor_Detail (
#         contractor_id INTEGER PRIMARY KEY,
#         name TEXT,
#         phone TEXT,
#         address TEXT,
#         employees INTEGER,
#         are_they_tracking_refrigerant TEXT,
#         time_basis TEXT,
#         FOREIGN KEY (contractor_id) REFERENCES Contractor(contractor_id)
#     )
# ''')

# Create the "refit_admin" table
cursor.execute('''
    CREATE TABLE refit_admin (
        admin_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        code_2fa_code TEXT,
        admin_level INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')

# Create the "wholesaler" table
cursor.execute('''
    CREATE TABLE wholesaler (
        wholesaler_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        tag_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(user_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
    )
''')

# Create the "invoices" table
cursor.execute('''
    CREATE TABLE invoices (
        invoice_id INTEGER PRIMARY KEY,
        subscription_id INTEGER,
        tag_id INTEGER,
        amount REAL,
        payment_method TEXT,
        tax REAL,
        date TEXT,
        FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
    )
''')

# Create the "subscription" table
cursor.execute('''
    CREATE TABLE subscription (
        subscription_id INTEGER PRIMARY KEY,
        start_date TEXT,
        end_Date TEXT,
        package_size TEXT,
        compliant TEXT
    )
''')



# Create the "tags" table
cursor.execute('''
    CREATE TABLE tags (
        tag_id INTEGER PRIMARY KEY,
        invoice_id INTEGER,
        tag_number TEXT,
        tag_url TEXT,
        type TEXT,
        cylinder_id INTEGER
        
    )
''')

# Create the "unit" table
cursor.execute('''
    CREATE TABLE unit (
        unit_id INTEGER PRIMARY KEY,
        technician_id INTEGER,
        unit_name TEXT,
        tag_id INTEGER,
        other_attribute TEXT,
        installation_date TEXT,
        last_maintenance_date TEXT,
        manufacturer TEXT,
        model TEXT,
        type_of_refrigerant TEXT,
        factory_charge_amount INTEGER,
        unit_type TEXT,
        store_id TEXT,
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
        FOREIGN KEY (store_id) REFERENCES store(store_id)
    )
''')

# Create the "USER LOGGING" table
cursor.execute('''
    CREATE TABLE user_logging (
        log_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        entry_date TEXT,
        ip_address TEXT,
        address_gps TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')



# Create the "ODS Sheets" table
cursor.execute('''
    CREATE TABLE ODS_sheets (
        ods_id INTEGER PRIMARY KEY,
        contractor_id INTEGER,
        technician_id INTEGER,
        unit_id INTEGER,
        tag_id INTEGER,
        repair_id INTEGER,
        rec_id INTEGER,
        FOREIGN KEY (contractor_id) REFERENCES contractor(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
        FOREIGN KEY (unit_id) REFERENCES unit(unit_id),
        FOREIGN KEY (repair_id) REFERENCES repairs(repair_id),
        FOREIGN KEY (rec_id) REFERENCES  reclaim_recovery(rec_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
    )
''')

# Create the "technician_offer" table
cursor.execute('''
    CREATE TABLE technician_offer (
        contractor_id INTEGER,
        technician_id INTEGER,
        offer_status TEXT,
        email_time_sent TEXT,
        FOREIGN KEY (contractor_id) REFERENCES contractor(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id)
    )
''')

# Create the "Organizations/Groups" table
cursor.execute('''
    CREATE TABLE organizations (
        organization_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id),
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE store (
        store_id INTEGER PRIMARY KEY,
        organization_id INTEGER,
        branch TEXT,
        name TEXT,
        user_id INTEGER,
        address TEXT,
        gps_location TEXT,
        FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
''')

# Create the "Store_locations" table
cursor.execute('''
    CREATE TABLE store_locations (
        store_id INTEGER PRIMARY KEY,
        gps_location TEXT,
        FOREIGN KEY (store_id) REFERENCES store(store_id)
    )
''')
               
#create cylinder_type table
cursor.execute('''
    CREATE TABLE cylinder_type (
        cylinder_type_id INTEGER PRIMARY KEY,
        type_name TEXT
    )
''')

# Create the "Cylinder" table
cursor.execute('''
    CREATE TABLE cylinder (
        cylinder_id INTEGER PRIMARY KEY,
        cylinder_size TEXT,
        cylinder_type_id,
        cylinder_weight TEXT,
        added_date TEXT,
        refrigerant_id INTEGER,
        technician_id INTEGER,
        purchase_date TEXT,
        supplier TEXT,
        last_refill_date TEXT,
        condition TEXT,
        tag_id INTEGER,
        FOREIGN KEY (refrigerant_id) REFERENCES refrigerant(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
        FOREIGN KEY (cylinder_type_id) REFERENCES cylinder_type(cylinder_type_id)
    )
''')


# Create the "Repairs" table
cursor.execute('''
    CREATE TABLE repairs (
        repair_id INTEGER PRIMARY KEY,
        unit_id INTEGER,
        repair_date TEXT,
        technician_id INTEGER,
        causes TEXT,
        status TEXT,
        FOREIGN KEY (unit_id) REFERENCES unit(unit_id),
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id)
    )
''')

# Create the "Reclaim/Recovery" table
cursor.execute('''
    CREATE TABLE reclaim_Recovery (
        rec_id INTEGER PRIMARY KEY,
        unit_id INTEGER,
        gas_type TEXT,
        quantity_before_in_lbs REAL,
        quantity_after_in_lbs REAL,
        technician_id INTEGER,
        notes TEXT,
        date TEXT,
        status TEXT,
        refrigerant_id INTEGER,
        cylinder_id INTEGER,
        FOREIGN KEY (unit_id) REFERENCES unit(unit_id),
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
        FOREIGN KEY (refrigerant_id) REFERENCES refrigerant(refrigerant_id),
        FOREIGN KEY (cylinder_id) REFERENCES cylinder(cylinder_id)
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE refrigerant (
        refrigerant_id INTEGER PRIMARY KEY,
        refrigerant_name TEXT)
''')

#create "Maintenance table"               
cursor.execute('''
    CREATE TABLE maintenance (
        maintenance_id INT PRIMARY KEY,
        technician_id INT,
        unit_id INT,
        log TEXT,
        last_updated DATETIME,
        service_history TEXT,
        maintenance_date DATETIME,
        maintenance_type VARCHAR(50),
        parts_used TEXT,
        notes TEXT,
        FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
        FOREIGN KEY (unit_id) REFERENCES unit(unit_id)
    )
''')

#create Maintenance detail table               
cursor.execute('''
    CREATE TABLE maintenance_detail (
        maintenance_detail_id INT PRIMARY KEY,
        maintenance_id INT,
        description TEXT,
        status VARCHAR(50),
        FOREIGN KEY (maintenance_id) REFERENCES maintenance(maintenance_id)
    )
''')
               





# Commit the changes and close the connection
conn.commit()
conn.close()
