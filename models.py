from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, REAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy



db=SQLAlchemy()

Base = declarative_base()
Base.query = db.session.query_property()

engine = create_engine('sqlite:///database.db')
def get_session():
    Session=sessionmaker(bind=engine)
    return Session()



class CRUDMixin:
    @classmethod
    def get_user_by_email(cls, email):
        # Get the database session
        session=get_session()

        try:
            # Perform a query to find the user with the given email
            user = session.query(User).filter_by(email=email).first()
            return user
        except Exception as e:
            # Handle any errors that may occur during the query
            raise e
        finally:
            # Close the session
            session.close()
    @classmethod
    def create(cls, model, **kwargs):
        # Create a new instance of the model with the given attributes
        new_instance = model(**kwargs)

        # Get the database session
        session = get_session()
        # session = Session()

        try:
            # Add the new instance to the session and commit changes
            session.add(new_instance)
            session.commit()
            return new_instance
        except Exception as e:
            # Rollback the session in case of any errors
            session.rollback()
            raise e
        finally:
            # Close the session
            session.close()

    

    @classmethod
    # def read(cls, model_class, instance_id):
    #     return model_class.query.get(instance_id)
    def read(cls, model_class, *args, **kwargs):
        session = get_session()
        query = session.query(model_class)

        if args:
            query = query.filter(*args)

        if kwargs:
            query = query.filter_by(**kwargs)

        return query.all()
        
        

    @classmethod
    def update(cls, model_class, instance_id, **kwargs):
        session = get_session()

        instance = session.query(model_class).get(instance_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance,key, value)
        session.commit()
        return instance

        

    @classmethod
    def delete(cls, model_class, instance_id):
        session = get_session()
        instance = session.query(model_class).get(instance_id)

        if instance:
            session.delete(instance)
            session.commit()
            return True
        else:
            return False


class User(Base, CRUDMixin):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String)
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
        return f'User {self.user_id}'
    

class User_detail(Base, CRUDMixin):
    __tablename__ = 'User_detail'

    user_detail_id = Column(Integer, primary_key=True)
    ODS_license_number = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    birthdate = Column(String)
    gender = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)
    user_id=Column(Integer,ForeignKey('User.user_id'))
    users = relationship('User', back_populates='user_details')

    def __repr__(self):
        return f'User_detail {self.user_id}'

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

    users = relationship('User', back_populates='technicians')
    units = relationship('Unit', back_populates='technicians')
    ods_sheets = relationship('ODS_Sheets', back_populates='technicians')
    cylinders = relationship('Cylinder', back_populates='technicians')
    repairs = relationship('Repairs', back_populates='technicians')
    reclaim_recoveries = relationship('Reclaim_Recovery', back_populates='technicians')
    technician_offers = relationship('Technician_offer', back_populates='technicians')
    maintenances = relationship('Maintenance', back_populates='technicians')



    def __repr__(self):
        return f'Technician {self.technician_id}'

class Contractor(Base, CRUDMixin):
    __tablename__ = 'Contractor'
    contractor_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)

    users = relationship('User', back_populates='contractors')
# #     technicians = relationship('Technician', back_populates='contractor')
    contractor_details = relationship('Contractor_Detail', back_populates='contractors')
    ods_sheets = relationship('ODS_Sheets', back_populates='contractors')
    technician_offers = relationship('Technician_offer', back_populates='contractors')

    def __repr__(self):
        return f'Contractor {self.contractor_id}'

class Refit_admin(Base, CRUDMixin):
    __tablename__ = 'Refit_admin'
    admin_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    status = Column(String)
    code_2fa_code = Column(String)
    admin_level = Column(Integer)

    users = relationship('User', back_populates='refit_admins')

    def __repr__(self):
        return f'Refit_admin {self.admin_id}'

class Wholesaler(Base, CRUDMixin):
    __tablename__ = 'Wholesaler'
    wholesaler_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    status = Column(String)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

    users = relationship('User', back_populates='wholesalers')
    tags = relationship('Tags', back_populates='wholesalers')

    def __repr__(self):
        return f'Wholesaler {self.wholesaler_id}'

