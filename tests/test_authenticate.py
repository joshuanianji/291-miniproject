'''
Test login functionlity
'''

from unittest.mock import patch
import unittest

import src.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('builtins.print')
        self.patcher2 = patch('builtins.input')
        self.patcher3 = patch('src.main.login')
        self.patcher4 = patch('src.main.signup')

        self.mock_print = self.patcher1.start()
        self.mock_input = self.patcher2.start()
        self.mock_login = self.patcher3.start()
        self.mock_signup = self.patcher4.start()

        assert main.login is self.mock_login
        assert main.signup is self.mock_signup
        assert print is self.mock_print
        assert input is self.mock_input


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()

    def test_auth_login_success(self):
        self.mock_input.return_value = 'L'
        self.mock_login.return_value = 'bced', True

        main.authenticate()

        self.mock_print.assert_called_once_with('Welcome to the login page! Press "L" to login or "S" to signup')
        self.mock_input.assert_called_once_with('Please enter your choice: ')
        self.mock_login.assert_called_once()
        return
    
    def test_auth_signup_success(self):
        self.mock_input.return_value = 'S'
        self.mock_signup.return_value = 'bced'

        main.authenticate()

        self.mock_print.assert_called_once_with('Welcome to the login page! Press "L" to login or "S" to signup')
        self.mock_input.assert_called_once_with('Please enter your choice: ')
        self.mock_signup.assert_called_once()
        return


if __name__ == '__main__':
    unittest.main()