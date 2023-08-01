**Models.py**

**Introduction**
SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) system that enables Python developers to interact with their database like they would with SQL, and also in a more Pythonic and object-oriented way. This document will provide an overview of the SQLAlchemy models defined in our codebase, which will aid any developer who takes over this project in understanding how we are interacting with our database.

**Model Overview**
Each SQLAlchemy model in our codebase corresponds to a table in our database. For instance, the User model corresponds to the 'User' table, Technician model to the 'Technician' table, and so forth. The attributes of each model represent the columns in their respective tables. These models are an abstraction that allows us to interact with our database in a more intuitive and Pythonic way.

**A brief description of what each model represents:**
2. Database Schema

The database schema consists of the following tables:

2.1 User
Represents user information with columns like user_id, email, password, role, etc.
Has relationships with several other classes representing different user roles (e.g., Technician, Contractor, Refit_admin, Wholesaler, etc.).

2.2 User_detail
Contains additional details about users with columns like user_detail_id, ODS_license_number, first_name, last_name, etc.
Has a relationship with the User class.

2.3 Technician
Represents information about technicians with columns like technician_id, user_detail, user_id, etc.
Has relationships with the User class and several other classes representing different technician-related data (e.g., Unit, ODS_Sheets, Cylinder, etc.).

2.4 Contractor
Represents contractor information with columns like contractor_id, name, user_id, etc.
Has relationships with the User class and other classes related to contractors (e.g., Technician_offer, Contractor_Detail, etc.).

2.5 Refit_admin
Represents refit admin information with columns like admin_id, name, user_id, etc.
Has a relationship with the User class.

2.6 Wholesaler
Represents wholesaler information with columns like wholesaler_id, name, user_id, etc.
Has relationships with the User class and Tags class.

2.7 Tags
Represents tags with columns like tag_id, invoice_id, tag_number, etc.
Has relationships with several other classes related to different entities using tags (e.g., Wholesaler, Cylinder, Unit, etc.).

2.8 Invoices
Represents invoice information with columns like invoice_id, subscription_id, tag_id, etc.
Has relationships with the Tags class and the Subscription class.

2.9 Subscription
Represents subscription information with columns like subscription_id, Start_date, End_Date, etc.
Has relationships with the Invoices class and the Organizations class.

2.10 Organizations
Represents organization information with columns like organization_id, name, logo, etc.
Has relationships with the Store class, the Subscription class, and the User class.

2.11 Store
Represents store information with columns like store_id, organization_id, branch, etc.
Has relationships with the Organizations class and the User class.

2.12 Store_locations
Represents store locations with columns like store_id and gps_location.

2.13 Cylinder
Represents cylinder information with columns like cylinder_id, cylinder_size, cylinder_type, etc.
Has relationships with the Reclaim_Recovery class, the Refrigerant class, the Technician class, and the Tags class.

2.14 Repairs
Represents repair information with columns like repair_id, unit_id, purchase_id, etc.
Has relationships with the Unit class, the Technician class, and the ODS_Sheets class.

2.15 Reclaim_Recovery
Represents information related to the reclaim and recovery process with columns like rec_id, purchase_id, unit_id, etc.
Has relationships with the ODS_Sheets class, the Unit class, the Technician class, the Cylinder class, and the Refrigerant class.

2.16 Refrigerant
Represents refrigerant information with columns like refrigerant_id, refrigerant_name, etc.
Has relationships with the Cylinder class and the Reclaim_Recovery class.

2.17 Maintenance
Represents maintenance information with columns like maintenance_id, technician_id, unit_id, etc.
Has relationships with the Maintenance_detail class, the Unit class, and the Technician class.

2.18 Maintenance_detail
Represents details related to maintenance with columns like maintenance_detail_id, maintenance_id, description, status, etc.
Has a relationship with the Maintenance class.

2.19 Technician_offer
Represents an offer made by a technician to a contractor with columns like contractor_id, technician_id, offer_status, etc.
Has relationships with Contractor and Technician.

2.20 Contractor_Detail
Represents detailed information about a contractor with columns like contractor_id, name, phone, address, etc.
Has a relationship with the Contractor class.

2.21 Unit
Represents a unit in the database with columns like unit_id, unit_name, address, province, etc.
Has relationships with Technician, Tags, and other classes for different types of relationships.

2.22 ODS_Sheets
Represents sheets related to ODS (Ozone-Depleting Substances) with columns like ods_id, contractor_id, technician_id, etc.
Has relationships with Contractor, Technician, Unit, Tags, Repairs, and Reclaim_Recovery.


3. CRUD Operations
The code provides CRUD (Create, Read, Update, Delete) operations using the CRUDMixin class. These operations can be performed on any of the defined model classes (e.g., User, Technician, Contractor, etc.). The CRUD operations are as follows:

3.1 Create
The create method allows creating a new instance of a model class and adding it to the database.
Example: User.create(User, email='example@example.com', password='password', role='technician', ...)

3.2 Read
The read method allows querying the database for instances of a model class based on filters.
Example: User.read(User, User.role == 'technician', User.status == 'active')

3.3 Update
The update method allows updating an existing instance of a model class.
Example: User.update(User, user_id=1, email='newemail@example.com')

3.4 Delete
The delete method allows deleting an instance of a model class based on its primary key.
Example: User.delete(User, user_id=1)


**Relationships in SQLAlchemy**
SQLAlchemy allows us to define relationships between tables. These relationships are represented in the models by the relationship() function. For example, in the User model, we have a relationship to the Technician model. This represents a one-to-one relationship: one user can have one user detail. The backref argument creates a back reference from Technician to User, allowing us to access a technician's user by using technician.user.

