from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, REAL, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import datet




# Base = declarative_base()

# engine = create_engine('sqlite:///database.db')
# Session=sessionmaker(bind=engine)

Base = declarative_base()

engine = create_engine('sqlite:///database.db')
def get_session():
    Session=sessionmaker(bind=engine)
    return Session()
   

class CRUDMixin:

    ''' This class is the main CRUD class with methods to create, read, update, and delete records. 
        Here all methods are classmethods which means there is no necessary to use the class constructor.'''

    # Constructor.
    def __init__(self, model, **kargs) -> None:
        
        self.model = model(**kargs)

    # Database model printing.
    def __repr__(self):
        return f"< model= **{self.model}** >"

    # Method to create a record.
    @classmethod
    def create(cls, model, rollback= False, **kargs):

        ''' This classmethod has the main function of creating a record, it receives the model class, the rollback argument, which
            is just for testing, and the arguments for the class model, such as name= 'My name', email= 'myemail@something.com'... '''
        
        # Class initializing.
        user = cls(model, **kargs)
        
        # rollback just for testing.
        if rollback == True:
            
            # Opening session.
            session = Session()
            # Adding the record.
            session.add(user.model)

            # Avoiding saving the record.
            session.rollback()

            # Writing the record.
            session.commit()

            # Closing session.
            session.close()

        else:

            # Opening session.
            session = Session()
            # Adding the record.
            session.add(user.model)
            # Writing the record.
            session.commit()

            # Closing session.
            session.close()
            # Returning the user.
            return user

    @classmethod
    def read(cls, model, all=False, latest_field=None, count_only=False, relative_match=None, order_by = False ,**kwargs):
        """
        This class method is used to read records within the model. It receives the class model, the argument 'all' which
        determines if all records should be returned if True, the field name for determining the latest record, whether to
        return only a count of records, the relative_match for filtering based on a relative string match, and the arguments
        of the class method to filter the records. It retrieves the record(s) based on the filter criteria and returns the
        latest record based on the specified field.
        """
        # Opening session.
        session = Session()

        if count_only:
            # If count_only is True, return a count of the records matching the filter criteria.
            count = session.query(func.count(model.ID)).filter_by(**kwargs).scalar()

            # Closing session.
            session.close()

            # Returning the count.
            return count
        else:
            # If all is True, return all records.
            if all:
                if order_by:
                    q = session.query(model).filter_by(**kwargs).order_by(model.date.asc()).all()
                else:
                    q = session.query(model).filter_by(**kwargs).all()
            else:
                if latest_field is None:
                    # If the latest_field is not specified, retrieve the first record that matches the filter criteria.
                    q = session.query(model).filter_by(**kwargs).first()
                else:
                    # Retrieve the record that matches the filter criteria and has the latest value for the specified field.
                    query = session.query(model).filter_by(**kwargs)

                    if relative_match is not None:
                        # Apply the relative string match filter.
                        query = query.filter(model.field.ilike(f"%{relative_match}%"))

                    q = query.order_by(getattr(model, latest_field).desc()).first()

            # Closing session.
            session.close()

            # Returning the query.
            return q




    # Method to modify the records.
    @classmethod
    def update(self, model, attr, new, **kwargs):

        ''' Update classmethod is used to update records, it receives the model, the attribute(attr) argument which we want to 
            update within the record, the new argument, which is the new input, and the arguments to find the record we want to
            modify. As an example for Admin -> Admin, 'name', new= 'New name', name= 'my name', it will search the first record
            with the name; then, it will replace the field name with the new input 'New name'. '''

        # Opening session.
        session = Session()
        # Adding all changes.

        record = session.query(model).filter_by(**kwargs).first()

        setattr(record, attr, new)

        session.commit()

        kwargs = {attr: new}

        print(session.query(model).filter_by(**kwargs).first())

        # Closing the session.
        session.close()

        print('updated')

    # Method to delete records within the database.
    @classmethod
    def delete(self, model, **kwargs):

        ''' Delete classmethod is to delete records within the database, it receives the model which is the class model,
            and the arguments to get this record, as an example. Admin -> Admin, 'name'= 'my name', 'password'= 'pass' 
            . It will delete the first record which matches the criterion. '''

        session = Session()

        record = session.query(model).filter_by(**kwargs).first()

        # Deleting the record.
        session.delete(record)
        # Deleting the record within the database.
        session.commit()

        # Closing the session.
        session.close()

        print('Deleted')

