#Import this script to generate a unique ID for each cylinder QR Tag.
#Script to generate a unique ID for each cylinder QR Tag.
import uuid
import pandas as pd

class CylinderQRGenerator:
    @classmethod
    def generate_cylinder_unique_id(cls, cylinder_id):
        my_cylinder_id = str(cylinder_id)
        return my_cylinder_id + "C-" + str(uuid.uuid4())  # Adding a unique cylinder ID and "C" for cylinder
    
class EquipmentQRGenerator:
    @classmethod
    def generate_equipment_unique_id(cls, unit_id):
        my_equipment_id = str(unit_id)
        return my_equipment_id + "E-" + str(uuid.uuid4())
class technicianQRGenerator:
    @classmethod
    def generate_technician_unique_id(cls):
        return str(uuid.uuid4())
    
    if __name__ == '__main__':
        my_equipment_id = str(1)
        x = my_equipment_id + "E-" + str(uuid.uuid4())
        print(x)
        # df = pd.read_csv("RefrigerantTypeLookupData.csv")
        # # Convert all entries in 'refrigerant_name' column to lowercase
        # df['refrigerant_name'] = df['refrigerant_name'].str.lower()

        # # If you want to save the modified DataFrame to a new CSV file
        # df.to_csv('your_modified_file.csv', index=False)