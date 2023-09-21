from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, REAL, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import os


# SQLAlcehmy base.
Base = declarative_base()

database_url= 'postgresql://sofvie:gXq!%g^&dm*OuWfK8HhC@refitdb.czvko9baktul.ca-central-1.rds.amazonaws.com:5432/postgres?sslmode=require'
engine = create_engine(database_url)
#engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
#database_url = os.getenv('DATABASE_URL')
#print(f'DATABASE_URL: {database_url}')


class User(Base):

    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String,default=func.now())
    user_detail = Column(String)
    status = Column(String)

    technicians = relationship('Technician', back_populates='users')
    contractors = relationship('Contractor', back_populates='users')
    refit_admins = relationship('Refit_admin', back_populates='users')
    wholesalers = relationship('Wholesaler', back_populates='users')
    user_details = relationship('User_detail', back_populates='users')
    organizations = relationship('Organizations', back_populates='users')
    stores = relationship('Store', back_populates='users')
    # user_loggings = relationship('User_logging', back_populates='users')

    def __repr__(self):
        return 'User model'
    

class User_detail(Base):
    __tablename__ = 'user_detail'

    user_detail_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)
    user_id=Column(Integer,ForeignKey('user.user_id'))
    users = relationship('User', back_populates='user_details')

    def __repr__(self):
        return 'User Detail Model'

class Technician(Base):
    __tablename__ = 'technician'
    technician_id = Column(Integer, primary_key=True)
    
    ODS_licence_number = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    contractor_id = Column(Integer,ForeignKey('contractor.contractor_id'))
    date_begin = Column(String)
    date_end = Column(String)
    user_status = Column(String)
    contractor_status = Column(String)

    users = relationship('User', back_populates='technicians')
    units = relationship('Unit', back_populates='technicians')
    ods_sheets = relationship('ODS_sheets', back_populates='technicians')
    cylinders = relationship('Cylinder', back_populates='technicians')
    repairs = relationship('Repairs', back_populates='technicians')
    reclaim_recoveries = relationship('Reclaim_recovery', back_populates='technicians')
    technician_offers = relationship('Technician_offer', back_populates='technicians')
    maintenances = relationship('Maintenance', back_populates='technicians')
    contractors = relationship('Contractor', back_populates='technicians')


    def __repr__(self):
        return 'Technician Model'

class Contractor(Base):

    __tablename__ = 'contractor'

    contractor_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    users = relationship('User', back_populates='contractors')
    technicians = relationship('Technician', back_populates='contractors')
    # contractor_details = relationship('ontractor_detail', back_populates='contractors')
    ods_sheets = relationship('ODS_sheets', back_populates='contractors')
    technician_offers = relationship('Technician_offer', back_populates='contractors')

    def __repr__(self):
        return f'Contractor {self.contractor_id}'

# class Contractor_Detail(Base):
#     __tablename__ = 'Contractor_Detail'

#     contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     address = Column(String)
#     employees = Column(Integer)
#     are_they_tracking_refrigerant = Column(String)
#     time_basis = Column(String)

#     contractors=relationship('Contractor', back_populates='contractor_details')

#     def __repr__(self):
#         return f'Contractor_Detail {self.contractor_id}'






   

class Refit_Admin(Base):

    __tablename__ = 'refit_admin'

    admin_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(String)
    code_2fa_code = Column(String)
    admin_level = Column(Integer)

    users = relationship('User', back_populates='refit_admins')

    def __repr__(self):
        return 'Refit Admin Model'

class Wholesaler(Base):

    __tablename__ = 'wholesaler'
    
    wholesaler_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'))

    users = relationship('User', back_populates='wholesalers')
    tags = relationship('Tags', back_populates='wholesalers')

    def __repr__(self):
        return 'Wholesaler Model'

class Tags(Base):

    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer)
    tag_number = Column(String)
    tag_url = Column(String)
    type = Column(String)
    cylinder_id = Column(Integer)

    # invoices = relationship('Invoices', back_populates='tags', foreign_keys=[invoice_id])
    wholesalers=relationship('Wholesaler',back_populates='tags')
    ods_sheets=relationship('ODS_sheets',back_populates='tags')
    cylinders=relationship('Cylinder',back_populates='tags')
    units=relationship('Unit',back_populates='tags')

    def __repr__(self):
        return 'Tags Model'


