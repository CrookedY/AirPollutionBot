from urllib2 import Request, urlopen, URLError
import json

request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations/')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

stations= json.loads (data)
#extract out station 2
stations2 = stations [7]

properties = stations2[u'properties']
#extract ID so can be use in link
ID = properties[u'id']
#print ID
url = ('https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations/'+str(ID))

request2 = Request (url)
try:
	response = urlopen(request2)
	data2 = response.read()
except URLError, e:
    print 'error:', e

#contains  station properties data. Need to get to timecourse ID
station_prop = data2
station_prop_json= json.loads (station_prop)
#ID is a key in dictionary so need to extract as a key
a= station_prop_json[u'properties'][u'timeseries'].keys()
i=a[0]

url2 =('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/'+str(i) +'/getData')

request3 = Request(url2)
try:
	response = urlopen(request3)
	data3 = response.read()
except URLError, e:
    print 'error:', e

print data3