class User(Base, CRUDMixin):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String)
    user_detail = Column(String)
    status = Column(String)

    technicians = relationship("Technician", backref="user")
    # contractors = relationship("Contractor", backref="user")
    # refit_admins = relationship("Refit_admin", backref="user")
    # wholesalers = relationship("Wholesaler", backref="user")
    # user_logs = relationship("User_logging", backref="user")
    # user_details = relationship("User_detail", backref="user")
    # organizations = relationship("Organizations", backref="user")
    # stores = relationship("Store", backref="user")
  
class Technician(Base, CRUDMixin):
    __tablename__ = 'Technician'
    technician_id = Column(Integer, primary_key=True)
    user_detail = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    contractor_id = Column(Integer)
    date_begin = Column(String)
    date_end = Column(String)
    user_status = Column(String)
    contractor_status = Column(String)

    # units = relationship("Unit", backref="technician")
    # ods_sheets = relationship("ODS_Sheets", backref="technician")
    # technician_offers = relationship("Technician_offer", backref="technician")
    # cylinders = relationship("Cylinder", backref="technician")
    # repairs = relationship("Repairs", backref="technician")
    # reclaims = relationship("Reclaim_Recovery", backref="technician")

# class Contractor(Base, CRUDMixin):
#     __tablename__ = 'Contractor'
#     contractor_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('user.user_id'))
#     logo = Column(String)
#     status = Column(String)
#     subscription_id = Column(Integer)
#     code_2fa_code = Column(String)

    # contractor_details = relationship("Contractor_Detail", backref="contractor")
    # ods_sheets = relationship("ODS_Sheets", backref="contractor")
    # technician_offers = relationship("Technician_offer", backref="contractor")

# class Contractor_Detail(Base, CRUDMixin):
#     __tablename__ = 'Contractor_Detail'
#     contractor_id = Column(Integer,ForeignKey('Contractor.contractor_id'), primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     address = Column(String)
#     employees = Column(Integer)
#     are_they_tracking_refrigerant = Column(String)
#     time_basis = Column(String)

# class Refit_admin(Base, CRUDMixin):
#     __tablename__ = 'Refit_admin'
#     admin_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     status = Column(String)
#     code_2fa_code = Column(String)
#     admin_level = Column(Integer)

# class Wholesaler(Base, CRUDMixin):
#     __tablename__ = 'Wholesaler'
#     wholesaler_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     status = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

# class Invoices(Base, CRUDMixin):
#     __tablename__ = 'Invoices'
#     invoice_id = Column(Integer, primary_key=True)
#     subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'))
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     amount = Column(REAL)
#     payment_method = Column(String)
#     tax = Column(REAL)
#     date = Column(String)

# class Subscription(Base, CRUDMixin):
#     __tablename__ = 'Subscription'
#     subscription_id = Column(Integer, primary_key=True)
#     Start_date = Column(String)
#     End_Date = Column(String)
#     Package_size = Column(String)
#     compliant = Column(String)

#     invoices = relationship("Invoices", backref="subscription")
#     organizations = relationship("Organizations", backref="subscription")

# class Tags(Base, CRUDMixin):
#     __tablename__ = 'Tags'
#     tag_id = Column(Integer, primary_key=True)
#     invoice_id = Column(Integer, ForeignKey('Invoices.invoice_id'))
#     tag_number = Column(String)
#     tag_url = Column(String)
#     type = Column(String)
#     cylinder_id = Column(Integer)

