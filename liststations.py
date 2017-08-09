from urllib2 import Request, urlopen, URLError
import json

request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations/')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

stations= json.loads (data)

#print stations

stations2 = stations [1]

print stations2
