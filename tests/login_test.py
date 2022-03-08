'''
Test login functionlity
'''

from unittest.mock import patch
from unittest import TestCase
import unittest

import src.project as project

class TestLogin(TestCase):

    # get_input will return 'yes' during this test
    # @patch('project.main')
    # def test_answer_yes(self, input):
    #     self.assertEqual(project.main(custom_path='./test.db'), 'Welcome to the login page! Press "L" to login or "S" to signup')
    
    # test that 1+1=2
    def test_add_one_plus_one_equals_two(self):
        self.assertEqual(1+1, 2)

if __name__ == '__main__':
    unittest.main()