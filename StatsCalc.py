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
        self.dict=dictionary
    def getTrip(self,tripid):
        pass
    def calculateStats(self):
        pass
    def plotStatistics(self):
        pass


if __name__=="__main__":
    CombinedDict=readCombinedCSVUser(CombinedCsvFile)