class Tags(Base, CRUDMixin):
    __tablename__ = 'Tags'

    tag_id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('Invoices.invoice_id'))
    tag_number = Column(String)
    tag_url = Column(String)
    type = Column(String)
    cylinder_id = Column(Integer)

    invoices = relationship('Invoices', back_populates='tags', foreign_keys=[invoice_id])
    wholesalers=relationship('Wholesaler',back_populates='tags')
    ods_sheets=relationship('ODS_Sheets',back_populates='tags')
    cylinders=relationship('Cylinder',back_populates='tags')
    units=relationship('Unit',back_populates='tags')

    def __repr__(self):
        return f'Tags {self.tag_id}'


class Invoices(Base, CRUDMixin):
    __tablename__ = 'Invoices'
    invoice_id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'))
    tag_id = Column(Integer)
    amount = Column(REAL)
    payment_method = Column(String)
    tax = Column(REAL)
    date = Column(String)

    tags = relationship('Tags', back_populates='invoices')
    subscriptions=relationship('Subscription',back_populates='invoices')

    def __repr__(self):
        return f'Invoices {self.invoice_id}'


class Subscription(Base, CRUDMixin):
    __tablename__ = 'Subscription'
    subscription_id = Column(Integer, primary_key=True)
    Start_date = Column(String)
    End_Date = Column(String)
    Package_size = Column(String)
    compliant = Column(String)

    invoices = relationship('Invoices', back_populates='subscriptions')
    organizations=relationship('Organizations',back_populates='subscriptions')

    def __repr__(self):
        return f'Subscription {self.subscription_id}'

class Contractor_Detail(Base, CRUDMixin):
    __tablename__ = 'Contractor_Detail'

    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    contractors=relationship('Contractor', back_populates='contractor_details')

    def __repr__(self):
        return f'Contractor_Detail {self.contractor_id}'


# class User_logging(Base, CRUDMixin):
#     __tablename__ = 'USER_LOGGING'
#     log_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('User.user_id'))
#     entry_date = Column(String)
#     ip_address = Column(String)
#     address_gps = Column(String)

#     users = relationship('User', back_populates='user_loggings')

#     def __repr__(self):
#         return f'User_logging {self.log_id}'






class Unit(Base, CRUDMixin):
    __tablename__ = 'Unit'
    unit_id = Column(Integer, primary_key=True)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    unit_name = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
    other_attribute = Column(String)
    installation_date = Column(String)
    last_maintenance_date = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    type_of_refrigerant = Column(String)
    factory_charge_amount = Column(Integer)
    unit_type = Column(String)
    store_id = Column(String)

    technicians = relationship('Technician', back_populates='units')
    tags = relationship('Tags', back_populates='units')
    reclaim_recoveries=relationship('Reclaim_Recovery',back_populates='units')
    ods_sheets=relationship('ODS_Sheets',back_populates='units')
    repairs=relationship('Repairs',back_populates='units')
    maintenances=relationship('Maintenance',back_populates='units')




    def __repr__(self):
        return f'Unit {self.unit_id}'

class ODS_Sheets(Base, CRUDMixin):
    __tablename__ = 'ODS_Sheets'
    ods_id = Column(Integer, primary_key=True)
    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
    repair_id = Column(Integer, ForeignKey('Repairs.repair_id'))
    rec_id = Column(Integer, ForeignKey('Reclaim_Recovery.rec_id'))

    contractors = relationship('Contractor', back_populates='ods_sheets')
    technicians = relationship('Technician', back_populates='ods_sheets')
    units = relationship('Unit', back_populates='ods_sheets')
    tags = relationship('Tags', back_populates='ods_sheets')
    repairs = relationship('Repairs', back_populates='ods_sheets')
    reclaim_recoveries = relationship('Reclaim_Recovery', back_populates='ods_sheets')


    def __repr__(self):
        return f'ODS_Sheets {self.ods_id}'

class Technician_offer(Base, CRUDMixin):
    __tablename__ = 'technician_offer'
    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'), primary_key=True)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'), primary_key=True)
    offer_status = Column(String)
    email_time_sent = Column(String)

    contractors = relationship('Contractor', back_populates='technician_offers')
    technicians = relationship('Technician', back_populates='technician_offers')

    def __repr__(self):
        return f'Technician_offer {self.contractor_id}, {self.technician_id}'

