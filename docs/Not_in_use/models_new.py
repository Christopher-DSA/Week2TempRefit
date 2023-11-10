from sqlalchemy import Column, String, Float, Integer, create_engine, ForeignKey, Date, BINARY, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()

# SQLAlcehmy base.
Base = declarative_base()

#Engine connection and sesion.
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

class User(Base):

    __tablename__ = "User"

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    email =  Column(String)
    password = Column(String)
    role = Column(String)
    enable_2_fa = Column(Boolean)

    def __repr__(self) -> str:
        return 'User model'

# Model Admin.
class Admin(Base):

    __tablename__ = "Admin"

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    name = Column(String)
    user_code = Column(Integer, ForeignKey('User.ID'), nullable= True)
    date = Column(String)
    user = relationship("User", backref="Admin")

    def __repr__(self):
        return 'Admin model'
    
# Model Tracking.
class Tracking(Base):

    __tablename__ = "Tracking"

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    entry_date = Column(String, nullable= True)
    user_code = Column(Integer, ForeignKey('User.ID'), nullable= True)
    ip_address = Column(String)
    user = relationship("User", backref="Tracking")

    def __repr__(self):
        return 'Tracking model'

# Model Person.
class Person(Base):

    __tablename__ = "Person"

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    name = Column(String)
    last_name = Column(String)
    birthdate = Column(String)
    gender = Column(String)

    def __repr__(self) -> str:
        return 'Person model'

# Model Company.
class Company(Base):

    __tablename__ = 'Company'

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    name = Column(String, unique= True)
    user_code = Column(Integer, ForeignKey('User.ID'), nullable= True)
    user = relationship("User", backref="Company")
    logo = Column(String)
    status = Column(Boolean, default= True)

    def __repr__(self) -> str:
        return 'Company model'

# Model Site.
class Site(Base):

    __tablename__ = 'Site'

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    company_code = Column(Integer, ForeignKey('Company.ID'), nullable= True)
    company = relationship("Company", backref="Site")
    site_name = Column(String)
    address = Column(String)
    province = Column(String)
    city = Column(String)
    postal_code = Column(String)
    telephone = Column(String)

    def __repr__(self):
        return 'Site model'

# Model Employee.
class Employee(Base):

    __tablename__ = 'Employee'

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    person_code = Column(Integer, ForeignKey('Person.ID'), nullable= True)
    person = relationship("Person", backref="Employee")
    company_code = Column(Integer, ForeignKey('Company.ID'), nullable= True)
    company = relationship("Company", backref="Employee")
    site_code = Column(Integer, ForeignKey('Site.ID'), nullable= True)
    site = relationship("Site", backref="Employee")
    user_code = Column(Integer, ForeignKey('User.ID'), nullable= True)
    user = relationship("User", backref="Employee")
    role = Column(String)
    date_begin = Column(String)
    date_end = Column(String)
    status = Column(Boolean, default= True)

    def __repr__(self):
        return 'Employee model'

# Model HealthRisk.
class HealthRisk(Base):

    __tablename__ = 'HealthRisk'

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    employee_code = Column(Integer, ForeignKey('Employee.ID'), nullable= True)
    employee = relationship("Employee", backref="HealthRisk")
    gender = Column(String)
    height_cm = Column(Float)
    height_inches = Column(Float)
    weight_kg = Column(Float)
    weight_lbs = Column(Float)
    bmi = Column(Float)
    waist = Column(Float)
    systolic = Column(Float)
    diastolic = Column(Float)
    fasted = Column(Boolean)
    total_cholesterol = Column(Float)
    hdl = Column(Float)
    bs = Column(Float)
    hba1c = Column(Float)
    date = Column(String)

    def __repr__(self) -> str:
        return 'HealthRisk model'

# Model HealthRiskGrade.
class HealthRiskGrade(Base):

    __tablename__ = 'HealthRiskGrade'

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable= True)
    source = Column(Integer, ForeignKey('HealthRisk.ID'), nullable= True)
    source_rel = relationship("HealthRisk", backref="HealthRiskGrade")
    weight_management_grade = Column(String)
    weight_management_value = Column(Float)
    blood_glucose_grade = Column(String)
    blood_glucose_value = Column(Float)
    blood_pressure_grade = Column(String)
    blood_pressure_value = Column(Float)
    overall_blood_lipid_panel_grade = Column(String)
    overall_blood_lipid_panel_value = Column(Float)
    tc_hdl_reading = Column(Float)
    overall_grade_grade = Column(String)
    overall_grade_value = Column(Float)
    first_access = Column(String)
    last_access = Column(String)
    date = Column(String)

    def __repr__(self) -> str:
        return 'Health Risk Grade model'

# Model LifeStyle.
class LifeStyle(Base):

    __tablename__ = 'LifeStyle'

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    employee_code = Column(Integer, ForeignKey('Employee.ID'), nullable= True)
    employee = relationship("Employee", backref="LifeStyle")
    nutrition = Column(Integer)
    physical_activity = Column(Integer)
    stretching = Column(Integer)
    sitting = Column(String)
    check_in = Column(String)
    sleep_quality = Column(Integer)
    sleep_hours = Column(Integer)
    mental_wellness = Column(Integer)
    stress_levels = Column(Integer)
    smoker = Column(Boolean)
    packs_per_week = Column(String)
    date = Column(String)

    def __repr__(self) -> str:
        return 'LifeStyle model'

# Model LifeStyleGrade.
class LifeStyleGrade(Base):

    __tablename__ = 'LifeStyleGrade'

    ID = Column(Integer, primary_key= True, autoincrement= True, nullable= True)
    source = Column(Integer, ForeignKey('LifeStyle.ID'), nullable= True)
    source_rel = relationship("LifeStyle", backref="LifeStyleGrade")
    total_value = Column(Float)
    total_grade = Column(String)
    nutrition = Column(Float)
    physical_activity = Column(Float)
    stretching = Column(Float)
    sitting = Column(Float)
    check_in = Column(Float)
    sleep_hours = Column(Float)
    sleep_quality = Column(Float)
    mental_wellness = Column(Float)
    stress_levels = Column(Float)
    smoker = Column(Float)
    packs_per_week = Column(Float)
    first_access = Column(String)
    last_access = Column(String)
    date = Column(String)
    
    def __repr__(self) -> str:
        return 'LifeStyle Grade model'

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