class Invoices(Base):
    __tablename__ = 'Invoices'
    invoice_id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('subscription.subscription_id'))
    tag_id = Column(Integer)
    amount = Column(REAL)
    payment_method = Column(String)
    tax = Column(REAL)
    date = Column(String)

    # tags = relationship('Tags', back_populates='invoices')
    subscriptions=relationship('Subscription',back_populates='invoices')

    def __repr__(self):
        return 'Invoices Model'


class Subscription(Base):

    __tablename__ = 'subscription'

    subscription_id = Column(Integer, primary_key=True)
    Start_date = Column(String)
    End_Date = Column(String)
    Package_size = Column(String)
    compliant = Column(String)

    invoices = relationship('Invoices', back_populates='subscriptions')
    organizations=relationship('Organizations',back_populates='subscriptions')

    def __repr__(self):
        return 'Subscription MOdel'



# class User_logging(Base):
#     __tablename__ = 'USER_LOGGING'
#     log_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     entry_date = Column(String)
#     ip_address = Column(String)
#     address_gps = Column(String)

#     users = relationship('User', back_populates='user_loggings')

#     def __repr__(self):
#         return f'User_logging {self.log_id}'






class Unit(Base):

    __tablename__ = 'unit'
    
    unit_id = Column(Integer, primary_key=True)
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    unit_name = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'))
    other_attribute = Column(String)
    installation_date = Column(String)
    last_maintenance_date = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    type_of_refrigerant = Column(String)
    factory_charge_amount = Column(Integer)
    unit_type = Column(String)
    store_id = Column(Integer,ForeignKey('store.store_id'))
    

    technicians = relationship('Technician', back_populates='units')
    tags = relationship('Tags', back_populates='units')
    reclaim_recoveries=relationship('Reclaim_recovery',back_populates='units')
    ods_sheets=relationship('ODS_sheets',back_populates='units')
    repairs=relationship('Repairs',back_populates='units')
    maintenances=relationship('Maintenance',back_populates='units')
    ustores=relationship('Store',back_populates='units')

    def __repr__(self):
        return 'Unit MOdel'

class ODS_sheets(Base):

    __tablename__ = 'ODS_sheets'
    
    ods_id = Column(Integer, primary_key=True)
    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    unit_id = Column(Integer, ForeignKey('unit.unit_id'))
    tag_id = Column(Integer, ForeignKey('tags.tag_id'))
    repair_id = Column(Integer, ForeignKey('repairs.repair_id'))
    rec_id = Column(Integer, ForeignKey('reclaim_recovery.rec_id'))

    contractors = relationship('Contractor', back_populates='ods_sheets')
    technicians = relationship('Technician', back_populates='ods_sheets')
    units = relationship('Unit', back_populates='ods_sheets')
    tags = relationship('Tags', back_populates='ods_sheets')
    repairs = relationship('Repairs', back_populates='ods_sheets')
    reclaim_recoveries = relationship('Reclaim_recovery', back_populates='ods_sheets')


    def __repr__(self):
        return 'ODS_Sheets Model'

class Technician_offer(Base):

    __tablename__ = 'technician_offer'

    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'), primary_key=True)
    technician_id = Column(Integer, ForeignKey('technician.technician_id'), primary_key=True)
    offer_status = Column(String)
    email_time_sent = Column(String)

    contractors = relationship('Contractor', back_populates='technician_offers')
    technicians = relationship('Technician', back_populates='technician_offers')

    def __repr__(self):
        return 'Technician Offer Model'

class Organizations(Base):

    __tablename__ = 'organizations'

    organization_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer,ForeignKey('subscription.subscription_id'))
    code_2fa_code = Column(String)
    
    stores=relationship('Store',back_populates='organizations')
    subscriptions=relationship('Subscription',back_populates='organizations')
    users=relationship('User',back_populates='organizations')

    def __repr__(self):
        return 'Organizations Model'

class Store(Base):

    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.organization_id'))
    branch = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    address = Column(String)
    gps_location = Column(String)


    organizations = relationship('Organizations', back_populates='stores')
    users = relationship('User', back_populates='stores')
    units=relationship('Unit', back_populates='stores')

    def __repr__(self):
        return 'Store Model'

# class Store_locations(Base):
#     __tablename__ = 'Store_locations'

#     store_id = Column(Integer, ForeignKey('Store.store_id'), primary_key=True)
#     gps_location = Column(String)

#     # store = relationship('Store', back_populates='store_locations')
# # 
#     def __repr__(self):
#         return f'Store_locations {self.store_id}'


