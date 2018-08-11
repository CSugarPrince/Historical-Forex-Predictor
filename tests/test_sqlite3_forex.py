import unittest
import sqlite3

# appending to sys.path enables scripts in test folder to import code from
# parent directory where src files are located
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forex_rate import ForexRate
import sqlite3_forex

# NOTE: This test file changes the current working directory to the directory that contains this python file.
# TODO: use the class method for 'setUpClass' to change directories before running unittest.main
# TODO: re-think unittest design. Currentyl don't know how to properly test "insert_fr" or otherdatabse functions

class TestSqlite3Forex(unittest.TestCase):

    def setUp(self):
        """ Will set up a test database before every test. """
        print('setUp')

        # make some test ForexRate objects
        fr_1_source = 'http://fakesource1.com'
        fr_1_data = {'base': 'EUR',
                     'timestamp': 1528073647,
                     'date': '2018-06-04',
                     'rates': { 'USD': 1.167819,
                                'EUR': 1,
                                'JPY': 128.081684,
                                'GBP': 0.873692,
                                'CHF': 1.155101}}
        self.fr_1 = ForexRate(fr_1_source, fr_1_data)

        fr_2_source = 'http://notarealwebsite.org'
        fr_2_data = {'base': 'EUR',
                     'timestamp': 915235199,
                     'date': '1999-01-01',
                     'rates': { 'USD': 1.171626,
                                'EUR': 1,
                                'JPY': 133.151679,
                                'GBP': 0.706421,
                                'CHF': 1.611044}}
        self.fr_2 = ForexRate(fr_2_source, fr_2_data) 

        fr_3_source = 'http://mocksite.io/api'
        fr_3_data = {'base': 'USD',
                     'timestamp': 1017676800,
                     'date': '2002-04-01',
                     'rates': { 'USD': 1,
                                'EUR': 1.137345,
                                'JPY': 133.236033,
                                'GBP': 0.695451,
                                'CHF': 1.664613}}
        self.fr_3 = ForexRate(fr_3_source, fr_3_data)  

        # connect to the database
        self.connection = sqlite3.connect('test.db')
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.execute("""CREATE TABLE forex_rates(
                        source text,
                        timestamp integer,
                        date text,
                        base text,
                        USD integer,
                        EUR integer,
                        JPY integer,
                        GBP integer,
                        CHF integer
                        )""")
        
        # close the connection
        self.connection.close()
           
                        

    def tearDown(self):
        """ Deletes 'test.db' database after every test. """
        print('tearDown')

        os.remove('test.db')

    def test_insert_fr(self):
        """ Tests that a Forex rate is inserted correctly into the database. """
        print('test_insert_fr')


        pass


if __name__ == "__main__":
    # saves path to old directory
    old_dir = os.getcwd()
    print(os.getcwd())

    # changes dir to the dir where this file is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(os.getcwd())

    unittest.main()   

    # ERROR: the code that comes after unittest.main() apparently doesn't run....
    # restores previous working directory
    os.chdir(old_dir)
    print('goober')
    print(os.getcwd())