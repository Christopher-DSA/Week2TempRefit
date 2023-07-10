import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Drop the tables if they already exist
cursor.execute('DROP TABLE IF EXISTS User')
cursor.execute('DROP TABLE IF EXISTS Technician')
cursor.execute('DROP TABLE IF EXISTS Contractor')
cursor.execute('DROP TABLE IF EXISTS Refit_admin')
cursor.execute('DROP TABLE IF EXISTS Wholesaler')
cursor.execute('DROP TABLE IF EXISTS Invoices')
cursor.execute('DROP TABLE IF EXISTS Subscription')
cursor.execute('DROP TABLE IF EXISTS Contractor_Detail')
cursor.execute('DROP TABLE IF EXISTS Tags')
cursor.execute('DROP TABLE IF EXISTS "USER LOGGING"')
cursor.execute('DROP TABLE IF EXISTS User_detail')
cursor.execute('DROP TABLE IF EXISTS Unit')
cursor.execute('DROP TABLE IF EXISTS Organizations')
cursor.execute('DROP TABLE IF EXISTS Store')
cursor.execute('DROP TABLE IF EXISTS Store_locations')
cursor.execute('DROP TABLE IF EXISTS ODS_Sheets')
cursor.execute('DROP TABLE IF EXISTS technician_offer')
cursor.execute('DROP TABLE IF EXISTS Cylinder')
cursor.execute('DROP TABLE IF EXISTS Repairs')
cursor.execute('DROP TABLE IF EXISTS Reclaim_Recovery')
cursor.execute('DROP TABLE IF EXISTS Refrigerant')

# Create the "User" table
cursor.execute('''
    CREATE TABLE User (
        user_id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        role TEXT,
        added_date TEXT,
        user_detail TEXT,
        status TEXT,
    )
''')