#     wholesalers = relationship("Wholesaler", backref="tag")
#     units = relationship("Unit", backref="tag")
#     ods_sheets = relationship("ODS_Sheets", backref="tag")
#     cylinders = relationship("Cylinder", backref="tag")

# class Unit(Base, CRUDMixin):
#     __tablename__ = 'Unit'
#     unit_id = Column(Integer, primary_key=True)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     unit_name = Column(String)
#     address = Column(String)
#     province = Column(String)
#     city = Column(String)
#     postal_code = Column(String)
#     telephone = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     other_attribute = Column(String)
#     installation_date = Column(String)
#     last_maintenance_date = Column(String)
#     manufacturer = Column(String)
#     model = Column(String)
#     type_of_refrigerant = Column(String)
#     factory_charge_amount = Column(Integer)
#     unit_type = Column(String)
#     store_id = Column(String)

#     ods_sheets = relationship("ODS_Sheets", backref="unit")
#     repairs = relationship("Repairs", backref="unit")
#     reclaims = relationship("Reclaim_Recovery", backref="unit")

# class User_logging(Base, CRUDMixin):
#     __tablename__ = 'USER LOGGING'
#     log_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     entry_date = Column(String)
#     ip_address = Column(String)
#     address_gps = Column(String)

# class User_detail(Base, CRUDMixin):
#     __tablename__ = 'User_detail'
#     user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
#     ODS_license_number = Column(String)
#     first_name = Column(String)
#     middle_name = Column(String)
#     last_name = Column(String)
#     birthdate = Column(String)
#     gender = Column(String)
#     address = Column(String)
#     province = Column(String)
#     city = Column(String)
#     postal_code = Column(String)
#     telephone = Column(String)

# class ODS_Sheets(Base, CRUDMixin):
#     __tablename__ = 'ODS_Sheets'
#     ods_id = Column(Integer, primary_key=True)
#     contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'))
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     repair_id = Column(Integer)
#     rec_id = Column(Integer)

# class Technician_offer(Base, CRUDMixin):
#     __tablename__ = 'technician_offer'
#     contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'), primary_key=True)
#     offer_status = Column(String)
#     email_time_sent = Column(String)

# class Organizations(Base, CRUDMixin):
#     __tablename__ = 'Organizations'
#     organization_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     logo = Column(String)
#     status = Column(String)
#     subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'))
#     code_2fa_code = Column(String)

#     stores = relationship("Store", backref="organization")

# class Store(Base, CRUDMixin):
#     __tablename__ = 'Store'
#     store_id = Column(Integer, primary_key=True)
#     organization_id = Column(Integer, ForeignKey('Organizations.organization_id'))
#     branch = Column(String)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     address = Column(String)

#     store_locations = relationship("Store_locations", backref="store")

# class Store_locations(Base, CRUDMixin):
#     __tablename__ = 'Store_locations'
#     store_id = Column(Integer, ForeignKey('Store.store_id'), primary_key=True)
#     gps_location = Column(String)

# class Cylinder(Base, CRUDMixin):
#     __tablename__ = 'Cylinder'
#     cylinder_id = Column(Integer, primary_key=True)
#     cylinder_size = Column(String)
#     cylinder_type = Column(String)
#     cylinder_weight = Column(String)
#     added_date = Column(String)
#     refrigerant_id = Column(Integer)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     purchase_date = Column(String)
#     supplier = Column(String)
#     last_refill_date = Column(String)
#     condition = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

#     reclaims = relationship("Reclaim_Recovery", backref="cylinder")

# class Repairs(Base, CRUDMixin):
#     __tablename__ = 'Repairs'
#     repair_id = Column(Integer, primary_key=True)
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     repair_date = Column(String)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     causes = Column(String)
#     status = Column(String)

