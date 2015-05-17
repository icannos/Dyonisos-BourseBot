__author__ = 'Atelier'
#__all__ = ['GoogleParse']

import appclass
import json
import time
import urllib2
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# This Class is used only to grab financial info from the Google API and store it in the database,
# there is no reflexion in this class

class GoogleParse():

    api_url = 'http://finance.google.com/finance/info?client=ig&q=EPA:'
    data = {}


    def __init__(self):
        pass

    def get_stock_quote(self, firm):
        url = self.api_url + firm[2]
        try:
            lines = urllib2.urlopen(url).read().decode('ISO-8859-1').splitlines()
            return [firm[1], json.loads(''.join([x for x in lines if x not in ('// [', ']')]))]
        except urllib2.HTTPError as error:
            print(error)
            logging.warning(firm[0] + ': ' + str(error))



    def get_multi_stock_quote(self, firms):
        answer = []
        for f in firms:
            answer.append(self.get_stock_quote(f))
        return answer

    def write_in_db(self, firm_data):
        print firm_data
        params = {'isin': firm_data[0], 'quotation':firm_data[1]['l'], 'time': time.time()}
        appclass.AutoApp.DataM.execute('INSERT INTO system_firms_quotation (isin, quotation, date) '
                              'VALUES (:isin, :quotation, :time)', params)
        appclass.AutoApp.DataM.commit()

    def write_multi_in_db(self, firms_data):
        for firm_data in firms_data:
            self.write_in_db(firm_data)

    def save_firms_data(self, firms):
        firms_data = self.get_multi_stock_quote(firms)
        self.write_multi_in_db(firms_data)





