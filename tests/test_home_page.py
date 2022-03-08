'''
Test login functionlity
'''

from unittest.mock import patch, create_autospec, call
import unittest

import src.main as main


class TestHomePage(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('builtins.print')
        self.patcher2 = patch('builtins.input')
        self.patcher3 = patch('src.main.signup')
        self.patcher4 = patch('src.main.system')
        self.patcher5 = patch('src.main.connect')
        self.patcher6 = patch('src.main.authenticate')

        self.mock_print = self.patcher1.start()
        self.mock_input = self.patcher2.start()
        self.mock_signup = self.patcher3.start()
        self.mock_system = self.patcher4.start()
        self.mock_connect = self.patcher5.start()
        self.mock_authenticate = self.patcher6.start()

        assert main.authenticate is self.mock_authenticate
        assert main.connect is self.mock_connect
        assert main.system is self.mock_system
        assert main.signup is self.mock_signup
        assert print is self.mock_print
        assert input is self.mock_input

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()
        self.patcher6.stop()

    # Testing main file
    def test_main_authenticate(self):

        # check print statemenets in mock_main
        self.mock_authenticate.return_value = 'bced', True # editor

        main.main('./test.db')

        self.mock_connect.assert_called_once_with('./test.db')
        self.mock_authenticate.assert_called_once()
        self.mock_system.assert_called_once_with('bced', True)
        return


if __name__ == '__main__':
    unittest.main()