# Create the "Technician" table
cursor.execute('''
    CREATE TABLE Technician (
        technician_id INTEGER PRIMARY KEY,
        user_detail TEXT,
        user_id INTEGER,
        contractor_id INTEGER,
        date_begin TEXT,
        date_end TEXT,
        user_status TEXT,
        contractor_status TEXT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "Contractor" table
cursor.execute('''
    CREATE TABLE Contractor (
        contractor_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "Refit_admin" table
cursor.execute('''
    CREATE TABLE Refit_admin (
        admin_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        code_2fa_code TEXT,
        admin_level INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "Wholesaler" table
cursor.execute('''
    CREATE TABLE Wholesaler (
        wholesaler_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        status TEXT,
        tag_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
''')

# Create the "Invoices" table
cursor.execute('''
    CREATE TABLE Invoices (
        invoice_id INTEGER PRIMARY KEY,
        subscription_id INTEGER,
        tag_id INTEGER,
        amount REAL,
        payment_method TEXT,
        tax REAL,
        date TEXT,
        FOREIGN KEY (subscription_id) REFERENCES Subscription(subscription_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
''')

# Create the "Subscription" table
cursor.execute('''
    CREATE TABLE Subscription (
        subscription_id INTEGER PRIMARY KEY,
        Start_date TEXT,
        End_Date TEXT,
        Package_size TEXT,
        compliant TEXT
    )
''')

# Create the "Contractor Detail" table
cursor.execute('''
    CREATE TABLE Contractor_Detail (
        contractor_id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        employees INTEGER,
        are_they_tracking_refrigerant TEXT,
        time_basis TEXT
    )
''')

# Create the "Tags" table
cursor.execute('''
    CREATE TABLE Tags (
        tag_id INTEGER PRIMARY KEY,
        invoice_id INTEGER,
        tag_number TEXT,
        tag_url TEXT,
        type TEXT,
        cylinder_id INTEGER,
        FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id)
    )
''')

# Create the "Unit" table
cursor.execute('''
    CREATE TABLE Unit (
        unit_id INTEGER PRIMARY KEY,
        technician_id INTEGER,
        unit_name TEXT,
        address TEXT,
        province TEXT,
        city TEXT,
        postal_code TEXT,
        telephone TEXT,
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
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
''')

# Create the "USER LOGGING" table
cursor.execute('''
    CREATE TABLE "USER LOGGING" (
        log_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        entry_date TEXT,
        ip_address TEXT,
        address_gps TEXT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "User_detail" table
cursor.execute('''
    CREATE TABLE User_detail (
        user_id INTEGER PRIMARY KEY,
        ODS_license_number TEXT,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        birthdate TEXT,
        gender TEXT,
        address TEXT,
        province TEXT,
        city TEXT,
        postal_code TEXT,
        telephone TEXT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "ODS Sheets" table
cursor.execute('''
    CREATE TABLE ODS_Sheets (
        ods_id INTEGER PRIMARY KEY,
        contractor_id INTEGER,
        technician_id INTEGER,
        unit_id INTEGER,
        tag_id INTEGER,
        repair_id INTEGER,
        rec_id INTEGER,
        FOREIGN KEY (contractor_id) REFERENCES Contractor(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id),
        FOREIGN KEY (unit_id) REFERENCES Unit(unit_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
''')

# Create the "technician_offer" table
cursor.execute('''
    CREATE TABLE technician_offer (
        contractor_id INTEGER,
        technician_id INTEGER,
        offer_status TEXT,
        email_time_sent TEXT,
        FOREIGN KEY (contractor_id) REFERENCES Contractor(contractor_id),
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id)
    )
''')

# Create the "Organizations/Groups" table
cursor.execute('''
    CREATE TABLE Organizations (
        organization_id INTEGER PRIMARY KEY,
        name TEXT,
        user_id INTEGER,
        logo TEXT,
        status TEXT,
        subscription_id INTEGER,
        code_2fa_code TEXT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "Store" table
cursor.execute('''
    CREATE TABLE Store (
        store_id INTEGER PRIMARY KEY,
        organization_id INTEGER,
        branch TEXT,
        name TEXT,
        user_id INTEGER,
        address TEXT,
        FOREIGN KEY (organization_id) REFERENCES Organizations(organization_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the "Store_locations" table
cursor.execute('''
    CREATE TABLE Store_locations (
        store_id INTEGER PRIMARY KEY,
        gps_location TEXT,
        FOREIGN KEY (store_id) REFERENCES Store(store_id)
    )
''')

# Create the "Cylinder" table
cursor.execute('''
    CREATE TABLE Cylinder (
        cylinder_id INTEGER PRIMARY KEY,
        cylinder_size TEXT,
        cylinder_type TEXT,
        cylinder_weight TEXT,
        added_date TEXT,
        refrigerant_id INTEGER,
        technician_id INTEGER,
        purchase_date TEXT,
        supplier TEXT,
        last_refill_date TEXT,
        condition TEXT,
        tag_id INTEGER,
        FOREIGN KEY (refrigerant_id) REFERENCES Refrigerant(refrigerant_id),
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
''')

# Create the "Repairs" table
cursor.execute('''
    CREATE TABLE Repairs (
        repair_id INTEGER PRIMARY KEY,
        unit_id INTEGER,
        purchase_id INTEGER,
        repair_date TEXT,
        technician_id INTEGER,
        causes TEXT,
        status TEXT,
        FOREIGN KEY (unit_id) REFERENCES Unit(unit_id),
        FOREIGN KEY (purchase_id) REFERENCES Purchase(purchase_id),
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id)
    )
''')

# Create the "Reclaim/Recovery" table
cursor.execute('''
    CREATE TABLE Reclaim_Recovery (
        rec_id INTEGER PRIMARY KEY,
        purchase_id INTEGER,
        tank_id INTEGER,
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
        FOREIGN KEY (purchase_id) REFERENCES Purchase(purchase_id),
        FOREIGN KEY (tank_id) REFERENCES Tank(tank_id),
        FOREIGN KEY (unit_id) REFERENCES Unit(unit_id),
        FOREIGN KEY (technician_id) REFERENCES Technician(technician_id),
        FOREIGN KEY (refrigerant_id) REFERENCES Refrigerant(refrigerant_id),
        FOREIGN KEY (cylinder_id) REFERENCES Cylinder(cylinder_id)
    )
''')

# Create the "Refrigerant" table
cursor.execute('''
    CREATE TABLE Refrigerant (
        refrigerant_id INTEGER PRIMARY KEY,
        refrigerant_name TEXT,
        list TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
