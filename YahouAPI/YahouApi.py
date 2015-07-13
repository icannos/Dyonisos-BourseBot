__author__ = 'Maxime'

import urllib2, urllib, json

class YahouRestApiRequest:
    base_url = "http://query.yahooapis.com/v1/yql?"

    def encodequery(self, query):
        return self.base_url + urllib.urlencode({'q':query}) + "&format=json"

class RequestQuoteFirms(YahouRestApiRequest):
    firmscode = []
    quote_query = "select * from yahoo.finance.quote where symbol in "

    query = ''

    def __init__(self, firmscode):
        self.firmscode = firmscode

    def createquery(self):
        firmsquery = "("

        for f in self.firmscode:
            firmsquery += '"' + f + '.PA'+'"'

        firmsquery += ")"

        self.query = self.quote_query + firmsquery
        return self.query

    def getall(self):
        self.createquery()

        result = urllib2.urlopen(self.encodequery(self.query)).read()
        data = json.loads(result)
        self.data = data['query']['results']['quote']
        return self.data





