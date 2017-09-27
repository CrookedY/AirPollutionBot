from urllib2 import Request, urlopen, URLError
import json
import pandas

def getValidTimeseriesKey(timerseries_keys, offering_id):
	invalid_offering = '9999999999'
	if offering_id == invalid_offering:
		return timeseries_keys[1]
	else:
		return timeseries_keys[0]

requestpoll = Request ('http://dd.eionet.europa.eu/vocabulary/aq/pollutant/json')
try:
    response = urlopen(requestpoll)
    pollutant_prop = response.read()
except URLError, e:
    print 'error:', e

json_pollutantlist = json.loads(pollutant_prop)
jsonpollutantlistdictionaries = json_pollutantlist[u'concepts']

listofpollutants = {}
for pollutant in jsonpollutantlistdictionaries:
    statID = pollutant['@id']
    pollutantname = pollutant[u'prefLabel'][0]['@value']
    listofpollutants.update ({statID:pollutantname})

allstations = pandas.read_csv("liststations.csv")
allstations = allstations.drop('Unnamed: 0', 1)
allstations = allstations.set_index('ID')

ID=(3907, 3903)

listofstationsdata = []

for i in ID:
    url = ('https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations/'+str(i))
    request2 = Request (url)
    try:
    	response = urlopen(request2)
    	station_data = response.read()
    except URLError, e:
        print 'error:', e

    station_prop_json = json.loads (station_data)
    station_time_series = station_prop_json[u'properties'][u'timeseries']
    timeseries_keys = (station_time_series.keys())
    first_timeseries = station_time_series[timeseries_keys[0]]
    offering_id = first_timeseries[u'offering'][u'id']
    first_timeserieskey = getValidTimeseriesKey(timeseries_keys, offering_id)
    station_pollutant = first_timeseries[u'category'][u'id']
    station_ID = first_timeseries[u'feature'][u'id']
    StationName = allstations.loc[(int(station_ID) , 'place')]
    PollutantName = listofpollutants.get(station_pollutant)
    url2getdata = ('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/'+str(first_timeserieskey) +'/getData')

    request_time_series_data = Request(url2getdata)
    try:
    	response = urlopen(request_time_series_data)
    	time_series_data = response.read()
    except URLError, e:
        print 'error:', e

    listofstationsdata.append((StationName, PollutantName, time_series_data))

print listofstationsdata