class Organizations(Base, CRUDMixin):
    __tablename__ = 'Organizations'
    organization_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer,ForeignKey('Subscription.subscription_id'))
    code_2fa_code = Column(String)
    
    stores=relationship('Store',back_populates='organizations')
    subscriptions=relationship('Subscription',back_populates='organizations')
    users=relationship(User,back_populates='organizations')

    def __repr__(self):
        return f'Organizations {self.organization_id}'

class Store(Base, CRUDMixin):
    __tablename__ = 'Store'
    store_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('Organizations.organization_id'))
    branch = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    address = Column(String)

    organizations = relationship('Organizations', back_populates='stores')
    users = relationship('User', back_populates='stores')

    def __repr__(self):
        return f'Store {self.store_id}'

class Store_locations(Base, CRUDMixin):
    __tablename__ = 'Store_locations'

    store_id = Column(Integer, ForeignKey('Store.store_id'), primary_key=True)
    gps_location = Column(String)

    # store = relationship('Store', back_populates='store_locations')
# 
    def __repr__(self):
        return f'Store_locations {self.store_id}'


class Cylinder(Base, CRUDMixin):
    __tablename__ = 'Cylinder'
    cylinder_id = Column(Integer, primary_key=True)
    cylinder_size = Column(String)
    cylinder_type = Column(String)
    cylinder_weight = Column(String)
    added_date = Column(String)
    refrigerant_id = Column(Integer,ForeignKey('Refrigerant.refrigerant_id'))
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    purchase_date = Column(String)
    supplier = Column(String)
    last_refill_date = Column(String)
    condition = Column(String)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

    reclaim_recoveries=relationship('Reclaim_Recovery',back_populates='cylinders')
    refrigerants=relationship('Refrigerant',back_populates='cylinders')
    technicians = relationship('Technician', back_populates='cylinders')
    tags = relationship('Tags', back_populates='cylinders')

    def __repr__(self):
        return f'Cylinder {self.cylinder_id}'

class Repairs(Base, CRUDMixin):
    __tablename__ = 'Repairs'
    repair_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    purchase_id = Column(Integer)
    repair_date = Column(String)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    causes = Column(String)
    status = Column(String)

    units = relationship('Unit', back_populates='repairs')
    technicians = relationship('Technician', back_populates='repairs')
    ods_sheets=relationship('ODS_Sheets',back_populates='repairs')


    def __repr__(self):
        return f'Repairs {self.repair_id}'

class Reclaim_Recovery(Base, CRUDMixin):
    __tablename__ = 'Reclaim_Recovery'
    rec_id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer)
    tank_id = Column(Integer)
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

    ods_sheets=relationship('ODS_Sheets',back_populates='reclaim_recoveries')
    units = relationship('Unit', back_populates='reclaim_recoveries')
    technicians = relationship('Technician', back_populates='reclaim_recoveries')
    cylinders = relationship('Cylinder', back_populates='reclaim_recoveries')
    refrigerants = relationship('Refrigerant', back_populates='reclaim_recoveries')

    def __repr__(self):
        return f'Reclaim_Recovery {self.rec_id}'

class Refrigerant(Base, CRUDMixin):
    __tablename__ = 'Refrigerant'
    refrigerant_id = Column(Integer, primary_key=True)
    refrigerant_name = Column(String)
    list = Column(String)

    cylinders=relationship('Cylinder',back_populates='refrigerants')
    reclaim_recoveries=relationship('Reclaim_Recovery',back_populates='refrigerants')


    def __repr__(self):
        return f'Refrigerant {self.refrigerant_id}'
    
class Maintenance(Base, CRUDMixin):
    __tablename__ = 'Maintenance'
    maintenance_id = Column(Integer, primary_key=True)
    technician_id=Column(Integer,ForeignKey('Technician.technician_id'))
    unit_id=Column(Integer,ForeignKey('Unit.unit_id'))
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
        return f'Refrigerant {self.maintenance_id}'
    
class Maintenance_detail(Base, CRUDMixin):
    __tablename__ = 'Maintenance_detail'
    maintenance_detail_id = Column(Integer, primary_key=True)
    maintenance_id=Column(Integer,ForeignKey('Maintenance.maintenance_id'))
    description = Column(String)
    status = Column(String)

    maintenances=relationship('Maintenance',back_populates='maintenance_details')





    def __repr__(self):
        return f'Refrigerant {self.refrigerant_id}'
    



