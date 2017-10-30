from urllib2 import Request, urlopen, URLError
import json, os
from getdata import NOXresult, p2result

def whichresult(pollutant):
	if pollutant[-1][u'value'] !=-99.0:
	#	print result2[-1][u'value']
		return pollutant[-1][u'value']
	else:
		if pollutant[-2][u'value']!=-99.0:
			#print result2[-2][u'value']
			return pollutant[-2][u'value']
		else:
			if pollutant[-3][u'value']!=-99.0:
				#print result2[-3][u'value']
				return pollutant[-3][u'value']
			elif pollutant[-4][u'value']!=-99.0:
				#print result2[-3][u'value']
				return pollutant[-4][u'value']
NOX = whichresult(NOXresult)
P2 = whichresult(p2result)

#print NOX

if os.environ.get("DEBUG"):
  print whichresult()

def highorlowp2(P2):
	if P2<=35:
		return 'low'
	elif P2>=54:
		return 'high'
	else:
		return 'medium'

if os.environ.get("DEBUG"):
	print highorlow()

def highorlowNOX(NOX):
	if NOX<=200:
		return 'low'
	elif NOX>=400:
		return 'high'
	else:
		return 'medium'

def higholowP10(P10):
	if P10 <=50:
		return 'low'
	elif p10>=83:
		return 'high'
	else:
		return 'medium'

def highorlow(highorlowNOX, highorlowp2):
	if highorlowNOX =='high' or highorlowp2 == 'high':
		return 'high'
	elif highorlowNOX =='medium' or highorlowp2 =='medium':
		return 'medium'
	else:
		return 'low'
