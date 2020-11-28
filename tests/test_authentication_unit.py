import unittest
from modules.Authentication import User

class TestAuthentication(unittest.TestCase):
    
    def setUp(self):
        self.user = User()

    def test_user_login(self):
        message = self.user.login(1, "445566")
        self.assertEqual(message, True)

        message = self.user.login(2, "sag_22311as")
        self.assertEqual(message, True)

        with self.assertRaises(ValueError) as context:
            _ = self.user.login(4, "12345")
        self.assertTrue("User with ID 4 not found.", context.exception)

    def test_user_incorrect_password(self):
        with self.assertRaises(PermissionError) as context:
            _ = self.user.login(1, "123456")
        self.assertTrue("Password invalid. Permission denied.", context.exception)
        
        with self.assertRaises(PermissionError) as context:
            _ = self.user.login(2, "123456")
        self.assertTrue("Password invalid. Permission denied.", context.exception)