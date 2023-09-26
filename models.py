from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, REAL, Text, DateTime, Sequence, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# SQLAlcehmy base.
Base = declarative_base()


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)



class User(Base):

    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String)
    user_detail = Column(String)
    status = Column(String)

    Technician = relationship('Technician', backref='User')
    Contractor = relationship('Contractor', backref='User')
    Refit_Admin = relationship('Refit_Admin', backref='User')
    wholesaler = relationship('Wholesaler', backref='User')
    user_detail = relationship('User_Detail', backref='User')
    organization = relationship('Organization', backref='User')
    store = relationship('Store', backref='User')
    user_logging = relationship('User_Logging', backref='User')

    def __repr__(self):
        return 'User model'
    

class User_Detail(Base):

    __tablename__ = "User_Detail"

    user_detail_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)
    user_id=Column(Integer,ForeignKey('User.user_id'), nullable= True)
    
    User = relationship('User', backref='user_details')

    def __repr__(self):
        return 'User Detail Model'

class Technician(Base):

    __tablename__ = "Technician"
    technician_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    
    ODS_licence_number = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable= True)
    contractor_id = Column(Integer,ForeignKey('Contractor.contractor_id'), nullable= True)
    date_begin = Column(String)
    date_end = Column(String)
    user_status = Column(String)
    contractor_status = Column(String)

    user = relationship('User', backref='Technician')
    unit = relationship('Unit', backref='Technician')
    ods_sheet = relationship('ODS_Sheet', backref='Technician')
    cylinder = relationship('Cylinder', backref='Technician')
    repair = relationship('Repair', backref='Technician')
    reclaim_recovery = relationship('Reclaim_Recovery', backref='Technician')
    technician_offer = relationship('Technician_offer', backref='Technician')
    maintenance = relationship('Maintenance', backref='Technician')
    contractor = relationship('Contractor', backref='Technician')


    def __repr__(self):
        return 'Technician Model'

class Contractor(Base):

    __tablename__ = "Contractor"

    contractor_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable= True)
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    user = relationship('User', backref='Contractor')
    technician = relationship('Technician', backref='Contractor')
    contractor_detail = relationship('Contractor_Detail', backref='Contractor')
    ods_sheet = relationship('ODS_Sheet', backref='Contractor')
    technician_offer = relationship('Technician_offer', backref='Contractor')

    def __repr__(self):
        return f'Contractor {self.contractor_id}'

class Contractor_Detail(Base):

    __tablename__ = "Contractor_Detail"

    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    contractor=relationship('Contractor', backref='Contractor_Detail')

    def __repr__(self):
        return f'Contractor_Detail {self.contractor_id}'

class Refit_Admin(Base):

    __tablename__ = "Refit_Admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id', nullable= True))
    status = Column(String)
    code_2fa_code = Column(String)
    admin_level = Column(Integer)

    user = relationship('User', backref='Refit_Admin')

    def __repr__(self):
        return 'Refit Admin Model'

class Tag(Base):

    __tablename__ = "Tag"

    tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    invoice_id = Column(Integer, ForeignKey('Invoice.invoice_id'), nullable= True)
    tag_number = Column(String)
    tag_url = Column(String)
    type = Column(String)
    cylinder_id = Column(Integer, ForeignKey('Cylinder.cylinder_id'), nullable= True)
    wholesaler_id = Column(Integer, ForeignKey('Wholesaler.wholesaler_id'), nullable= True)

    cylinder = relationship('Cylinder', backref='Tag')
    invoice  = relationship('Invoice', backref='Tag')
    wholesaler =relationship('Wholesaler',backref='Tag')
    ods_sheet =relationship('ODS_Sheet',backref='Tag')
    unit =relationship('Unit',backref='Tag')

    def __repr__(self):
        return 'Tag Model'

class Wholesaler(Base):

    __tablename__ = "Wholesaler"
    
    wholesaler_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable= True)
    status = Column(String)
    tag_id = Column(Integer, ForeignKey('tag.tag_id'), nullable= True)

    user = relationship('User', backref='Wholesaler')
    tag = relationship('Tag', backref='Wholesaler')


    def __repr__(self):
        return 'Wholesaler Model'

