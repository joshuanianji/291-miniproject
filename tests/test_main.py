'''
Test login functionlity
'''

from unittest.mock import patch
import unittest

import src.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('src.main.system')
        self.patcher2 = patch('src.main.connect')
        self.patcher3 = patch('src.main.authenticate')

        self.mock_system = self.patcher1.start()
        self.mock_connect = self.patcher2.start()
        self.mock_authenticate = self.patcher3.start()

        assert main.authenticate is self.mock_authenticate
        assert main.connect is self.mock_connect
        assert main.system is self.mock_system

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

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