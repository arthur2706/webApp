import unittest
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, request
from validate import ValidateInputs


app = Flask(__name__)


valid_data = '{"message": "foo"}'
invalid_data = '{"name": 100}'


class ValidateTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(method='POST', data=valid_data, content_type='application/json'):
            inputs = ValidateInputs(request)
            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
            inputs = ValidateInputs(request)
            self.assertFalse(inputs.validate())

if __name__ == '__main__':
    unittest.main()
