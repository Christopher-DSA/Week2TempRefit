import unittest
from models import Technician, User, Contractor, CRUD

class TestTechnicianModel(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.technician_data = {
            "ods_licence_number": "123456789",
            "user_id": 1,
            "contractor_id": 1,
            "date_begin": "2023-01-01",
            "date_end": "2023-12-31",
            "user_status": "active",
            "contractor_status": "active"
        }
    
    def test_create_technician(self):
        # Test creating a technician
        new_technician = CRUD.create(Technician, **self.technician_data)
        self.assertIsNotNone(new_technician, "Technician creation failed.")

    def test_read_technician(self):
        # Test reading a technician
        created_technician = CRUD.create(Technician, **self.technician_data)
        retrieved_technician = CRUD.read(Technician, ods_licence_number=self.technician_data["ods_licence_number"])
        self.assertIsNotNone(retrieved_technician, "Technician retrieval failed.")
        self.assertEqual(retrieved_technician.ods_licence_number, self.technician_data["ods_licence_number"], "Retrieved technician does not match.")

    def test_update_technician(self):
        # Test updating a technician
        created_technician = CRUD.create(Technician, **self.technician_data)
        new_user_status = "inactive"
        CRUD.update(Technician, "user_status", new_user_status, ods_licence_number=self.technician_data["ods_licence_number"])
        updated_technician = CRUD.read(Technician, ods_licence_number=self.technician_data["ods_licence_number"])
        self.assertIsNotNone(updated_technician, "Technician update failed.")
        self.assertEqual(updated_technician.user_status, new_user_status, "User status not updated.")

    def test_delete_technician(self):
        # Test deleting a technician
        created_technician = CRUD.create(Technician, **self.technician_data)
        CRUD.delete(Technician, ods_licence_number=self.technician_data["ods_licence_number"])
        deleted_technician = CRUD.read(Technician, ods_licence_number=self.technician_data["ods_licence_number"])
        self.assertIsNone(deleted_technician, "Technician deletion failed.")

if __name__ == '__main__':
    unittest.main()
