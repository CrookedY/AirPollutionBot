# -*- coding: utf-8 -*-
import pandas as pd
import tweepy
import os
import string
from createlistofstations import finallist
from geotext import GeoText
from fuzzywuzzy import process
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from urllib2 import Request, urlopen, URLError
import json

geolocator = Nominatim()


auth = tweepy.OAuthHandler('wA4BLtKEtSEwYZpBo3nU7swL8', 'VydrPUsMcgwbWkdVoktm5MfaZcmle8j72aO7wdF03RW50vkBbv')
auth.set_access_token('892859700819091456-IoQMfI4Bbk5E7vvNXwt8SWghl9buIq2', 'Pvd8X5lHes4mTeHsGPvaZdk1GxZ18L9WOUpoQBicKh7W0')
api = tweepy.API(auth)


searchstrings = ["@shefairpol",
                  "shefairpol",
                  "what is the air pollution in",
                  "What's the air pollution"
                  ]
tweetslookup = api.search(q="Sheffield Air Pollution")

print (tweetslookup[0].text)

Place = GeoText(tweetslookup[1].text)
PlaceNames = Place.cities
PlaceName = Place.cities[0]
location = str(PlaceName.translate(string.punctuation)) #needs to be a forloop?

print (PlaceNames)

###############################################################################

tweetedLocation = geolocator.geocode(location, timeout = None)

LocationCoordinates = (tweetedLocation.longitude,tweetedLocation.latitude)

print (LocationCoordinates)

ListofStationCoordinates = finallist.loc[ : , "latandlong"]

#print (ListofStationCoordinates)


shortest_distance = None
shortest_distance_coordinates = None

for station in ListofStationCoordinates:
    distance = vincenty(LocationCoordinates, station)
    if distance < shortest_distance or shortest_distance is None:
        shortest_distance = distance
        shortest_distance_coordinates = station

print (shortest_distance_coordinates)

ClosestStation = finallist[finallist.latandlong.isin([shortest_distance_coordinates])]

#print(ClosestStation)

ClosestStationKeys = ClosestStation.loc[:, "ID"]

print(ClosestStationKeys)

##########################################################################

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


ID=(ClosestStationKeys)

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
    StationName = PlaceName
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
