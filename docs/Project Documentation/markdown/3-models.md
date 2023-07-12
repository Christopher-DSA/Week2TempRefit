**Models.py**

**Introduction**
SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) system that enables Python developers to interact with their database like they would with SQL, and also in a more Pythonic and object-oriented way. This document will provide an overview of the SQLAlchemy models defined in our codebase, which will aid any developer who takes over this project in understanding how we are interacting with our database.

**Model Overview**
Each SQLAlchemy model in our codebase corresponds to a table in our database. For instance, the User model corresponds to the 'User' table, Technician model to the 'Technician' table, and so forth. The attributes of each model represent the columns in their respective tables. These models are an abstraction that allows us to interact with our database in a more intuitive and Pythonic way.

**A brief description of what each model represents:**
User: This represents the 'User' table in our database. Each instance of this model corresponds to a user in our system. It holds information such as email, password, role, added date, user detail, and status.

Technician: This model corresponds to the 'Technician' table and holds information specific to technicians in our system, such as the user detail, user ID, contractor ID, and the dates a technician began and ended.

Contractor: The 'Contractor' table is represented by this model. It contains information about contractors, such as their name, user ID, logo, status, subscription ID, and 2FA code.

Refit_admin: This model represents the 'Refit_admin' table, holding information about the Refit admins in our system, including their name, user ID, status, 2FA code, and admin level.

Wholesaler: This model corresponds to the 'Wholesaler' table and holds the necessary information for wholesalers, such as their name, user ID, status, and tag ID.

Tags: The 'Tags' table is represented by this model. It includes attributes like invoice ID, tag number, tag URL, type, and cylinder ID.

Invoices: This model corresponds to the 'Invoices' table and holds information regarding invoices, such as subscription ID, tag ID, amount, payment method, tax, and date.

Subscription: This model represents the 'Subscription' table. It contains details about subscriptions, such as start date, end date, package size, and compliance status.

Contractor_Detail: This model represents the 'Contractor_Detail' table and holds detailed information about contractors, such as name, phone, address, number of employees, whether they are tracking refrigerant, and the time basis.

User_logging: This model corresponds to the 'USER LOGGING' table, which contains logging information for each user, such as user ID, entry date, IP address, and GPS address.

User_detail: This model represents the 'User_detail' table and holds detailed information about users, including their ODS license number, name, birthdate, gender, address, province, city, postal code, and telephone.

Unit: This model represents a unit entity in the database. It includes several attributes such as unit_name, address, province, city, postal_code, telephone, etc. These attributes hold the information about a specific unit.

ODS_Sheets: This model represents the ODS (Ozone Depletion Substances) sheets table in the database. It contains multiple attributes such as contractor_id, technician_id, unit_id, tag_id, repair_id, and rec_id. This table essentially links contractors, technicians, units, and tags together and holds information related to ODS sheets.

Technician_offer: This model represents the offers made by technicians. It is linked with both the Contractor and Technician tables via foreign keys and contains information such as the status of an offer and the time an email was sent about the offer.

Organizations: This model holds the information about various organizations. Attributes include the name of the organization, a logo, and status among others. It is linked to the User table, indicating which user is associated with the organization.

Store: This model represents a store entity in the database. It contains information about a store, including its name and address. It is linked to the Organizations and User tables, indicating which organization the store belongs to and which user is associated with the store.

Store_locations: This model represents the geographical locations of various stores. It is linked to the Store table and includes the GPS location of each store.

Cylinder: This model represents a cylinder entity in the database. It contains various attributes, including the size, type, and weight of the cylinder, its current condition, and when it was last refilled. It is linked to the Technician and Tags tables, indicating which technician is associated with the cylinder and which tags are related to it.

Repairs: This model represents repair operations. It includes details about the repair, including the unit it's linked to, the technician performing the repair, the date, and the status. It's linked to the Unit and Technician tables.

Reclaim_Recovery: This model represents a reclaim and recovery entity. It contains various attributes such as the type of gas, quantities before and after in lbs, notes, date, status, and others. It is linked to the Unit, Technician, and Cylinder tables, providing associations with these entities.

Refrigerant: This model represents a refrigerant entity in the database. It contains attributes that define the name of the refrigerant and a list associated with it.


**Relationships in SQLAlchemy**
SQLAlchemy allows us to define relationships between tables. These relationships are represented in the models by the relationship() function. For example, in the User model, we have a relationship to the Technician model. This represents a one-to-many relationship: one user can have many technicians. The backref argument creates a back reference from Technician to User, allowing us to access a technician's user by using technician.user.

**CRUDMixin**
The CRUDMixin class is a helper class that adds convenient methods for CRUD (Create, Read, Update, Delete) operations to our models. This allows us to easily perform these operations on instances of our models, without having to write the SQLAlchemy code for these operations each time.

For instance, the create method allows us to create a new record and save it to the database. The update method allows us to update specific fields of a record. The save method saves the record to the database, and the delete method removes the record from the database.