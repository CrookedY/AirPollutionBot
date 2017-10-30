from urllib2 import Request, urlopen, URLError
import json, os
import pandas
#
# request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/455/')
#
# try:
# 	response = urlopen(request)
# 	station_prop = response.read()
# except URLError, e:
#     print 'error:', e
#
# station_prop_json = json.loads (station_prop)
#
# pollutant_webadd = station_prop_json[u'parameters'][u'phenomenon'][u'id']

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













#finallistpollutants=pandas.DataFrame(listofpollutants, columns = ('statID', 'pollutantname'))

#finallistpollutants.to_csv('pollutantlist.csv', sep=',', encoding = 'utf-8')

print listofpollutants
