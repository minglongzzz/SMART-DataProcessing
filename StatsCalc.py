# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 03:09:28 2016

@author: minglong_zhou
"""

#==============================================================================
# Use : CombinedDict
# CombinedDict is {User ID: { 'routes':
#                         {Travel ID: 
#                             {Duration (second):
#                              End Lat:
#                              End Lon:
#                              Start Lat:
#                              Start Lon:
#                              End Time:
#                              Final Mode:
#                              Main Activity:
#                              Predicted Mode:
#                              Start Time:
#                              Travel ID:
#                              User ID:
#                              Travel/Stop:
#                              Trip Index:
#                              Segment Order:
#                              validated?:
#                             }
#                            }
#                         }
#                 }
# 
#==============================================================================



from dataFormating import *
import GoogleMapFunctions
import datetime as dt
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib.dates as mdates

class User():
    def __init__(self,userid,dictionary):
        self.userid=userid
        self.dict=dictionary[userid]
        
    def getTripbyIndex(self,tripIndex):
        #tripIndex is an int
        trip=dict([(key,self.dict['routes'][key]) for key in self.dict['routes'].keys() if self.dict['routes'][key]['Trip Index']==str(tripIndex)])
        return trip
    def getTripbyDate(self,date):
        #date is in this format: yyyy-mm-dd
        trip=dict([(key,self.dict['routes'][key]) for key in self.dict['routes'].keys() if self.dict['routes'][key]['Start Time'].split(' ')[0]==str(date)])
        return trip
    def calcCarbonFootprint(self,dist,mode):
        bus_emission = 66.0 #grams/passenger-kilometer
        train_emission = 12.9 #grams/passenger-kilometer
        car_emission= 187.0   #grams/passenger-kilometer
        if mode=='Car/Van':
            return car_emission*dist
        elif mode=='Bus':
            return bus_emission*dist
        elif mode=='LRT/MRT':
            return train_emission*dist
        else:
            return 0
    def getDateTimeFormat(self, datetimeStr):
        #'2016-02-02 19:30:30'
        time_seg=datetimeStr.split(' ')[0]+' '+datetimeStr.split(' ')[1]
        datetimeObj=dt.datetime.strptime(time_seg,'%Y-%m-%d %H:%M:%S')
        return datetimeObj
        
    def calculateStatsforTrip(self,tripIndex):
        print tripIndex
        statsKeys=['Travel Time', 'Travel Distance', 'Average Speed', 'Transit Time', 'Carbon Emission']
        statsDict=dict([(key,0) for key in statsKeys])
        trip=self.getTripbyIndex(tripIndex)
        timeList=[]
        for i in range(len(trip.keys())):
            timeList.append(0)
        distList=[]
        travel_time=0
        for index,(TravelID,details) in enumerate(trip.items()):
            travelmode=GoogleMapFunctions.matchmode(details['Final Mode'])
            origin=tuple([float(details['Start Lat']),float(details['Start Lon'])])
            destination=tuple([float(details['End Lat']),float(details['End Lon'])])
            if travelmode=='transit':
                transit_mode=GoogleMapFunctions.matchTransitMode(details['Final Mode'])
                dist=GoogleMapFunctions.getDistanceTransit(origin,destination,mode='transit',transitmode=transit_mode)
            else:
                dist=GoogleMapFunctions.getDistance(origin,destination,mode=travelmode)
            statsDict['Carbon Emission']+=self.calcCarbonFootprint(dist/1000.0,details['Final Mode'])
            distList.append(dist)
            timeList[int(details['Segment Order'])-1]=(tuple([details['Start Time'],details['End Time']]))
            start_time = self.getDateTimeFormat(details['Start Time'])
            end_time = self.getDateTimeFormat(details['End Time'])
            travel_time+=(end_time-start_time).total_seconds()/3600.0   #in hours
        
        start_time = self.getDateTimeFormat(timeList[0][0])
        end_time = self.getDateTimeFormat(timeList[-1][1])

        total_time=(end_time-start_time).total_seconds()/3600.0  #in hours
        transit_time=total_time-travel_time   #in hours
        total_dist=sum(distList)/1000.0   #in kilometer
        #print total_time
        statsDict['Transit Time']=transit_time
        statsDict['Travel Distance']=total_dist
        statsDict['Travel Time']=travel_time
        statsDict['Average Speed']=total_dist/travel_time

        return statsDict
        
    def calculateStatsforDate(self,date):
        #date is in this format: yyyy-mm-dd
        print date
        statsKeys=['Travel Time', 'Travel Distance', 'Average Speed', 'Transit Time', 'Carbon Emission']
        statsDict=dict([(key,0) for key in statsKeys])
        trip=self.getTripbyDate(date)
        if len(trip.keys())==0:
            return statsDict
        else:
            timeList=[]
            distList=[]
            travel_time=0
            triplist=set()
            for index,details in trip.items():
                triplist.update([int(details['Trip Index'])])
            for index in triplist:
                tempStatsDict=self.calculateStatsforTrip(index)
                statsDict['Transit Time']+=tempStatsDict['Transit Time']
                statsDict['Travel Distance']+=tempStatsDict['Travel Distance']
                statsDict['Travel Time']+=tempStatsDict['Travel Time']
                statsDict['Carbon Emission']+=tempStatsDict['Carbon Emission']
            statsDict['Average Speed']=statsDict['Travel Distance']/statsDict['Travel Time']
    
            return statsDict

    def calculateStatsCumulative(self):
        dates=[]
        statsKeys=['Travel Time', 'Distance','Transit Time', 'Carbon Emission']
        statsDict=dict([(key,0) for key in statsKeys])
        for tripID, details in self.dict['routes'].items():
            date=details['Start Time'].split(' ')[0]
            if date not in dates:
                dates.append(date)
        for date in dates:
            tempStatsDict=self.calculateStatsforDate(date)
            for key in statsKeys:
                try:
                    statsDict[key]+=tempStatsDict[key]
                except:
                    statsDict[key]+=0
        return statsDict
    
    def date_calc(self,date,days):
        start_date=dt.datetime.strptime(date,"%Y-%m-%d")
        end_date = start_date - timedelta(days)
        return end_date.strftime("%Y-%m-%d")

    def pie1(self,statsDict):
        labels = 'Transit Time','Travel Time'
        sizes = [statsDict['Transit Time']*3600,statsDict['Travel Time']*3600]
        colors=['gold','lightskyblue']
        plt.pie(sizes,labels=labels,autopct='%1.1f%%',colors=colors)
        plt.title('Fraction of Transit Time')
        plt.show()

    def plotStatistics(self,date=None,trip=None,cumulative=False,trend=False,period=None):
        #trip and date can only choose one to be True        
        if trend==False:
            #plot static statistics
            if cumulative==False:
                #plot trip or date
                if date:
                    statsDict=self.calculateStatsforDate(date)
                    self.pie1(statsDict)
                elif trip:
                    statsDict=self.calculateStatsforTrip(trip)
                    self.pie1(statsDict)
                else:
                    return None
                    
            elif cumulative==True:
                #plot all trips so far
                statsDict=self.calculateStatsCumulative()
                self.pie1(statsDict)
        elif trend==True:
            dist_list=[]
            time_list=[]
            carbon_list=[]
            speed_list=[]
            transit_list=[]
            #plot trend
            if date:
                date_list=[]
                for i in range(period):
                    end_date=self.date_calc(date,i)
                    date_list.append(end_date)
                    print end_date
                    statsDict=self.calculateStatsforDate(end_date)
                    dist_list.append(statsDict["Travel Distance"])
                    time_list.append(statsDict['Travel Time'])
                    carbon_list.append(statsDict['Carbon Emission'])
                    speed_list.append(statsDict["Average Speed"])
                    transit_list.append(statsDict["Transit Time"])


                x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in date_list]
                plt.figure(figsize=(10,10))                
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())

                plt.subplot(221)
                plt.plot(x,dist_list)
                plt.gcf().autofmt_xdate()
                plt.title("Travel Distance")

                plt.subplot(222)
                plt.plot(x,carbon_list)
                plt.gcf().autofmt_xdate()
                plt.title("Carbon Emission")

                plt.subplot(223)
                plt.plot(x,time_list,color='b',label='Travel')
                plt.plot(x,transit_list,color='r',label='Transit')
                plt.legend(loc='upper left', frameon=False)
                plt.gcf().autofmt_xdate()
                plt.title("Travel Time & Transit Time")

                plt.subplot(224)
                plt.plot(x,speed_list)
                plt.gcf().autofmt_xdate()
                plt.title("Average Speed")
                plt.show()
                
            elif trip:
                trip_list=[]
                for i in range(period):
                    statsDict=self.calculateStatsforTrip(trip-i)
                    trip_list.insert(0,trip-i)
                    dist_list.insert(0,statsDict["Travel Distance"])
                    time_list.insert(0,statsDict['Travel Time'])
                    carbon_list.insert(0,statsDict['Carbon Emission'])
                    speed_list.insert(0,statsDict["Average Speed"])
                    transit_list.insert(0,statsDict["Transit Time"])
                
                plt.figure(figsize=(10,10)) 
                
                plt.subplot(221)
                plt.plot(dist_list)
                plt.title("Travel Distance")

                plt.subplot(222)
                plt.plot(carbon_list)
                plt.title("Carbon Emission")

                plt.subplot(223)
                plt.plot(time_list,'b',label='Travel')
                plt.plot(transit_list,'r',label='Transit')
                plt.title("Travel Time & Transit Time")

                plt.subplot(224)
                plt.plot(trip_list,speed_list)
                plt.title("Average Speed")
                plt.show()
            


def test0():
    user643=User('643',CombinedDict)
    #trip10=user643.getTripbyIndex(10)
    #trip_02_19=user643.getTripbyDate('2016-02-19')
    #statistics_for_trip_10=user643.calculateStatsforTrip(10)
    #statistics_for_trip_02_19=user643.calculateStatsforDate('2016-03-02')

    user643.plotStatistics(date='2016-03-03',trend=True,period=7)
    #user643.plotStatistics(trip=20,trend=True,period=10)
    #user643.plotStatistics(date='2016-03-02')    
    #user643.plotStatistics(trip=10)    
    #user643.plotStatistics(cumulative=True)    



if __name__=="__main__":
    CombinedDict=readCombinedCSVUser(CombinedCsvFile)
    test0()