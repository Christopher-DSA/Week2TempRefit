from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, REAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String)
    user_detail = Column(String)
    status = Column(String)

    technicians = relationship('Technician', backref='user')
    contractors = relationship('Contractor', backref='user')
    refit_admins = relationship('Refit_admin', backref='user')
    wholesalers = relationship('Wholesaler', backref='user')
    user_details = relationship('User_detail', backref='user')
    organizations = relationship('Organizations', backref='user')
    stores = relationship('Store', backref='user')
    user_logging = relationship('USER_LOGGING', backref='user')

    def __repr__(self):
        return f'User {self.user_id}'

class Technician(Base):
    __tablename__ = 'Technician'
    technician_id = Column(Integer, primary_key=True)
    user_detail = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    contractor_id = Column(Integer)
    date_begin = Column(String)
    date_end = Column(String)
    user_status = Column(String)
    contractor_status = Column(String)

    user = relationship('User', backref='technicians')
    units = relationship('Unit', backref='technician')
    ods_sheets = relationship('ODS_Sheets', backref='technician')
    cylinders = relationship('Cylinder', backref='technician')
    repairs = relationship('Repairs', backref='technician')
    reclaim_recoveries = relationship('Reclaim_Recovery', backref='technician')

    def __repr__(self):
        return f'Technician {self.technician_id}'

class Contractor(Base):
    __tablename__ = 'Contractor'
    contractor_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)

    user = relationship('User', backref='contractors')
    technicians = relationship('Technician', backref='contractor')
    contractor_details = relationship('Contractor_Detail', backref='contractor')
    ods_sheets = relationship('ODS_Sheets', backref='contractor')
    technician_offers = relationship('technician_offer', backref='contractor')

    def __repr__(self):
        return f'Contractor {self.contractor_id}'

class Refit_admin(Base):
    __tablename__ = 'Refit_admin'
    admin_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    status = Column(String)
    code_2fa_code = Column(String)
    admin_level = Column(Integer)

    user = relationship('User', backref='refit_admins')

    def __repr__(self):
        return f'Refit_admin {self.admin_id}'

class Wholesaler(Base):
    __tablename__ = 'Wholesaler'
    wholesaler_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    status = Column(String)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

    user = relationship('User', backref='wholesalers')
    tag = relationship('Tags', backref='wholesalers')

    def __repr__(self):
        return f'Wholesaler {self.wholesaler_id}'

class Invoices(Base):
    __tablename__ = 'Invoices'
    invoice_id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'))
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
    amount = Column(REAL)
    payment_method = Column(String)
    tax = Column(REAL)
    date = Column(String)

    subscription = relationship('Subscription', backref='invoices')
    tag = relationship('Tags', backref='invoices')

    def __repr__(self):
        return f'Invoices {self.invoice_id}'

class Subscription(Base):
    __tablename__ = 'Subscription'
    subscription_id = Column(Integer, primary_key=True)
    Start_date = Column(String)
    End_Date = Column(String)
    Package_size = Column(String)
    compliant = Column(String)

    invoices = relationship('Invoices', backref='subscription')

    def __repr__(self):
        return f'Subscription {self.subscription_id}'

class Contractor_Detail(Base):
    __tablename__ = 'Contractor_Detail'

    contractor_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    def __repr__(self):
        return f'Contractor_Detail {self.contractor_id}'

class Tags(Base):
    __tablename__ = 'Tags'
    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String)

    def __repr__(self):
        return f'Tags {self.tag_id}'

class User_logging(Base):
    __tablename__ = 'USER LOGGING'
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    entry_date = Column(String)
    ip_address = Column(String)
    address_gps = Column(String)

    user = relationship('User', backref='user_logging')

    def __repr__(self):
        return f'User_logging {self.log_id}'

class User_detail(Base):
    __tablename__ = 'User_detail'

    user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
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

    user = relationship('User', backref='user_details')

    def __repr__(self):
        return f'User_detail {self.user_id}'


