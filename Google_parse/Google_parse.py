__author__ = 'Atelier'

from appclass import AutoApp
import json
import time

# This Class is used only to grab financial info from the Google API and store it in the database,
# there is no reflexion in this class

class Google_Parse():

    api_url = 'http://finance.google.com/finance/info?q=EPA:'
    data = {}


    def __init__(self):
        pass

    def get_stock_quote(self, firm):
        url = self.api_url + firm[2]
        lines = urllib2.urlopen(url).read().splitlines()
        return [firm[1],json.loads(''.join([x for x in lines if x not in ('// [', ']')]))]


    def get_multi_stock_quote(self, firms):
        answer = []
        for f in firms:
            answer.append(self.get_stock_quote(f))
        return answer

    def write_in_db(self, firm_data):
        params = {'isin': firm_data[0], 'quotation':firm_data[1]['l_cur'], 'time': time.time()}
        AutoApp.DataM.execute('INSERT INTO system_firms_quotation (isin, quotation, date) '
                              'VALUES (:isin, :quotation, :time)', params)

    def write_multi_in_db(self, firms_data):
        for firm_data in firms_data:
            self.write_in_db(firm_data)

    def save_firms_data(self, firms):
        firms_data = self.get_multi_stock_quote(firms)
        self.write_multi_in_db(firms_data)




