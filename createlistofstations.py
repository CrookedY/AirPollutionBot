from urllib2 import Request, urlopen, URLError
import json
import pandas

request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations/')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

stations= json.loads (data)

# print(data)

listofstations = []
for i in stations:
	statID=(i [u'properties'][u'id'])
	name=(i[u'properties'][u'label'])
	latitude = (i[u'geometry'][u'coordinates'][0])
	longitude = (i[u'geometry'][u'coordinates'][1])
	listofstations.append ((statID,name, (latitude, longitude)))

#print(listofstations)


finallist=pandas.DataFrame(listofstations, columns = ('ID', 'station', 'latandlong'))

#print finallist

#finallist.to_csv('liststations.csv', sep=',', encoding = 'utf-8')