# class Reclaim_Recovery(Base, CRUDMixin):
#     __tablename__ = 'Reclaim_Recovery'
#     rec_id = Column(Integer, primary_key=True)
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     gas_type = Column(String)
#     quantity_before_in_lbs = Column(REAL)
#     quantity_after_in_lbs = Column(REAL)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     notes = Column(String)
#     date = Column(String)
#     status = Column(String)
#     refrigerant_id = Column(Integer)
#     cylinder_id = Column(Integer, ForeignKey('Cylinder.cylinder_id'))

# class Refrigerant(Base, CRUDMixin):
#     __tablename__ = 'Refrigerant'
#     refrigerant_id = Column(Integer, primary_key=True)
#     refrigerant_name = Column(String)
#     list = Column(String)

# class Maintenance(Base, CRUDMixin):
#     __tablename__ = 'Maintenance'
#     maintenance_id = Column(Integer, primary_key=True)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     log = Column(Text)
#     # last_updated = Column(DateTime)
#     service_history = Column(Text)
#     # maintenance_date = Column(DateTime)
#     maintenance_type = Column(String(50))
#     parts_used = Column(Text)
#     notes = Column(Text)

#     maintenance_details = relationship("Maintenance_detail", backref="maintenance")

# class Maintenance_detail(Base, CRUDMixin):
#     __tablename__ = 'Maintenance_detail'
#     maintenance_detail_id = Column(Integer, primary_key=True)
#     maintenance_id = Column(Integer, ForeignKey('Maintenance.maintenance_id'))
#     description = Column(Text)
#     status = Column(String(50))

# class User(Base):
#     __tablename__ = 'User'

#     user_id = Column(Integer, primary_key=True)
#     email = Column(String)
#     password = Column(String)
#     role = Column(String)
#     added_date = Column(String)
#     user_detail = Column(String)
#     status = Column(String)

#     technicians = relationship('Technician', backref='user')
#     contractors = relationship('Contractor', backref='user')
#     refit_admins = relationship('Refit_admin', backref='user')
#     wholesalers = relationship('Wholesaler', backref='user')
#     user_details = relationship('User_detail', backref='user')
#     organizations = relationship('Organizations', backref='user')
#     stores = relationship('Store', backref='user')
#     user_logging = relationship('USER_LOGGING', backref='user')

#     def __repr__(self) -> str:
#         return f'User {self.user_id}'

# class Technician(Base):
#     __tablename__ = 'Technician'
#     technician_id = Column(Integer, primary_key=True)
#     user_detail = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     contractor_id = Column(Integer)
#     date_begin = Column(String)
#     date_end = Column(String)
#     user_status = Column(String)
#     contractor_status = Column(String)

#     user = relationship('User', backref='technicians')
#     units = relationship('Unit', backref='technician')
#     ods_sheets = relationship('ODS_Sheets', backref='technician')
#     cylinders = relationship('Cylinder', backref='technician')
#     repairs = relationship('Repairs', backref='technician')
#     reclaim_recoveries = relationship('Reclaim_Recovery', backref='technician')
#     technician_offers = relationship('technician_offer', backref='contractor')

#     def __repr__(self):
#         return f'Technician {self.technician_id}'

# class Contractor(Base):
#     __tablename__ = 'Contractor'
#     contractor_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     logo = Column(String)
#     status = Column(String)
#     subscription_id = Column(Integer)
#     code_2fa_code = Column(String)

#     user = relationship('User', backref='contractors')
#     technicians = relationship('Technician', backref='contractor')
#     contractor_details = relationship('Contractor_Detail', backref='contractor')
#     ods_sheets = relationship('ODS_Sheets', backref='contractor')
#     technician_offers = relationship('technician_offer', backref='contractor')

#     def __repr__(self):
#         return f'Contractor {self.contractor_id}'

# class Refit_admin(Base):
#     __tablename__ = 'Refit_admin'
#     admin_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     status = Column(String)
#     code_2fa_code = Column(String)
#     admin_level = Column(Integer)

#     user = relationship('User', backref='refit_admins')

#     def __repr__(self):
#         return f'Refit_admin {self.admin_id}'

