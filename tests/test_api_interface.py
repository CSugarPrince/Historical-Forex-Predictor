import unittest
from unittest.mock import patch, Mock

# appending to sys.path enables scripts in test folder to import code from
# parent directory where src files are located
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import api_interface

""" unittest design notes:
The two functions tested do two things:
1. they make an http request to a server
2. they download and parse the repsonse (which is a json file)

I am using a mock object to impersonate the 'requests.get' function so that
the unittest code doesn't actually make a http request.

The return value of the mocked 'requests.get' changes based on what I am testing for
The things I have tested for include:
1. The function makes the request and gets a response containging the desired info
2. The function makes the request but it doesn't get a response from the server (requests.get returns None)
3. The function makes the request and gets a response, but it is an error message. When the function receives an error message
    it should print out the error message (will be changed to a log) and it will return a None object

"""

class TestApiInterface(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.sample_date_1 = '2002-04-14'
    
    def tearDown(self):
        pass

    def test_get_fixer_historical_rates(self):
        print('test_get_fixer_historical_rates')
        with patch('api_interface.requests.get') as mocked_get:
            # test that a successful call yields a successful response
            mocked_get.return_value = Mock()
            mocked_get.return_value.json.return_value = {'success': True, 'info': 'foo'}
            
            
            function_output = api_interface.get_fixer_historical_rates(self.sample_date_1)

            self.assertEqual(function_output['success'], True)
            self.assertEqual(function_output['source'], 'http://data.fixer.io/api/')
            
            # test that an unsuccessful call causes the function to return None
            # case 1: something wrong on server side (internet is down, etc...)
            mocked_get.return_value = None

            function_output = api_interface.get_fixer_historical_rates(self.sample_date_1)

            self.assertEqual(function_output, None)

            # case 2: get a response, but the response is an error message
            mocked_get.return_value = Mock()
            parsed_error_message = {'success': False,
                                    'error': {
                                            'code': 999,
                                            'type': 'mock error'
                                            }
                                    }
            mocked_get.return_value.json.return_value = parsed_error_message

            function_output = api_interface.get_fixer_historical_rates(self.sample_date_1)

            self.assertEqual(function_output, None)
        
    
    def test_get_openex_historical_rates(self):
        print('test_get_openex_historical_rates')
        with patch('api_interface.requests.get') as mocked_get:
            # test that a successful call yields a successful response
            mocked_get.return_value = Mock()
            mocked_get.return_value.json.return_value = {'success': True, 'info': 'foo'}
            
            
            function_output = api_interface.get_openex_historical_rates(self.sample_date_1)

            self.assertEqual(function_output['success'], True)
            self.assertEqual(function_output['date'], self.sample_date_1)
            self.assertEqual(function_output['source'], 'https://openexchangerates.org/api/')
            
            # test that an unsuccessful call causes the function to return None
            # case 1: something wrong on server side (internet is down, etc...)
            mocked_get.return_value = None

            function_output = api_interface.get_openex_historical_rates(self.sample_date_1)

            self.assertEqual(function_output, None)

            # case 2: get a response, but the response is an error message
            mocked_get.return_value = Mock()
            parsed_error_message = {'success'   : False,
                                    'error'     : True,
                                    'status'    : 999,
                                    'message'   : 'not_available',
                                    'description': 'mock error description'
                                    }
            mocked_get.return_value.json.return_value = parsed_error_message

            function_output = api_interface.get_openex_historical_rates(self.sample_date_1)

            self.assertEqual(function_output, None)


if __name__ == "__main__":
    unittest.main()