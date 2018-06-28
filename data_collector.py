import api_interface as api
from forex_rate import ForexRate
import sqlite3_forex as db
import datetime
import threading
import queue

# TODO: test for correct input in the get_time_series()
# TODO: sort objects by date???


class DownloadWorker(threading.Thread):
    """ This thread sends and receives api requests. 
        This thread intentionally modifies queues and lists that originate from outside its class/method definitions."""

    # Class Variables
    available_apis = {'fixer': True, 'openex': True}


    def __init__(self, name, date_queue, parsed_data):
        threading.Thread.__init__(self)

        self.name = name

        # stores link to queues and lists. takes advantage of Python's call-by-object-reference.
        self.dq = date_queue
        self.pd = parsed_data

       
    def run(self):
        """ makes requests for data from available apis. stores data in parsed_data list. """
        
        while self.dq.empty() == False:
            
            date = self.dq.get()

            if DownloadWorker.available_apis['fixer']:
                # log...
                print('{} downloading {} from fixer'.format(self.name, date))
                
                # if fixer is working ok, request historical data from it
                data = api.get_fixer_historical_rates(date)
                          
                if data is not None:
                    # store data in list to await processing and storage into database
                    self.pd.append(data)

                    # log...
                    print('{} received historical data for {} from fixer'.format(self.name, date))
                else:
                    # if no data was received from fixer, set it as an unavailable api
                    DownloadWorker.available_apis['fixer'] = False

                    # put date back in queue
                    self.dq.put(date)

                    # log...
                    print('{} did NOT receive historical data for {} from fixer'.format(self.name, date))
            
            elif DownloadWorker.available_apis['openex']:     
                # log...
                print('{} downloading {} from openex'.format(self.name, date))
                # if fixer not available, but openex is available, request historical data from it
                data = api.get_openex_historical_rates(date)

                if data is not None:
                    # store data in list to await processing and storage into database
                    self.pd.append(data)

                    # log...
                    print('{} received historical data for {} from openex'.format(self.name, date))
                else:
                    # if no data was received from openex, set it as an unavailable api
                    DownloadWorker.available_apis['openex'] = False

                    # put date back in queue
                    self.dq.put(date)

                    # log...
                    print('{} did NOT receive historical data for {} from openex'.format(self.name, date))

            else:
                # if no api requests are returning with data, break out of loop, log error message
                
                # put date back in queue
                self.dq.put(date)

                # log...
                print("no api's available to download data for {}.".format(date))

                break        


def create_date_queue(start_date, end_date):
    """ creates a queue a dates that starts at the start_date, increments by a day until it reaches end_date """

    # convert date strings into date objects
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()

    date_queue = queue.Queue()

    # print out every day between the start date and the end date
    for n in range(int((end_date - start_date).days) + 1):
        date_queue.put(str(start_date + datetime.timedelta(n)))

    return date_queue    
        



def get_time_series(start_date, end_date):
    """ This is a massive function that uses multiple threads to download data, process data, and store it in a database. """

    # test for correct input here:
    #...

    # create date_queue
    date_queue = create_date_queue(start_date, end_date)

    # create parsed_data list
    parsed_data = []
    
    # create DownloadWorker threads
    dw_threads = []
    for i in range(4):
        dw = DownloadWorker('dw_thread ' + str(i), date_queue, parsed_data)

        # log DEBUG...
        print('created {}'.format(dw.name))

        dw_threads.append(dw)
    
    # start download threads
    for thread in dw_threads:
        thread.start()

        # log...
        print('starting {}'.format(thread.name))
    
    # wait for download threads to finish running
    for thread in dw_threads:
        thread.join()

        # log...
        print('joining {}'.format(thread.name))
   
    
    # after threads are finished downloading data from internet, convert them to forex objects, store them in database
    fr_objs = []
    for data in parsed_data:
        fr = ForexRate(data['source'], data)
        fr_objs.append(fr)

    # store ForexRate objects in database
    for obj in fr_objs:
        db.insert_fr(obj) 

        # log...
        print('stored hr for {} in database'.format(obj.date)) 

    # log...
    print('dates still in dq:')
    while not date_queue.empty():
        print(date_queue.get())      


if __name__ == "__main__":

    # get historical data from start date to end date
    sd = '2002-04-17'
    ed = '2004-12-01' 
    get_time_series(sd, ed)

    # massive success! Decreased runtime from several minutes
    # to under ten seconds!
    
    # The next range of dates should be from:
    # sd = '2004-12-02'
    # ed = idk. gotta calculate it        