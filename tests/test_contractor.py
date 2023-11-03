import unittest
from models import Contractor, User, CRUD

class TestContractorModel(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.contractor_data = {
            "name": "Contractor Name",
            "user_id": 1,
            "logo": "logo.png",
            "status": "active",
            "subscription_id": 1,
            "code_2fa_code": "123456",
            "employees": 10,
            "are_they_tracking_refrigerant": "Yes",
            "time_basis": "Hourly"
        }
    
    def test_create_contractor(self):
        # Test creating a contractor
        new_contractor = CRUD.create(Contractor, **self.contractor_data)
        self.assertIsNotNone(new_contractor, "Contractor creation failed.")

    def test_read_contractor(self):
        # Test reading a contractor
        created_contractor = CRUD.create(Contractor, **self.contractor_data)
        retrieved_contractor = CRUD.read(Contractor, name=self.contractor_data["name"])
        self.assertIsNotNone(retrieved_contractor, "Contractor retrieval failed.")
        self.assertEqual(retrieved_contractor.name, self.contractor_data["name"], "Retrieved contractor does not match.")

    def test_update_contractor(self):
        # Test updating a contractor
        created_contractor = CRUD.create(Contractor, **self.contractor_data)
        new_status = "inactive"
        CRUD.update(Contractor, "status", new_status, name=self.contractor_data["name"])
        updated_contractor = CRUD.read(Contractor, name=self.contractor_data["name"])
        self.assertIsNotNone(updated_contractor, "Contractor update failed.")
        self.assertEqual(updated_contractor.status, new_status, "Contractor status not updated.")

    def test_delete_contractor(self):
        # Test deleting a contractor
        created_contractor = CRUD.create(Contractor, **self.contractor_data)
        CRUD.delete(Contractor, name=self.contractor_data["name"])
        deleted_contractor = CRUD.read(Contractor, name=self.contractor_data["name"])
        self.assertIsNone(deleted_contractor, "Contractor deletion failed.")

if __name__ == '__main__':
    unittest.main()
