#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#




#==============================================================================
# Signature: client.directions(origin, destination, mode=None, waypoints=None, alternatives=False, avoid=None, language=None, units=None, region=None, departure_time=None, arrival_time=None, optimize_waypoints=False, transit_mode=None, transit_routing_preference=None, traffic_model=None)
# Docstring:
# Get directions between an origin point and a destination point.
# 
# :param origin: The address or latitude/longitude value from which you wish
#     to calculate directions.
# :type origin: string, dict, list, or tuple
# 
# :param destination: The address or latitude/longitude value from which
#     you wish to calculate directions.
# :type destination: string, dict, list, or tuple
# 
# :param mode: Specifies the mode of transport to use when calculating
#     directions. One of "driving", "walking", "bicycling" or "transit"
# :type mode: string
# 
# :param waypoints: Specifies an array of waypoints. Waypoints alter a
#     route by routing it through the specified location(s).
# :type waypoints: a single location, or a list of locations, where a
#     location is a string, dict, list, or tuple
# 
# :param alternatives: If True, more than one route may be returned in the
#     response.
# :type alternatives: bool
# 
# :param avoid: Indicates that the calculated route(s) should avoid the
#     indicated features.
# :type avoid: list or string
# 
# :param language: The language in which to return results.
# :type language: string
# 
# :param units: Specifies the unit system to use when displaying results.
#     "metric" or "imperial"
# :type units: string
# 
# :param region: The region code, specified as a ccTLD ("top-level domain"
#     two-character value.
# :type region: string
# 
# :param departure_time: Specifies the desired time of departure.
# :type departure_time: int or datetime.datetime
# 
# :param arrival_time: Specifies the desired time of arrival for transit
#     directions. Note: you can't specify both departure_time and
#     arrival_time.
# :type arrival_time: int or datetime.datetime
# 
# :param optimize_waypoints: Optimize the provided route by rearranging the
#     waypoints in a more efficient order.
# :type optimize_waypoints: bool
# 
# :param transit_mode: Specifies one or more preferred modes of transit.
#     This parameter may only be specified for requests where the mode is
#     transit. Valid values are "bus", "subway", "train", "tram", "rail".
#     "rail" is equivalent to ["train", "tram", "subway"].
# :type transit_mode: string or list of strings
# 
# :param transit_routing_preference: Specifies preferences for transit
#     requests. Valid values are "less_walking" or "fewer_transfers"
# :type transit_routing_preference: string
# 
# :param traffic_model: Specifies the predictive travel time model to use.
#     Valid values are "best_guess" or "optimistic" or "pessimistic".
#     The traffic_model parameter may only be specified for requests where
#     the travel mode is driving, and where the request includes a
#     departure_time.
# :type units: string
# 
# :rtype: list of routes
# File:      ~/anaconda/lib/python2.7/site-packages/googlemaps/directions.py
# Type:      instancemethod
#==============================================================================

"""Tests for the directions module."""

from datetime import datetime
import responses
import requests
import time
import googlemaps


GoogleAPIKey = 'AIzaSyD5uhcVtSuVST28SYcrRdcjX139-O82I1w'
MapClient = googlemaps.Client(GoogleAPIKey)

def getDirection(origin,destination,mode='walking',alternatives=False):
    try:
        directions=MapClient.directions(origin,destination,mode,alternatives)
    except:
        return None
    for step in directions[0]['legs'][0]['steps']:
        HTMLInsturction=str(step['html_instructions'])
        stepInstruction=''
        adding=True
        for char in HTMLInsturction:
            if adding==True:
                if char=='<':
                    adding=False
                    continue
                stepInstruction+=char
            elif adding==False:
                if char=='>':
                    adding=True
    print stepInstruction,';  distance is: '+str(step['distance']['value'])+'m',';  duration is: '+str(step['duration']['value'])+'s'
    return directions
    
def getDistance(origin,destination,mode='walking',alternatives=False):
    try:
        distanceMatrix=MapClient.distance_matrix(origin,destination,mode,alternatives)
        return distanceMatrix['rows'][0]['elements'][0]['distance']['value']
    except:
        return None

def matchmode(dictMode):
    if dictMode=='Car/Van':
        mode='driving'
    elif dictMode=='Bus' or dictMode=='LRT/MRT':
        mode='transit'
    elif dictMode=='Motorcycle/Scooter':
        mode='bicycling'
    else:
        mode='walking'
    return mode

#routes = client.directions("Sydney", "Melbourne")
#routes = MapClient.directions("1.340835, 103.962101", "1.339784, 103.956479",mode='walking')
#distanceMatrix=MapClient.distance_matrix("1.340835, 103.962101", "1.339784, 103.956479",mode='walking')
#dis=0
'''
for step in routes[0]['legs'][0]['steps']:
    #dis+=float(step['distance']['value'])
    HTMLInsturction=str(step['html_instructions'])
    stepInstruction=''
    adding=True
    for char in HTMLInsturction:
        if adding==True:
            if char=='<':
                adding=False
                continue
            stepInstruction+=char
        elif adding==False:
            if char=='>':
                adding=True

    #stepInstruction=stepInstruction.replace('<b>','')
    #stepInstruction=stepInstruction.replace('</b>','')
    print stepInstruction,';  distance is: '+str(step['distance']['value'])+'m',';  duration is: '+str(step['duration']['value'])+'s'
'''
#print dis    
#print distanceMatrix['rows'][0]['elements'][0]['distance']['value']
    
    
    
    