from urllib2 import Request, urlopen, URLError
import json

def getValidTimeseriesKey(timerseries_keys, offering_id):
	invalid_offering = '9999999999'
	if offering_id == invalid_offering:
		return timeseries_keys[1]
	else:
		return timeseries_keys[0]

ID=(3903, 4054, 3907)

stationdata = {}

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
    url2getdata = ('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/'+str(first_timeserieskey) +'/getData')

    request_time_series_data = Request(url2getdata)
    try:
    	response = urlopen(request_time_series_data)
    	time_series_data = response.read()
    except URLError, e:
        print 'error:', e

    stationdata.update({first_timeserieskey: time_series_data})
