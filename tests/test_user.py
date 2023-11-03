import unittest
from models import User, CRUD

class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.user_data = {
            "email": "test@example.com",
            "password": "test_password",
            "role": "test_role",
            "added_date": "2023-11-03",
            "user_detail": "test_user_detail",
            "status": "test_status"
        }
    
    def test_create_user(self):
        # Test creating a user
        new_user = CRUD.create(User, **self.user_data)
        self.assertIsNotNone(new_user, "User creation failed.")

    def test_read_user(self):
        # Test reading a user
        created_user = CRUD.create(User, **self.user_data)
        retrieved_user = CRUD.read(User, email=self.user_data["email"])
        self.assertIsNotNone(retrieved_user, "User retrieval failed.")
        self.assertEqual(retrieved_user.email, self.user_data["email"], "Retrieved user does not match.")

    def test_update_user(self):
        # Test updating a user
        created_user = CRUD.create(User, **self.user_data)
        new_email = "updated_test@example.com"
        CRUD.update(User, "email", new_email, email=self.user_data["email"])
        updated_user = CRUD.read(User, email=new_email)
        self.assertIsNotNone(updated_user, "User update failed.")
        self.assertEqual(updated_user.email, new_email, "Email not updated.")

    def test_delete_user(self):
        # Test deleting a user
        created_user = CRUD.create(User, **self.user_data)
        CRUD.delete(User, email=self.user_data["email"])
        deleted_user = CRUD.read(User, email=self.user_data["email"])
        self.assertIsNone(deleted_user, "User deletion failed.")

if __name__ == '__main__':
    unittest.main()
