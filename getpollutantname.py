from urllib2 import Request, urlopen, URLError
import json, os
import pandas


requestpoll = Request ('http://dd.eionet.europa.eu/vocabulary/aq/pollutant/json')
try:
	response = urlopen(requestpoll)
	pollutant_prop = response.read()
except URLError, e:
    print 'error:', e

json_pollutantlist = json.loads(pollutant_prop)
jsonpollutantlistdictionaries = json_pollutantlist[u'concepts']

listofpollutants = []
for pollutant in jsonpollutantlistdictionaries:
	statID = pollutant['@id']
	pollutantname = pollutant[u'prefLabel'][0]['@value']
	listofpollutants.append ((statID,pollutantname))




print listofpollutants
