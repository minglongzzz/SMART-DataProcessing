# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:29:17 2016

@author: minglong_zhou
"""

import numpy as np
import time
import datetime
import csv
import sys

TravelCsvFile="/Users/minglong_zhou/Documents/Singapore/SUTD/Undergraduate/Year_3/Term8/Capstone 2/travel_summary_all.csv"
StopCsvFile="/Users/minglong_zhou/Documents/Singapore/SUTD/Undergraduate/Year_3/Term8/Capstone 2/stops_summary_all.csv"
CombinedCsvFile="/Users/minglong_zhou/Documents/Singapore/SUTD/Undergraduate/Year_3/Term8/Capstone 2/combined.csv"

def combineCSV(travelfile,stopfile,combinedfile):
    
    travelCSV=open(travelfile,'r')
    stopCSV=open(stopfile,'r')
    combinedCSV=open(combinedfile,'w')
    combinedCSV.truncate()
    readerTravel=csv.DictReader(travelCSV)
    readerStop=csv.DictReader(stopCSV)
    #fieldNames=readerTravel.fieldnames
    #fieldNames.insert(2,'Travel/Stop')
    fieldNames=['Travel ID',
                'User ID',
                'Travel/Stop',
                'Trip Index',
                'Start Time',
                'End Time',
                'Duration (Seconds)',
                'Start Lat',
                'Start Lon',
                'End Lat',
                'End Lon',
                'Final Mode',
                'Predicted Mode',
                'Main Activity',
                'Validated?']

    writer=csv.DictWriter(combinedCSV,fieldNames)
    writer.writeheader()
    k=1
    for row in readerTravel:
        temp=row
        temp['Travel/Stop']='Travel'
        temp['Trip Index']=k
        temp['Main Activity']=''
        writer.writerow({fieldname:temp[fieldname] for fieldname in fieldNames})
        for row2 in readerStop:
            if row2['Stop ID']==row['Travel ID'].split('-')[1]:
                temp2=row2
                temp2['Travel ID']=row2['Stop ID']
                temp2['Travel/Stop']='Stop'
                temp2['Trip Index']=''
                temp2['Start Lat']=''
                temp2['Start Lon']=''
                temp2['End Lat']=row2['Final lat']
                temp2['End Lon']=row2['Final lon']
                temp2['Duration (Seconds)']=row2['Duration (sec)']
                writer.writerow({fieldname2:temp2[fieldname2] for fieldname2 in fieldNames})
                if row2['Main Activity']!='Change Mode/Transfer':
                    k+=1
                break
        
    travelCSV.close()
    stopCSV.close()
    combinedCSV.close()
    
    
#Read Seperated CSV Files(Travel CSV or Stop CSV)
#return dict({User: {Travel/Stop ID: {details} } })
def readCSVUser(Csvfile):
    TravelDict=dict()
    with open(Csvfile,'r') as travelCsv:
        reader=csv.DictReader(travelCsv)
        TravelFieldnames=travelCsv.readline().strip().split(',')
        travelCsv.seek(0)
        for row in reader:
            try:
                TravelID=row['Travel ID'].split('-')
                TravelID = tuple(TravelID)
            except:
                TravelID=row['Stop ID']
            try:
                TravelDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in TravelFieldnames}
            except:
                TravelDict[row['User ID']]=dict()
                TravelDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in TravelFieldnames}
    return TravelDict

def readCombinedCSVUser(Csvfile):
    CombinedDict=dict()
    with open(Csvfile,'r') as combinedCsv:
        reader=csv.DictReader(combinedCsv)
        Fieldnames=combinedCsv.readline().strip().split(',')
        combinedCsv.seek(0)
        for row in reader:
            TravelID=row['Travel ID'].split('-')
            TravelID = tuple(TravelID)
            try:
                CombinedDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
            except:
                CombinedDict[row['User ID']]=dict()
                CombinedDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
    return CombinedDict
    
    
def formatDictUser(travelDict,stopDict):
    TravelDict=dict()
    for user in travelDict.keys():
        TravelDict[user]=dict()
        for index,tripDetails in enumerate(travelDict[user].items()):
            if stopDict[user][tripDetails[0]]['Main Activity']=="Change Mode/Transfer":
                start=tripDetails[0]
                for index2,tripDetails2 in enumerate(travelDict[user].items()):
                    pass
            pass
        pass
        
    return TravelDict




if __name__=="__main__":
    #combineCSV(TravelCsvFile,StopCsvFile,CombinedCsvFile)  #iniitalizing combined CSV
    #TravelDict=readCSVUser(TravelCsvFile)
    #StopDict=readCSVUser(StopCsvFile)
    CombinedDict=readCombinedCSVUser(CombinedCsvFile)




