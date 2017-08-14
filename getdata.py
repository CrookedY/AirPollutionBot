from urllib2 import Request, urlopen, URLError
import json, os

#p2.5

request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/455/getData')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

result= json.loads (data)

p2result = result [u'values']

#NOX
request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/453/getData')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

result= json.loads (data)

NOXresult = result [u'values']

#print NOXresult
