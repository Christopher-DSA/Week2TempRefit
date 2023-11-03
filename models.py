# In each table, one forignkey go with one relationship, other relationships should be deleted as they are duplicated from the reference table.
# From user to company, in the user table, there should be empty, but in the user table, it shpould be a forignkey and a relationship.
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    REAL,
    Text,
    DateTime,
    Sequence,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# SQLAlcehmy base.
Base = declarative_base()


engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    added_date = Column(String)
    user_detail = Column(String)
    status = Column(String)

    def __repr__(self):
        return "User model"


class User_Detail(Base):
    __tablename__ = "User_Detail"

    user_detail_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)

    user = relationship("User", backref="User_Detail")

    def __repr__(self):
        return "User Detail Model"


class Technician(Base):
    __tablename__ = "Technician"
    technician_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    ods_licence_number = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    contractor_id = Column(
        Integer, ForeignKey("Contractor.contractor_id"), nullable=True
    )
    date_begin = Column(String)
    date_end = Column(String)
    user_status = Column(String)
    contractor_status = Column(String)

    user = relationship("User", backref="Technician")
    contractor = relationship("Contractor", backref="Technician")

    def __repr__(self):
        return "Technician Model"


class Contractor(Base):
    __tablename__ = "Contractor"

    contractor_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(Integer)
    code_2fa_code = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    user = relationship("User", backref="Contractor")

    def __repr__(self):
        return f"Contractor {self.contractor_id}"


class Contractor_Detail(Base):
    __tablename__ = "Contractor_Detail"

    contractor_detail_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    contractor_id = Column(
        Integer, ForeignKey("Contractor.contractor_id"), nullable=True
    )
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    employees = Column(Integer)
    are_they_tracking_refrigerant = Column(String)
    time_basis = Column(String)

    contractor = relationship("Contractor", backref="Contractor_Detail")

    def __repr__(self):
        return f"Contractor Detail Model"


class Admin(Base):
    __tablename__ = "Admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    status = Column(String)
    code_2fa_code = Column(String)
    admin_level = Column(Integer)

    # Define the relationship with the User table and specify the backref attribute
    user = relationship("User", backref="Admin")

    def __repr__(self):
        return "Refit Admin Model"


class Tag(Base):
    __tablename__ = "Tag"

    tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    invoice_id = Column(Integer, ForeignKey("Invoice.invoice_id"), nullable=True)
    tag_number = Column(String)
    tag_url = Column(String)
    type = Column(String)
    cylinder_id = Column(Integer, ForeignKey("Cylinder.cylinder_id"), nullable=True)
    wholesaler_id = Column(
        Integer, ForeignKey("Wholesaler.wholesaler_id"), nullable=True
    )

    cylinder = relationship("Cylinder", backref="Tag")
    invoice = relationship("Invoice", backref="Tag")
    wholesaler = relationship("Wholesaler", backref="Tag")

    def __repr__(self):
        return "Tag Model"


class Wholesaler(Base):
    __tablename__ = "Wholesaler"

    wholesaler_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    status = Column(String)

    user = relationship("User", backref="Wholesaler")

    def __repr__(self):
        return "Wholesaler Model"


class Invoice(Base):
    __tablename__ = "Invoice"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    subscription_id = Column(
        Integer, ForeignKey("Subscription.subscription_id"), nullable=True
    )
    amount = Column(REAL)
    payment_method = Column(String)
    tax = Column(REAL)
    date = Column(String)

    subscription = relationship("Subscription", backref="Invoice")

    def __repr__(self):
        return "Invoice Model"


class Subscription(Base):
    __tablename__ = "Subscription"

    subscription_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    start_date = Column(String)
    end_Date = Column(String)
    package_size = Column(String)
    compliant = Column(String)

    def __repr__(self):
        return "Subscription Model"


class User_Logging(Base):
    __tablename__ = "User_Logging"

    log_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    entry_date = Column(String)
    ip_address = Column(String)
    address_gps = Column(String)

    user = relationship("User", backref="User_Logging")

    def __repr__(self):
        return f"User Logging Model"


class Unit(Base):
    __tablename__ = "Unit"

    unit_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    unit_name = Column(String)
    tag_id = Column(Integer, ForeignKey("Tag.tag_id"), nullable=True)
    other_attribute = Column(String)
    installation_date = Column(String)
    last_maintenance_date = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    type_of_refrigerant = Column(String)
    factory_charge_amount = Column(Integer)
    unit_type = Column(String)
    store_id = Column(Integer, ForeignKey("Store.store_id"), nullable=True)

    technician = relationship("Technician", backref="Unit")
    tag = relationship("Tag", backref="Unit")
    store = relationship("Store", backref="Unit")

    def __repr__(self):
        return "Unit Model"


