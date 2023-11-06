import unittest
from models import User_Detail, CRUD

class TestUserDetailModel(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.user_detail_data = {
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "address": "123 Main Street",
            "province": "California",
            "city": "Los Angeles",
            "postal_code": "90001",
            "telephone": "123-456-7890",
            "user_id": 1
        }
    
    def test_create_user_detail(self):
        # Test creating a user detail
        new_user_detail = CRUD.create(User_Detail, **self.user_detail_data)
        self.assertIsNotNone(new_user_detail, "User detail creation failed.")

    def test_read_user_detail(self):
        # Test reading a user detail
        created_user_detail = CRUD.create(User_Detail, **self.user_detail_data)
        retrieved_user_detail = CRUD.read(User_Detail, user_id=self.user_detail_data["user_id"])
        self.assertIsNotNone(retrieved_user_detail, "User detail retrieval failed.")
        self.assertEqual(retrieved_user_detail.user_id, self.user_detail_data["user_id"], "Retrieved user detail does not match.")

    def test_update_user_detail(self):
        # Test updating a user detail
        created_user_detail = CRUD.create(User_Detail, **self.user_detail_data)
        new_telephone = "987-654-3210"
        CRUD.update(User_Detail, "telephone", new_telephone, user_id=self.user_detail_data["user_id"])
        updated_user_detail = CRUD.read(User_Detail, user_id=self.user_detail_data["user_id"])
        self.assertIsNotNone(updated_user_detail, "User detail update failed.")
        self.assertEqual(updated_user_detail.telephone, new_telephone, "Telephone not updated.")

    def test_delete_user_detail(self):
        # Test deleting a user detail
        created_user_detail = CRUD.create(User_Detail, **self.user_detail_data)
        CRUD.delete(User_Detail, user_id=self.user_detail_data["user_id"])
        deleted_user_detail = CRUD.read(User_Detail, user_id=self.user_detail_data["user_id"])
        self.assertIsNone(deleted_user_detail, "User detail deletion failed.")

if __name__ == '__main__':
    unittest.main()
