# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 03:09:28 2016

@author: minglong_zhou
"""

#==============================================================================
# Use : CombinedDict
# CombinedDict is {User ID: 
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
#                              validated?:
#                             }
#                         }
#                 }
# 
#==============================================================================



from dataFormating import *
import GoogleMapFunctions


class User():
    def __init__(self,userid,dictionary):
        self.userid=userid
        self.dict=dictionary[userid]
        
    def getTrip(self,tripIndex):
        trip=[{(key,self.dict[key]) for key in self.dict.keys() if (self.dict[key]['Trip Index']==tripIndex and self.dict[key]['Travel/Stop']=='Travel')}]
        return trip
        
    def calculateStatsforTrip(self,tripIndex):
        pass
    def plotStatistics(self):
        pass


if __name__=="__main__":
    CombinedDict=readCombinedCSVUser(CombinedCsvFile)
