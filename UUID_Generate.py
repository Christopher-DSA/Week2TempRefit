#Import this script to generate a unique ID for each cylinder QR Tag.
#Script to generate a unique ID for each cylinder QR Tag.
import uuid
import pandas as pd

class CylinderQRGenerator:
    @classmethod
    def generate_cylinder_unique_id(cls, cylinder_id):
        my_cylinder_id = str(cylinder_id)
        return my_cylinder_id + "C-" + str(uuid.uuid4())  # Adding a unique cylinder ID and "C" for cylinder
    
    
    
    if __name__ == '__main__':
        df = pd.read_csv("RefrigerantTypeLookupData.csv")
        # Convert all entries in 'refrigerant_name' column to lowercase
        df['refrigerant_name'] = df['refrigerant_name'].str.lower()

        # If you want to save the modified DataFrame to a new CSV file
        df.to_csv('your_modified_file.csv', index=False)