class ODS_Sheet(Base):
    __tablename__ = "ODS_Sheet"

    ods_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    contractor_id = Column(
        Integer, ForeignKey("Contractor.contractor_id"), nullable=True
    )
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    unit_id = Column(Integer, ForeignKey("Unit.unit_id"), nullable=True)
    tag_id = Column(Integer, ForeignKey("Tag.tag_id"), nullable=True)
    repair_id = Column(Integer, ForeignKey("Repair.repair_id"), nullable=True)
    rec_id = Column(Integer, ForeignKey("Reclaim_Recovery.rec_id"), nullable=True)

    contractor = relationship("Contractor", backref="ODS_Sheet")
    technician = relationship("Technician", backref="ODS_Sheet")
    unit = relationship("Unit", backref="ODS_Sheet")
    tag = relationship("Tag", backref="ODS_Sheet")
    repair = relationship("Repair", backref="ODS_Sheet")
    reclaim_recoveries = relationship("Reclaim_Recovery", backref="ODS_Sheet")

    def __repr__(self):
        return "ODS Sheet Model"


class Technician_Offer(Base):
    __tablename__ = "Technician_Offer"

    technician_offer_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    contractor_id = Column(
        Integer, ForeignKey("Contractor.contractor_id"), nullable=True
    )
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    offer_status = Column(String)
    email_time_sent = Column(String)

    contractor = relationship("Contractor", backref="Technician_Offer")
    technician = relationship("Technician", backref="Technician_Offer")

    def __repr__(self):
        return "Technician Offer Model"


class Technician_Own_Company(Base):
    __tablename__ = "Technician_Own_Company"

    to_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    name = Column(String)
    branch_nm = Column(String)
    phone_nm = Column(String)
    ods_rece_email = Column(String)
    address = Column(String)
    apartment = Column(String)
    city = Column(String)
    province = Column(String)
    postal_code = Column(String)
    technician = relationship("Technician", backref="Technician_Own_Company")

    def __repr__(self):
        return "Technician Own Company Model"


class Organization(Base):
    __tablename__ = "Organization"

    organization_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    logo = Column(String)
    status = Column(String)
    subscription_id = Column(
        Integer, ForeignKey("Subscription.subscription_id"), nullable=True
    )
    code_2fa_code = Column(String)

    subscription = relationship("Subscription", backref="Organization")
    User = relationship("User", backref="Organization")

    def __repr__(self):
        return "Organization Model"


class Store(Base):
    __tablename__ = "Store"

    store_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    organization_id = Column(
        Integer, ForeignKey("Organization.organization_id"), nullable=True
    )
    branch = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=True)
    address = Column(String)
    gps_location = Column(String)

    organization = relationship("Organization", backref="Store")
    user = relationship("User", backref="Store")

    def __repr__(self):
        return "Store Model"


class Store_Location(Base):
    __tablename__ = "Store_Location"

    store_location_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    store_id = Column(Integer, ForeignKey("Store.store_id"), nullable=True)
    gps_location = Column(String)

    store = relationship("Store", backref="Store_Location")

    def __repr__(self):
        return f"Store Location Model"


class Cylinder(Base):
    __tablename__ = "Cylinder"

    cylinder_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    cylinder_size = Column(String)
    cylinder_type_id = Column(
        String, ForeignKey("Cylinder_Type.cylinder_type_id"), nullable=True
    )
    cylinder_weight = Column(String)
    added_date = Column(String)
    refrigerant_id = Column(
        Integer, ForeignKey("Refrigerant.refrigerant_id"), nullable=True
    )
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    purchase_date = Column(String)
    supplier = Column(String)
    last_refill_date = Column(String)
    condition = Column(String)

    refrigerants = relationship("Refrigerant", backref="Cylinder")
    technician = relationship("Technician", backref="Cylinder")
    cylinder_types = relationship("Cylinder_Type", backref="Cylinder")

    def __repr__(self):
        return "Cylinder Model"


class Cylinder_Type(Base):
    __tablename__ = "Cylinder_Type"

    cylinder_type_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    type_name = Column(String)

    def __repr__(self):
        return "Cylinder Type Model"


class Purchase(Base):
    __tablename__ = "Purchase"

    purchase_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    def __repr__(self):
        return "Purchase Model"


class Repair(Base):
    __tablename__ = "Repair"

    repair_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    unit_id = Column(Integer, ForeignKey("Unit.unit_id"), nullable=True)
    purchase_id = Column(Integer, ForeignKey("Purchase.purchase_id"), nullable=True)
    repair_date = Column(String)
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    causes = Column(String)
    status = Column(String)

    unit = relationship("Unit", backref="Repair")
    technician = relationship("Technician", backref="Repair")
    purchase = relationship("Purchase", backref="Repair")

    def __repr__(self):
        return "Repair Model"


