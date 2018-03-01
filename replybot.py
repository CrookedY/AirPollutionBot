# -*- coding: utf-8 -*-
import pandas as pd
import tweepy
import os
import string
from createlistofstations import finallist
from geotext import GeoText
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from urllib2 import Request, urlopen, URLError
import json

auth = tweepy.OAuthHandler('wA4BLtKEtSEwYZpBo3nU7swL8', 'VydrPUsMcgwbWkdVoktm5MfaZcmle8j72aO7wdF03RW50vkBbv')
auth.set_access_token('892859700819091456-IoQMfI4Bbk5E7vvNXwt8SWghl9buIq2', 'Pvd8X5lHes4mTeHsGPvaZdk1GxZ18L9WOUpoQBicKh7W0')
api = tweepy.API(auth)

geolocator = Nominatim()

def getValidTimeseriesKey(timeseries_keys, offering_id):
	invalid_offering = '9999999999'
	if offering_id == invalid_offering:
		return timeseries_keys[1]
	else:
		return timeseries_keys[0]

def highorlowp2(P2):
	if P2<=35:
		return 'low'
	elif P2>=54:
		return 'high'
	else:
		return 'medium'

def highorlowP10(P10):
	if P10 <=50:
		return 'low'
	elif p10>=83:
		return 'high'
	else:
		return 'medium'

def highorlowNOX(NOX):
	if NOX<=200:
		return 'low'
	elif NOX>=400:
		return 'high'
	else:
		return 'medium'

def pollutionlevel(pollutionresults):
	if 'high' in pollutionresults:
		return 'high'
	if 'medium' in pollutionresults and 'high' not in pollutionresults:
		return 'medium'
	else:
		return 'low'

def makepollutantlist():
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
    return listofpollutants

listofpollutants = makepollutantlist()
ListofStationCoordinates = finallist.loc[ : , "latandlong"]

def findkeys(Tweet):
    tweet, location = Tweet.split("in ")
    tweetedLocation = geolocator.geocode(location, timeout = None)
    LocationCoordinates = (tweetedLocation.longitude,tweetedLocation.latitude)
    def distancetotweet(coordinate):
        return vincenty(LocationCoordinates, coordinate)
    ClosestStationlatlong = min(ListofStationCoordinates, key=distancetotweet)
    closeststation = finallist.loc[finallist['latandlong'] == ClosestStationlatlong]
    ClosestStationKeys1 = (closeststation.loc[:, "ID"])
    return ClosestStationKeys1

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

def getlistofdata(keylist):
    listofstationsdata = []
    ID=keylist
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
        PollutantName = listofpollutants.get(station_pollutant)
#         print PollutantName
        if first_timeseries[u'category'][u'id'] == '9' or first_timeseries[u'category'][u'id'] == '6001' or first_timeseries[u'category'][u'id'] == '5':
            url2getdata = ('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/'+str(first_timeserieskey) +'/getData')

            request_time_series_data = Request(url2getdata)
            try:
                response = urlopen(request_time_series_data)
                time_series_data = response.read()


            except URLError, e:
                print 'error:', e
#             print (time_series_data)
            listofstationsdata.append((PollutantName, time_series_data, station_pollutant))
    return listofstationsdata

def stationvalues (locationdata):
    stationvalidvalues = []
    for i in locationdata:
        timedata = json.loads(i[1])
        stationvalidvalues.append((i[0],(whichresult(timedata[u'values'])), i[2]))
    return stationvalidvalues

def pollutantLevelFinderstep1(station_values):
    pollutantLevels = []
    for i in station_values:
        if i[1] == None :
            pass
        else:
            if i[2] == '9':
                pollutantLevels.append(highorlowNOX(i[1]))
            elif i[2]=='6001':
                pollutantLevels.append(highorlowp2(i[1]))
            elif i[2]=='5':
                pollutantLevels.append(highorlowP10(i[1]))
            else:
                pollutantLevels.append('error')
    return pollutantLevels

def pollutantLevelFinderstep2(pollutantLevels):
    if 'high' in pollutantLevels:
        return 'High'
    else:
        if 'medium' in pollutantLevels:
            return 'Raised'
        else:
            return 'Low'

def createEndText(station_values):
    endText = ""
    for line in station_values:
        if str(line[1]) == 'None':
            pass
        else:
            if endText == "":
                endText += (' '+ line[0] + ' = ' + str(line[1])+ u'µg/m³')
            else:
                endText += (', '+ line[0] + ' is ' + str(line[1])+ u'µg/m³')
    return endText

def getusername(Tweet):
    reply_to = Tweet.user.screen_name
    return reply_to

def getplacename(Tweet):
    placename, location = Tweet.split("in ")
    return location

def createfinaltweet(tweet):
    username = getusername(tweet)
    tweettext = (tweet).text
    placenameloc = getplacename(tweettext)
    locationdata = getlistofdata(findkeys(tweettext))
    station_values = stationvalues(locationdata)
    level = pollutantLevelFinderstep2(pollutantLevelFinderstep1(station_values))
    final_tweet = u'@'+ username + ' The air pollution in ' + placenameloc + ' is ' + level + '.' + createEndText(station_values)+ ' #airpollution'
    return final_tweet