class Cylinder(Base):

    __tablename__ = 'cylinder'

    cylinder_id = Column(Integer, primary_key=True)
    cylinder_size = Column(String)
    cylinder_type = Column(String, ForeignKey('cylinder_type.cylinder_type_id'))
    cylinder_weight = Column(String)
    added_date = Column(String)
    refrigerant_id = Column(Integer,ForeignKey('refrigerant.refrigerant_id'))
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    purchase_date = Column(String)
    supplier = Column(String)
    last_refill_date = Column(String)
    condition = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'))

    reclaim_recoveries=relationship('Reclaim_recovery',back_populates='cylinders')
    refrigerants=relationship('Refrigerant',back_populates='cylinders')
    technicians = relationship('Technician', back_populates='cylinders')
    tags = relationship('Tags', back_populates='cylinders')
    cylinder_types = relationship('Cylinder_type', back_populates='cylinders')


    def __repr__(self):
        return 'Cylinder Model'
    
class Cylinder_type(Base):

    __tablename__ = 'cylinder_type'

    cylinder_type_id = Column(Integer, primary_key=True)
    type_name = Column(String)

    cylinders= relationship('Cylinder', back_populates='cylinder_types')


    def __repr__(self):
        return 'Cylinder Model'

class Repairs(Base):

    __tablename__ = 'repairs'

    repair_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('unit.unit_id'))
    purchase_id = Column(Integer)
    repair_date = Column(String)
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    causes = Column(String)
    status = Column(String)

    units = relationship('Unit', back_populates='repairs')
    technicians = relationship('Technician', back_populates='repairs')
    ods_sheets=relationship('ODS_sheets',back_populates='repairs')


    def __repr__(self):
        return 'Repairs Model'

class Reclaim_recovery(Base):

    __tablename__ = 'reclaim_recovery'

    rec_id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer)
    tank_id = Column(Integer)
    unit_id = Column(Integer, ForeignKey('unit.unit_id'))
    gas_type = Column(String)
    quantity_before_in_lbs = Column(REAL)
    quantity_after_in_lbs = Column(REAL)
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    notes = Column(String)
    date = Column(String)
    status = Column(String)
    refrigerant_id = Column(Integer, ForeignKey('refrigerant.refrigerant_id'))
    cylinder_id = Column(Integer, ForeignKey('cylinder.cylinder_id'))

    ods_sheets=relationship('ODS_sheets',back_populates='reclaim_recoveries')
    units = relationship('Unit', back_populates='reclaim_recoveries')
    technicians = relationship('Technician', back_populates='reclaim_recoveries')
    cylinders = relationship('Cylinder', back_populates='reclaim_recoveries')
    refrigerants = relationship('Refrigerant', back_populates='reclaim_recoveries')

    def __repr__(self):
        return 'Reclaim_Recovery Model'

class Refrigerant(Base):

    __tablename__ = 'refrigerant'

    refrigerant_id = Column(Integer, primary_key=True)
    refrigerant_name = Column(String)
    list = Column(String)

    cylinders=relationship('Cylinder',back_populates='refrigerants')
    reclaim_recoveries=relationship('Reclaim_recovery',back_populates='refrigerants')


    def __repr__(self):
        return 'Refrigerant Model'
    
class Maintenance(Base):

    __tablename__ = 'maintenance'

    maintenance_id = Column(Integer, primary_key=True)
    technician_id=Column(Integer,ForeignKey('technician.technician_id'))
    unit_id=Column(Integer,ForeignKey('unit.unit_id'))
    log = Column(String)
    last_updated = Column(String)
    service_history=Column(String)
    maintenance_date=Column(String)
    maintenance_type=Column(String)
    parts_used=Column(String)
    notes=Column(String)

    maintenance_details=relationship('Maintenance_detail',back_populates='maintenances')
    units=relationship('Unit',back_populates='maintenances')
    technicians=relationship('Technician',back_populates='maintenances')



    def __repr__(self):
        return 'Refrigerant Model'
    
class Maintenance_detail(Base):

    __tablename__ = 'maintenance_detail'

    maintenance_detail_id = Column(Integer, primary_key=True)
    maintenance_id=Column(Integer,ForeignKey('maintenance.maintenance_id'))
    description = Column(String)
    status = Column(String)

    maintenances=relationship('Maintenance',back_populates='maintenance_details')


    def __repr__(self):
        return 'Refrigerant Model'
    

# Class CRUD with all important features to worth with the Database.
class CRUD:

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


