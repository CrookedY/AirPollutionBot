from urllib2 import Request, urlopen, URLError
import json, os

#this script accesses the data and selects the appropriate values

request = Request('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/455/getData')

try:
	response = urlopen(request)
	data = response.read()
except URLError, e:
    print 'error:', e

result= json.loads (data)

result2 = result [u'values']

def whichresult():
	if result2[-1][u'value'] !=-99.0:
	#	print result2[-1][u'value']
		return result2[-1][u'value']
	else:
		if result2[-2][u'value']!=-99.0:
			#print result2[-2][u'value']
			return result2[-2][u'value']
		else:
			if result2[-3][u'value']!=-99.0:
				#print result2[-3][u'value']
				return result2[-3][u'value']
			elif result2[-4][u'value']!=-99.0:
				#print result2[-3][u'value']
				return result2[-4][u'value']

if os.environ.get("DEBUG"):
  print whichresult()

def highorlow():
	if whichresult()<=35:
		return 'low'
	elif whichresult()>=54:
		return 'high'
	else:
		return 'medium'

if os.environ.get("DEBUG"):
	print highorlow()
