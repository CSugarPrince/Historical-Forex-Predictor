import sqlite3
import pandas as pd

# TODO: ... next time I make a database, learn more about data and timestamp SQL data types...
# TODO: make a wrapper function for opening and closing a connection to the db
# TODO: write get_fr_by_date()
# TODO: write a wrapper function that connects to db, executes func(), closes connection

# DEV: 'with conn:' is used to auto-commit execution statements to the database

def insert_fr(fr):
    """ takes in ForexRate object. inserts time, date, and value of currency in the db """

    # connect to the database
    conn = sqlite3.connect('forex.db')
    c = conn.cursor()

    # insert data into db
    with conn:
        c.execute("INSERT INTO forex_rates VALUES (:source, :timestamp, :date, :base, :USD, :EUR, :JPY, :GBP, :CHF)", 
                    {'source': fr.source, 
                    'timestamp': fr.timestamp,
                    'date': fr.date,
                    'base': fr.base,
                    'USD': fr.USD,
                    'EUR': fr.EUR,
                    'JPY': fr.JPY,
                    'GBP': fr.GBP,
                    'CHF': fr.CHF
                    })

    # close connection to db
    conn.close()


def get_all():
    """ returns a list containing all items inside db. """
    
    # connect to the database
    conn = sqlite3.connect('forex.db')
    c = conn.cursor()

    # select and fetch all data
    c.execute("SELECT * FROM forex_rates")
    data = c.fetchall()

    # close connection to db
    conn.close()

    return data
    

def sql_to_df():
    """ returns dataframe """

    # connect to the database
    conn = sqlite3.connect('forex.db')

    # read database table as dataframe
    df = pd.read_sql_query("SELECT * FROM forex_rates", conn)

    # close connection
    conn.close()

    return df

def get_fr_by_date(date):
    pass    


def create_db():
    # "success":true,
    # "timestamp":1527865747,
    # "base":"EUR",
    # "date":"2018-06-01",
    # EUR/USD: The euro and the U.S. dollar
    # USD/JPY: The U.S. dollar and the Japanese yen
    # GBP/USD: The British pound sterling and the U.S. dollar
    # USD/CHF: The U.S. dollar and the Swiss franc

    # Possible Columns:
    # source - for the source URL

    # connect to the database
    conn = sqlite3.connect('forex.db')
    c = conn.cursor()

    # create forex_rates table
    with conn:
        c.execute("""CREATE TABLE forex_rates(
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



if __name__ == "__main__":
    print(__name__,'is running.')
    # create_db()
    # database table has already been created.