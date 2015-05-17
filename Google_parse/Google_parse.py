__author__ = 'Atelier'

from appclass import AutoApp
import json

# This Class is used only to grab financial info from the Google API and store it in the database,
# there is no reflexion in this class

class Google_Parse():

    api_url = 'http://finance.google.com/finance/info?q=EPA:'
    data = {}



    def __init__(self):
        pass

    def get_stock_quote(self, ticker_symbol):
        url = self.api_url + ticker_symbol
        lines = urllib2.urlopen(url).read().splitlines()
        self.data[ticker_symbol] = json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
        return self.data

