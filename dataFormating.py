# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:29:17 2016

@author: minglong_zhou
"""
import GoogleMapFunctions as gm
import numpy as np
import csv
import sys
import json
import db
import datetime as dt

TravelCsvFile="travel_summary_all.csv"
StopCsvFile="stops_summary_all.csv"
CombinedCsvFile="combined.csv"

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
                'Segment Order',
                'Validated?']

    writer=csv.DictWriter(combinedCSV,fieldNames)
    writer.writeheader()
    k=1
    segmentOrder=1
    temp=None
    for row in readerTravel:
        try:
            if row2['Main Activity']=='Change Mode/Transfer':
                dtDelta=getDateTimeFormat(row['Start Time'])-getDateTimeFormat(temp['Start Time'])
                if dtDelta.total_seconds()>3600:
                    k+=1
                    segmentOrder=1
        except:
            pass
        temp=row
        temp['Travel/Stop']='Travel'
        temp['Trip Index']=k
        temp['Segment Order']=segmentOrder
        temp['Main Activity']=''
        writer.writerow({fieldname:temp[fieldname] for fieldname in fieldNames})
        for row2 in readerStop:
            if row2['Stop ID']==row['Travel ID'].split('-')[1]:
                segmentOrder+=1
                temp2=row2
                temp2['Travel ID']=row2['Stop ID']
                temp2['Travel/Stop']='Stop'
                temp2['Trip Index']=''
                temp2['Start Lat']=''
                temp2['Start Lon']=''
                temp2['End Lat']=row2['Final lat']
                temp2['End Lon']=row2['Final lon']
                temp2['Segment Order']=''
                temp2['Duration (Seconds)']=row2['Duration (sec)']
                writer.writerow({fieldname2:temp2[fieldname2] for fieldname2 in fieldNames})
                if row2['Main Activity']!='Change Mode/Transfer':
                    k+=1
                    segmentOrder=1
                elif row2['Main Activity']=='Change Mode/Transfer':
                    dtDelta=getDateTimeFormat(row2['End Time'])-getDateTimeFormat(row2['Start Time'])
                    if dtDelta.total_seconds()>3600:
                        k+=1
                break
        
    travelCSV.close()
    stopCSV.close()
    combinedCSV.close()
def getDateTimeFormat(datetimeStr):
    #'2016-02-02 19:30:30'
    time_seg=datetimeStr.split(' ')[0]+' '+datetimeStr.split(' ')[1]
    datetimeObj=dt.datetime.strptime(time_seg,'%Y-%m-%d %H:%M:%S')
    return datetimeObj    
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
                # TravelID=row['Travel ID']
                TravelID = tuple(TravelID)
            except:
                TravelID=row['Stop ID']
            try:
                print TravelID
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
            TravelID=row['Travel ID']
            if len(TravelID) == 7:
                try:
                    CombinedDict[row['User ID']]['stops'][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
                except:
                    CombinedDict[row['User ID']]=dict()
                    CombinedDict[row['User ID']]['routes']=dict()
                    CombinedDict[row['User ID']]['stops']=dict()
                    CombinedDict[row['User ID']]['stops'][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
            else:
                try:
                    CombinedDict[row['User ID']]['routes'][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
                except:
                    CombinedDict[row['User ID']]=dict()
                    CombinedDict[row['User ID']]['routes']=dict()
                    CombinedDict[row['User ID']]['stops']=dict()
                    CombinedDict[row['User ID']]['routes'][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
            # TravelID=row['Travel ID'].split('-')
            # TravelID=row['Travel ID']
            # TravelID = tuple(TravelID)
            # try:
            #     CombinedDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
            # except:
            #     CombinedDict[row['User ID']]=dict()
            #     CombinedDict[row['User ID']][TravelID]={fieldname:row[fieldname] for fieldname in Fieldnames}
    return CombinedDict

def addStop(stop):
    lat, lng = stop['End Lat'], stop['End Lon']
    # results = geocoder.google(coordinates, method='reverse')
    try:
    # print 'Performing reverse geocode'
        results = gm.reverseGeocodeList(lat, lng)
        node = {}
        node['lat'], node['lon'] = results[1]['LatLon']
        node['name'] = results[1]['name']
        db.add_node(node)
    except Exception as e:
        print 'addStop', e

def processData(combined):
    for i in combined:
        for stop_id in combined[i]['stops']:
            stop = combined[i]['stops'][stop_id]
            # addStop(stop)
        for route_id in combined[i]['routes']:
            origin, dest = route_id.split('-')

            # route_details = combined[i]['routes'][route_id]

if __name__=="__main__":
    combineCSV(TravelCsvFile,StopCsvFile,CombinedCsvFile)  #iniitalizing combined CSV
    #TravelDict=readCSVUser(TravelCsvFile)
    #StopDict=readCSVUser(StopCsvFile)
    CombinedDict=readCombinedCSVUser(CombinedCsvFile)
    # with open('output.json','w') as f:
    #     f.write(json.dumps(CombinedDict, sort_keys = True, ensure_ascii=False))
    #processData(CombinedDict)