# class Wholesaler(Base):
#     __tablename__ = 'Wholesaler'
#     wholesaler_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     status = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

#     user = relationship('User', backref='wholesalers')
#     tag = relationship('Tags', backref='wholesalers')

#     def __repr__(self):
#         return f'Wholesaler {self.wholesaler_id}'

# class Tags(Base):
#     __tablename__ = 'Tags'

#     tag_id = Column(Integer, primary_key=True)
#     invoice_id = Column(Integer, ForeignKey('Invoices.invoice_id'))
#     tag_number = Column(String)
#     tag_url = Column(String)
#     type = Column(String)
#     cylinder_id = Column(Integer)

#     invoices = relationship('Invoices', backref='tags')

#     def __repr__(self):
#         return f'Tags {self.tag_id}'


# class Invoices(Base):
#     __tablename__ = 'Invoices'
#     invoice_id = Column(Integer, primary_key=True)
#     subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'))
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     amount = Column(REAL)
#     payment_method = Column(String)
#     tax = Column(REAL)
#     date = Column(String)

#     tags = relationship('Tags', backref='invoices')

#     def __repr__(self):
#         return f'Invoices {self.invoice_id}'


# class Subscription(Base):
#     __tablename__ = 'Subscription'
#     subscription_id = Column(Integer, primary_key=True)
#     Start_date = Column(String)
#     End_Date = Column(String)
#     Package_size = Column(String)
#     compliant = Column(String)

#     invoices = relationship('Invoices', backref='subscription')

#     def __repr__(self):
#         return f'Subscription {self.subscription_id}'

# class Contractor_Detail(Base):
#     __tablename__ = 'Contractor_Detail'

#     contractor_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     address = Column(String)
#     employees = Column(Integer)
#     are_they_tracking_refrigerant = Column(String)
#     time_basis = Column(String)

#     def __repr__(self):
#         return f'Contractor_Detail {self.contractor_id}'


# class User_logging(Base):
#     __tablename__ = 'USER LOGGING'
#     log_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     entry_date = Column(String)
#     ip_address = Column(String)
#     address_gps = Column(String)

#     user = relationship('User', backref='user_logging')

#     def __repr__(self):
#         return f'User_logging {self.log_id}'

# class User_detail(Base):
#     __tablename__ = 'User_detail'

#     user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
#     ODS_license_number = Column(String)
#     first_name = Column(String)
#     middle_name = Column(String)
#     last_name = Column(String)
#     birthdate = Column(String)
#     gender = Column(String)
#     address = Column(String)
#     province = Column(String)
#     city = Column(String)
#     postal_code = Column(String)
#     telephone = Column(String)

#     user = relationship('User', backref='user_details')

#     def __repr__(self):
#         return f'User_detail {self.user_id}'


# class Unit(Base):
#     __tablename__ = 'Unit'
#     unit_id = Column(Integer, primary_key=True)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     unit_name = Column(String)
#     address = Column(String)
#     province = Column(String)
#     city = Column(String)
#     postal_code = Column(String)
#     telephone = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     other_attribute = Column(String)
#     installation_date = Column(String)
#     last_maintenance_date = Column(String)
#     manufacturer = Column(String)
#     model = Column(String)
#     type_of_refrigerant = Column(String)
#     factory_charge_amount = Column(Integer)
#     unit_type = Column(String)
#     store_id = Column(String)

#     technician = relationship('Technician', backref='units')
#     tag = relationship('Tags', backref='units')

#     def __repr__(self):
#         return f'Unit {self.unit_id}'

# class ODS_Sheets(Base):
#     __tablename__ = 'ODS_Sheets'
#     ods_id = Column(Integer, primary_key=True)
#     contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'))
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
#     repair_id = Column(Integer)
#     rec_id = Column(Integer)

#     contractor = relationship('Contractor', backref='ods_sheets')
#     technician = relationship('Technician', backref='ods_sheets')
#     unit = relationship('Unit', backref='ods_sheets')
#     tag = relationship('Tags', backref='ods_sheets')

