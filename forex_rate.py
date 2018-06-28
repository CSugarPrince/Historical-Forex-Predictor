
# Possible changes:
# instead of storing only the majors, I could store all the rates as a dictionary
#   and I could have another dictionary called 'majors' that stores the rates of the majors

class ForexRate(object):
    """ object that contains base currency and values of tha currency in comparison to other currencies. """

    def __init__(self, source, data_dict):
        """ docstring """

        self.source = source
        """ list of sources:
        'http://data.fixer.io/api/'
        'https://openexchangerates.org/api/'
        """
        self.base = data_dict['base']                # the base should be USD by default
        self.timestamp = data_dict['timestamp']
        self.date = data_dict['date']
        self.USD = data_dict['rates']['USD']
        self.EUR = data_dict['rates']['EUR']
        self.JPY = data_dict['rates']['JPY']
        self.GBP = data_dict['rates']['GBP']
        self.CHF = data_dict['rates']['CHF']


if __name__ == "__main__":
    print("forex_rate.py")