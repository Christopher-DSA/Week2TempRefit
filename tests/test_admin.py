import unittest
from models import Admin, User, CRUD

class TestAdminModel(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.admin_data = {
            "name": "Admin Name",
            "user_id": 1,
            "status": "active",
            "code_2fa_code": "123456",
            "admin_level": 1
        }
    
    def test_create_admin(self):
        # Test creating an admin
        new_admin = CRUD.create(Admin, **self.admin_data)
        self.assertIsNotNone(new_admin, "Admin creation failed.")

    def test_read_admin(self):
        # Test reading an admin
        created_admin = CRUD.create(Admin, **self.admin_data)
        retrieved_admin = CRUD.read(Admin, name=self.admin_data["name"])
        self.assertIsNotNone(retrieved_admin, "Admin retrieval failed.")
        self.assertEqual(retrieved_admin.name, self.admin_data["name"], "Retrieved admin does not match.")

    def test_update_admin(self):
        # Test updating an admin
        created_admin = CRUD.create(Admin, **self.admin_data)
        new_admin_level = 2
        CRUD.update(Admin, "admin_level", new_admin_level, name=self.admin_data["name"])
        updated_admin = CRUD.read(Admin, name=self.admin_data["name"])
        self.assertIsNotNone(updated_admin, "Admin update failed.")
        self.assertEqual(updated_admin.admin_level, new_admin_level, "Admin level not updated.")

    def test_delete_admin(self):
        # Test deleting an admin
        created_admin = CRUD.create(Admin, **self.admin_data)
        CRUD.delete(Admin, name=self.admin_data["name"])
        deleted_admin = CRUD.read(Admin, name=self.admin_data["name"])
        self.assertIsNone(deleted_admin, "Admin deletion failed.")

if __name__ == '__main__':
    unittest.main()