#     def __repr__(self):
#         return f'ODS_Sheets {self.ods_id}'

# class Technician_offer(Base):
#     __tablename__ = 'technician_offer'
#     contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'), primary_key=True)
#     offer_status = Column(String)
#     email_time_sent = Column(String)

#     contractor = relationship('Contractor', backref='technician_offers')
#     technician = relationship('Technician', backref='technician_offers')

#     def __repr__(self):
#         return f'Technician_offer {self.contractor_id}, {self.technician_id}'

# class Organizations(Base):
#     __tablename__ = 'Organizations'
#     organization_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     logo = Column(String)
#     status = Column(String)
#     subscription_id = Column(Integer)
#     code_2fa_code = Column(String)

#     user = relationship('User', backref='organizations')

#     def __repr__(self):
#         return f'Organizations {self.organization_id}'

# class Store(Base):
#     __tablename__ = 'Store'
#     store_id = Column(Integer, primary_key=True)
#     organization_id = Column(Integer, ForeignKey('Organizations.organization_id'))
#     branch = Column(String)
#     name = Column(String)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     address = Column(String)

#     organization = relationship('Organizations', backref='stores')
#     user = relationship('User', backref='stores')

#     def __repr__(self):
#         return f'Store {self.store_id}'

# class Store_locations(Base):
#     __tablename__ = 'Store_locations'

#     store_id = Column(Integer, ForeignKey('Store.store_id'), primary_key=True)
#     gps_location = Column(String)

#     store = relationship('Store', backref='store_locations')

#     def __repr__(self):
#         return f'Store_locations {self.store_id}'


# class Cylinder(Base):
#     __tablename__ = 'Cylinder'
#     cylinder_id = Column(Integer, primary_key=True)
#     cylinder_size = Column(String)
#     cylinder_type = Column(String)
#     cylinder_weight = Column(String)
#     added_date = Column(String)
#     refrigerant_id = Column(Integer)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     purchase_date = Column(String)
#     supplier = Column(String)
#     last_refill_date = Column(String)
#     condition = Column(String)
#     tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

#     technician = relationship('Technician', backref='cylinders')
#     tag = relationship('Tags', backref='cylinders')

#     def __repr__(self):
#         return f'Cylinder {self.cylinder_id}'

# class Repairs(Base):
#     __tablename__ = 'Repairs'
#     repair_id = Column(Integer, primary_key=True)
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     purchase_id = Column(Integer)
#     repair_date = Column(String)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     causes = Column(String)
#     status = Column(String)

#     unit = relationship('Unit', backref='repairs')
#     technician = relationship('Technician', backref='repairs')

#     def __repr__(self):
#         return f'Repairs {self.repair_id}'

# class Reclaim_Recovery(Base):
#     __tablename__ = 'Reclaim_Recovery'
#     rec_id = Column(Integer, primary_key=True)
#     purchase_id = Column(Integer)
#     tank_id = Column(Integer)
#     unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
#     gas_type = Column(String)
#     quantity_before_in_lbs = Column(REAL)
#     quantity_after_in_lbs = Column(REAL)
#     technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
#     notes = Column(String)
#     date = Column(String)
#     status = Column(String)
#     refrigerant_id = Column(Integer)
#     cylinder_id = Column(Integer, ForeignKey('Cylinder.cylinder_id'))

#     unit = relationship('Unit', backref='reclaim_recoveries')
#     technician = relationship('Technician', backref='reclaim_recoveries')
#     cylinder = relationship('Cylinder', backref='reclaim_recoveries')

#     def __repr__(self):
#         return f'Reclaim_Recovery {self.rec_id}'

# class Refrigerant(Base):
#     __tablename__ = 'Refrigerant'
#     refrigerant_id = Column(Integer, primary_key=True)
#     refrigerant_name = Column(String)
#     list = Column(String)

#     def __repr__(self):
#         return f'Refrigerant {self.refrigerant_id}'