class Tank(Base):
    __tablename__ = "Tank"
    tank_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    def __repr__(self):
        return "Tank Model"


class Reclaim_Recovery(Base):
    __tablename__ = "Reclaim_Recovery"

    rec_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    purchase_id = Column(Integer, ForeignKey("Purchase.purchase_id"), nullable=True)
    tank_id = Column(Integer, ForeignKey("Tank.tank_id"), nullable=True)
    unit_id = Column(Integer, ForeignKey("Unit.unit_id"), nullable=True)
    gas_type = Column(String)
    quantity_before_in_lbs = Column(REAL)
    quantity_after_in_lbs = Column(REAL)
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    notes = Column(String)
    date = Column(String)
    status = Column(String)
    refrigerant_id = Column(
        Integer, ForeignKey("Refrigerant.refrigerant_id"), nullable=True
    )
    cylinder_id = Column(Integer, ForeignKey("Cylinder.cylinder_id"), nullable=True)

    purchase = relationship("Purchase", backref="Reclaim_Recovery")
    unit = relationship("Unit", backref="Reclaim_Recovery")
    tank = relationship("Tank", backref="Reclaim_Recovery")
    technician = relationship("Technician", backref="Reclaim_Recovery")
    cylinder = relationship("Cylinder", backref="Reclaim_Recovery")
    refrigerant = relationship("Refrigerant", backref="Reclaim_Recovery")

    def __repr__(self):
        return "Reclaim Recovery Model"


class Refrigerant(Base):
    __tablename__ = "Refrigerant"

    refrigerant_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    refrigerant_name = Column(String)
    list = Column(String)

    def __repr__(self):
        return "Refrigerant Model"


class Maintenance(Base):
    __tablename__ = "Maintenance"

    maintenance_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    technician_id = Column(
        Integer, ForeignKey("Technician.technician_id"), nullable=True
    )
    unit_id = Column(Integer, ForeignKey("Unit.unit_id"), nullable=True)
    log = Column(String)
    last_updated = Column(String)
    service_history = Column(String)
    maintenance_date = Column(String)
    maintenance_type = Column(String)
    parts_used = Column(String)
    notes = Column(String)

    unit = relationship("Unit", backref="Maintenance")
    technician = relationship("Technician", backref="Maintenance")

    def __repr__(self):
        return "Maintenance Model"


class Maintenance_Detail(Base):
    __tablename__ = "Maintenance_Detail"

    maintenance_detail_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    maintenance_id = Column(
        Integer, ForeignKey("Maintenance.maintenance_id"), nullable=True
    )
    description = Column(String)
    status = Column(String)

    maintenance = relationship("Maintenance", backref="Maintenance_Detail")

    def __repr__(self):
        return "Maintenance Detail Model"


# Class CRUD with all important features to worth with the Database.
class CRUD:

    """This class is the main CRUD class with methods to create, read, update, and delete records.
    Here all methods are classmethods which means there is no necessary to use the class constructor.
    """

    # Constructor.
    def __init__(self, model, **kargs) -> None:
        self.model = model(**kargs)

    # Database model printing.
    def __repr__(self):
        return f"< model= **{self.model}** >"

    # Method to create a record.
    @classmethod
    def create(cls, model, rollback=False, **kargs):
        """This classmethod has the main function of creating a record, it receives the model class, the rollback argument, which
        is just for testing, and the arguments for the class model, such as name= 'My name', email= 'myemail@something.com'...
        """

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
    def read(
        cls,
        model,
        all=False,
        latest_field=None,
        count_only=False,
        relative_match=None,
        order_by=False,
        **kwargs,
    ):
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
                    q = (
                        session.query(model)
                        .filter_by(**kwargs)
                        .order_by(model.date.asc())
                        .all()
                    )
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
        """Update classmethod is used to update records, it receives the model, the attribute(attr) argument which we want to
        update within the record, the new argument, which is the new input, and the arguments to find the record we want to
        modify. As an example for Admin -> Admin, 'name', new= 'New name', name= 'my name', it will search the first record
        with the name; then, it will replace the field name with the new input 'New name'.
        """

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

        print("updated")

    # Method to delete records within the database.
    @classmethod
    def delete(self, model, **kwargs):
        """Delete classmethod is to delete records within the database, it receives the model which is the class model,
        and the arguments to get this record, as an example. Admin -> Admin, 'name'= 'my name', 'password'= 'pass'
        . It will delete the first record which matches the criterion."""

        session = Session()

        record = session.query(model).filter_by(**kwargs).first()

        # Deleting the record.
        session.delete(record)
        # Deleting the record within the database.
        session.commit()

        # Closing the session.
        session.close()

        print("Deleted")
