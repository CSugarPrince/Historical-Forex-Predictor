import unittest

# appending to sys.path enables scripts in test folder to import code from
# parent directory where src files are located
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forex_rate import ForexRate

class TestForexRate(unittest.TestCase):

    def setUp(self):
        """ creates a ForexRate mock object  for testing."""

        print('setUp')

        # information that will be held in the ForexRate object
        source = "https://fakeurl.org/api/"
        information = {
            'base': 'EUR',
            'timestamp': 1527865747,
            "date": "2018-06-01",
            "rates":{
                "USD":1.307716,
                "EUR":1,
                "JPY":127.845959,
                "GBP":0.875365,
                "CHF":1.15304
            }
        }

        self.fr_1 = ForexRate(source, information)
        
    
    def tearDown(self):
        print('tearDown')
        pass

    def test_init(self):
        """ this test is probably unnecessary, as it tests whether or not
        the FR object was initialized correctly and the code for that is 
        pretty straightforward. """

        print('test_init')

        # test that the fr_1.source matches the given url
        self.assertEqual(self.fr_1.source, "https://fakeurl.org/api/")
        
        # test that the base currency's value is listed as 1.0
        # although, if it didn't, that means there would be an error
        # with the source, not my code
        base_cur = self.fr_1.base
        if base_cur == 'EUR':
            self.assertEqual(self.fr_1.EUR, 1)
        elif base_cur == 'USD':
            self.assertEqual(self.fr_1.USD, 1)
        elif base_cur == 'JPY':
            self.assertEqual(self.fr_1.JPY, 1)
        elif base_cur == 'GBP':
            self.assertEqual(self.fr_1.GBP, 1)
        elif base_cur == 'CHF':
            self.assertEqual(self.fr_1.CHF, 1)
        else:
            raise Exception('did not create a test for when there is a base other than the five listed')           

if __name__ == "__main__":
    unittest.main()