class Unit(Base):
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

    technician = relationship('Technician', backref='units')
    tag = relationship('Tags', backref='units')

    def __repr__(self):
        return f'Unit {self.unit_id}'

class ODS_Sheets(Base):
    __tablename__ = 'ODS_Sheets'
    ods_id = Column(Integer, primary_key=True)
    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))
    repair_id = Column(Integer)
    rec_id = Column(Integer)

    contractor = relationship('Contractor', backref='ods_sheets')
    technician = relationship('Technician', backref='ods_sheets')
    unit = relationship('Unit', backref='ods_sheets')
    tag = relationship('Tags', backref='ods_sheets')

    def __repr__(self):
        return f'ODS_Sheets {self.ods_id}'

class Technician_offer(Base):
    __tablename__ = 'technician_offer'
    contractor_id = Column(Integer, ForeignKey('Contractor.contractor_id'))
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    offer_status = Column(String)
    email_time_sent = Column(String)

    contractor = relationship('Contractor', backref='technician_offers')
    technician = relationship('Technician', backref='technician_offers')

    def __repr__(self):
        return f'Technician_offer {self.contractor_id}, {self.technician_id}'

class Organizations(Base):
    __tablename__ = 'Organizations'
    organization_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)

    user = relationship('User', backref='organizations')

    def __repr__(self):
        return f'Organizations {self.organization_id}'

class Store(Base):
    __tablename__ = 'Store'
    store_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('Organizations.organization_id'))
    branch = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    address = Column(String)

    organization = relationship('Organizations', backref='stores')
    user = relationship('User', backref='stores')

    def __repr__(self):
        return f'Store {self.store_id}'

class Store_locations(Base):
    __tablename__ = 'Store_locations'

    store_id = Column(Integer, ForeignKey('Store.store_id'), primary_key=True)
    gps_location = Column(String)

    store = relationship('Store', backref='store_locations')

    def __repr__(self):
        return f'Store_locations {self.store_id}'


class Cylinder(Base):
    __tablename__ = 'Cylinder'
    cylinder_id = Column(Integer, primary_key=True)
    cylinder_size = Column(String)
    cylinder_type = Column(String)
    cylinder_weight = Column(String)
    added_date = Column(String)
    refrigerant_id = Column(Integer)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    purchase_date = Column(String)
    supplier = Column(String)
    last_refill_date = Column(String)
    condition = Column(String)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'))

    technician = relationship('Technician', backref='cylinders')
    tag = relationship('Tags', backref='cylinders')

    def __repr__(self):
        return f'Cylinder {self.cylinder_id}'

class Repairs(Base):
    __tablename__ = 'Repairs'
    repair_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('Unit.unit_id'))
    purchase_id = Column(Integer)
    repair_date = Column(String)
    technician_id = Column(Integer, ForeignKey('Technician.technician_id'))
    causes = Column(String)
    status = Column(String)

    unit = relationship('Unit', backref='repairs')
    technician = relationship('Technician', backref='repairs')

    def __repr__(self):
        return f'Repairs {self.repair_id}'

class Reclaim_Recovery(Base):
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
    refrigerant_id = Column(Integer)
    cylinder_id = Column(Integer, ForeignKey('Cylinder.cylinder_id'))

    unit = relationship('Unit', backref='reclaim_recoveries')
    technician = relationship('Technician', backref='reclaim_recoveries')
    cylinder = relationship('Cylinder', backref='reclaim_recoveries')

    def __repr__(self):
        return f'Reclaim_Recovery {self.rec_id}'

class Refrigerant(Base):
    __tablename__ = 'Refrigerant'
    refrigerant_id = Column(Integer, primary_key=True)
    refrigerant_name = Column(String)
    list = Column(String)

    def __repr__(self):
        return f'Refrigerant {self.refrigerant_id}'


