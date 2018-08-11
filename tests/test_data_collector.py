import unittest
from unittest.mock import patch, Mock
import queue

# appending to sys.path enables scripts in test folder to import code from
# parent directory where src files are located
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import data_collector

class TestDataCollector(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_create_date_queue(self):
        print('test_create_date_queue')

        start_date_1 = '1998-01-14'
        end_date_1 = '1998-01-20'

        dates = data_collector.create_date_queue(start_date_1, end_date_1)
        dates = list(dates.queue)

        # DEBUG: print(dates)

        self.assertEqual(dates[0], '1998-01-14')
        self.assertEqual(dates[1], '1998-01-15')
        self.assertEqual(dates[2], '1998-01-16')
        self.assertEqual(dates[3], '1998-01-17')
        self.assertEqual(dates[4], '1998-01-18')
        self.assertEqual(dates[5], '1998-01-19')
        self.assertEqual(dates[6], '1998-01-20')
        
        
        


if __name__ == "__main__":
    unittest.main()