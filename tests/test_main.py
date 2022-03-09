'''
Test login functionlity
'''

from unittest.mock import MagicMock, Mock, patch, create_autospec
import unittest
import sqlite3

import src.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('src.main.system')
        self.patcher2 = patch('src.main.connect')
        self.patcher3 = patch('src.main.authenticate')
        self.patcher4 = patch('sqlite3.Connection')
        self.patcher5 = patch('sqlite3.Cursor')

        self.mock_system = self.patcher1.start()
        self.mock_connect = self.patcher2.start()
        self.mock_authenticate = self.patcher3.start()
        self.mock_connection = self.patcher4.start()
        self.mock_cursor = self.patcher5.start()

        assert main.authenticate is self.mock_authenticate
        assert main.connect is self.mock_connect
        assert main.system is self.mock_system
        assert sqlite3.Connection is self.mock_connection
        assert sqlite3.Cursor is self.mock_cursor

        main.cursor = sqlite3.Cursor(self.mock_connection)


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()

    # Testing main file
    def test_main(self):

        # check print statemenets in mock_main
        self.mock_authenticate.return_value = 'bced', True # editor

        main.main('./test.db')

        self.mock_connect.assert_called_once_with('./test.db')
        self.mock_authenticate.assert_called_once()
        self.mock_system.assert_called_once_with('bced', True)
        return


if __name__ == '__main__':
    unittest.main()