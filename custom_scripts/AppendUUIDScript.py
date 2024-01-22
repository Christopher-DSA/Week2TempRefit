import pandas as pd
import uuid

def append_uuid_to_csv(file_name):
    # Read the CSV file
    data = pd.read_csv(file_name)

    # Assuming the first column contains the strings to be appended
    column_name = data.columns[0]

    # Append UUID4 to each entry in the column
    data[column_name] = data[column_name].apply(lambda x: f"{x}-{uuid.uuid4()}")

    # Save the modified data back to the CSV file
    data.to_csv(file_name, index=False)
    print("Complete! Each entry has been appended with a unique UUID4.")


def check_duplicate_uuids(file_name):
    # Read the CSV file
    data = pd.read_csv(file_name)

    # Extracting the UUID part
    column_name = data.columns[0]
    data['UUID'] = data[column_name].apply(lambda x: x.split('-')[-1])

    # Checking for duplicates
    if data['UUID'].duplicated().any():
        print("Duplicate UUIDs found!")
    else:
        print("No duplicate UUIDs. All are unique!")
        
# The main block
if __name__ == '__main__':
    check_duplicate_uuids('Actual_EQP_numbers.csv')