class Invoice(Base):

    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    subscription_id = Column(Integer, ForeignKey('subscription.subscription_id'))
    tag_id = Column(Integer, ForeignKey('tag.tag_id'))
    amount = Column(REAL)
    payment_method = Column(String)
    tax = Column(REAL)
    date = Column(String)

    Tag = relationship('Tag', backref='invoices', foreign_keys=[tag_id], remote_side='tag.tag_id')
    subscriptions=relationship('Subscription',backref='invoices')

    def __repr__(self):
        return 'Invoice Model'


class Subscription(Base):

    __tablename__ = "subscription"

    subscription_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    Start_date = Column(String)
    End_Date = Column(String)
    Package_size = Column(String)
    compliant = Column(String)

    invoices = relationship('Invoice', backref='subscriptions')
    Organization=relationship('Organization',backref='subscriptions')

    def __repr__(self):
        return 'Subscription Model'



class User_Logging(Base):

    __tablename__ = "user_logging"

    log_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    entry_date = Column(String)
    ip_address = Column(String)
    address_gps = Column(String)

    User = relationship('User', backref='user_loggings')

    def __repr__(self):
        return f'User_Logging {self.log_id}'


class Unit(Base):

    __tablename__ = "unit"
    
    unit_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    unit_name = Column(String)
    tag_id = Column(Integer, ForeignKey('tag.tag_id'))
    other_attribute = Column(String)
    installation_date = Column(String)
    last_maintenance_date = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    type_of_refrigerant = Column(String)
    factory_charge_amount = Column(Integer)
    unit_type = Column(String)
    store_id = Column(Integer,ForeignKey('store.store_id'))
    

    Technician = relationship('Technician', backref='units')
    Tag = relationship('Tag', backref='units')
    reclaim_recoveries=relationship('Reclaim_Recovery',backref='units')
    ods_sheets=relationship('ODS_Sheet',backref='units')
    Repair=relationship('Repair',backref='units')
    maintenances=relationship('Maintenance',backref='units')
    stores=relationship('Store',backref='units')

    def __repr__(self):
        return 'Unit Model'

class ODS_Sheet(Base):

    __tablename__ = "ods_sheet"
    
    ods_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    unit_id = Column(Integer, ForeignKey('unit.unit_id'))
    tag_id = Column(Integer, ForeignKey('tag.tag_id'))
    repair_id = Column(Integer, ForeignKey('repair.repair_id'))
    rec_id = Column(Integer, ForeignKey('reclaim_recovery.rec_id'))

    Contractor = relationship('Contractor', backref='ods_sheets')
    Technician = relationship('Technician', backref='ods_sheets')
    units = relationship('Unit', backref='ods_sheets')
    Tag = relationship('Tag', backref='ods_sheets')
    Repair = relationship('Repair', backref='ods_sheets')
    reclaim_recoveries = relationship('Reclaim_Recovery', backref='ods_sheets')


    def __repr__(self):
        return 'ODS_Sheet Model'

class Technician_offer(Base):

    __tablename__ = "technician_offer"

    technician_offer_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    offer_status = Column(String)
    email_time_sent = Column(String)

    Contractor = relationship('Contractor', backref='Technician_Offer')
    Technician = relationship('Technician', backref='technician_offers')

    def __repr__(self):
        return 'Technician Offer Model'

class Organization(Base):

    __tablename__ = "organization"

    organization_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer,ForeignKey('Subscription.subscription_id'))
    code_2fa_code = Column(String)
    
    store =relationship('Store',backref='Organization')
    subscription =relationship('Subscription',backref='Organization')
    User =relationship('User',backref='Organization')

    def __repr__(self):
        return 'Organization Model'

class Store(Base):

    __tablename__ = "Store"

    store_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    organization_id = Column(Integer, ForeignKey('organization.organization_id'))
    branch = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    address = Column(String)
    gps_location = Column(String)


    Organization = relationship('Organization', backref='stores')
    User = relationship('User', backref='stores')
    units=relationship('Unit', backref='stores')

    def __repr__(self):
        return 'Store Model'

class Store_Location(Base):
    
    __tablename__ = "store_location"
    store_location_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    store_id = Column(Integer, ForeignKey('store.store_id'))
    gps_location = Column(String)

    store = relationship('Store', backref='store_locations')

    def __repr__(self):
        return f'Store_Location {self.store_id}'


class Cylinder(Base):

    __tablename__ = "cylinder"

    cylinder_id = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    cylinder_size = Column(String)
    cylinder_type_id = Column(String, ForeignKey('cylinder_type.cylinder_type_id'))
    cylinder_weight = Column(String)
    added_date = Column(String)
    refrigerant_id = Column(Integer,ForeignKey('refrigerant.refrigerant_id'))
    technician_id = Column(Integer, ForeignKey('technician.technician_id'))
    purchase_date = Column(String)
    supplier = Column(String)
    last_refill_date = Column(String)
    condition = Column(String)
    tag_id = Column(Integer, ForeignKey('tag.tag_id'))

    reclaim_recoveries=relationship('Reclaim_Recovery',backref='Cylinder')
    refrigerants=relationship('Refrigerant',backref='Cylinder')
    Technician = relationship('Technician', backref='Cylinder')
    Tag = relationship('Tag', backref='Cylinder')
    cylinder_types = relationship('Cylinder_type', backref='Cylinder')


    def __repr__(self):
        return 'Cylinder Model'
    
class Cylinder_Type(Base):

    __tablename__ = "Cylinder_Type"

    cylinder_type_id = Column(Integer, primary_key=True)
    type_name = Column(String)

    cylinder= relationship('Cylinder', backref='Cylinder_Type')


    def __repr__(self):
        return 'Cylinder Model'

class Purchase(Base):

    __tablename__ = "Purchase"

    purchase_id = Column(Integer, primary_key=True)


    def __repr__(self):
        return 'Purchase Model'
    
class Repair(Base):

    __tablename__ = "Repair"

    repair_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    purchase_id = Column(Integer, ForeignKey('Purchase.purchase_id'))
    repair_date = Column(String)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    causes = Column(String)
    status = Column(String)

    units = relationship('Unit', backref='Repair')
    Technician = relationship('Technician', backref='Repair')
    ods_sheets=relationship('ODS_Sheet',backref='Repair')

    def __repr__(self):
        return 'Repair Model'

class Reclaim_Recovery(Base):

    __tablename__ = "Reclaim_Recovery"

    rec_id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('Purchase.purchase_id'))
    tank_id = Column(Integer, ForeignKey('Tank.tank_id'))
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    gas_type = Column(String)
    quantity_before_in_lbs = Column(REAL)
    quantity_after_in_lbs = Column(REAL)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    notes = Column(String)
    date = Column(String)
    status = Column(String)
    refrigerant_id = Column(Integer, ForeignKey('Refrigerant.refrigerant_id'))
    cylinder_id = Column(Integer, ForeignKey('Cylinder.cylinder_id'))

    ods_sheets=relationship('ODS_Sheet',backref='reclaim_recoveries')
    units = relationship('Unit', backref='reclaim_recoveries')
    Technician = relationship('Technician', backref='reclaim_recoveries')
    Cylinder = relationship('Cylinder', backref='reclaim_recoveries')
    refrigerants = relationship('Refrigerant', backref='reclaim_recoveries')

    def __repr__(self):
        return 'Reclaim_Recovery Model'

class Refrigerant(Base):

    __tablename__ = "refrigerant"

    refrigerant_id = Column(Integer, primary_key=True)
    refrigerant_name = Column(String)
    list = Column(String)

    Cylinder=relationship('Cylinder',backref='refrigerants')
    reclaim_recoveries=relationship('Reclaim_Recovery',backref='refrigerants')

    def __repr__(self):
        return 'Refrigerant Model'
    
class Maintenance(Base):

    __tablename__ = "maintenance"

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

    maintenance_details=relationship('Maintenance_Detail',backref='maintenances')
    units=relationship('Unit',backref='maintenances')
    Technician=relationship('Technician',backref='maintenances')

    def __repr__(self):
        return 'Maintenance Model'
    
class Maintenance_Detail(Base):

    __tablename__ = "maintenance_detail"

    maintenance_detail_id = Column(Integer, primary_key=True)
    maintenance_id=Column(Integer,ForeignKey('maintenance.maintenance_id'))
    description = Column(String)
    status = Column(String)

    maintenances=relationship('Maintenance',backref='maintenance_details')


    def __repr__(self):
        return 'Maintenance_Detail Model'
    
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


