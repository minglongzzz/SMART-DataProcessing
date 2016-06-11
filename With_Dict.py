import googlemaps
from googlemaps import Client
import csv
from collections import OrderedDict

gmaps = Client('AIzaSyDdipvR3QRKC2NF4ueiculh8LuT-061zPQ')

def get_distance(start,end,mode):
	directions = gmaps.directions(start,end,mode=match_mode(mode),transit_mode=match_transit_mode(mode))
	if directions!=[]:
		dist=directions[0]['legs'][0]['distance']['value']
		return dist
	else:
		return 'NA'

def match_mode(mode):
	if mode == 'Car/Van' or mode=='Motorcycle/Scooter':
		return 'driving'
	elif mode=='Foot':
		return 'walking'
	elif mode=='LRT/MRT' or mode =='Bus':
		return 'transit'
	elif mode =='Bicycle':
		return 'bicycling'
	else:
		return None

def match_transit_mode(mode):
	if mode=='LRT/MRT':
		return 'train'
	elif mode =='Bus':
		return 'bus'
	else:
		return None

def read_data(stop,travel):
	f1=open(stop,'r')
	f2=open(travel,'r')
	f1reader=csv.reader(f1)
	f1data1=list(f1reader)
	f2reader=csv.reader(f2)
	f2data=list(f2reader)
	f1data1=f1data1[1:]
	f2data=f2data[1:]
	for i in f2data:
		i[0]=i[0].split('-')[0]
	f1data = []
	for i in f1data1:
		if i not in f1data:
			f1data.append(i)
	data=OrderedDict()
	keys = ['ID','Trip ID','Trip distance','Travel/Stop','userID','Start time','End time','duration','Start lat','Start lon','End lat','End lon','Mode','Main Activity','Validated?']
	for i in keys:
		data[i]=[]
		data[i]=[]
	tripID=0
	dist=0
	for i in f1data:
		k=0
		for j in f2data:
			if i[0]==j[0] and i[23]=='Change Mode/Transfer':
				k=1
				try:
					dist+=get_distance(j[6]+','+j[7],j[8]+','+j[9],j[10])
				except:
					dist+=0
				data['ID'].append(i[0])
				data['Trip ID'].append(tripID)
				data['Trip distance'].append('')
				data['Travel/Stop'].append('Stop')
				data['userID'].append(i[1])
				data['Start time'].append(i[2])
				data['End time'].append(i[3])
				data['duration'].append(i[7])	
				data['Start lat'].append('')
				data['Start lon'].append('')
				data['End lat'].append(i[8])
				data['End lon'].append(i[9])
				data['Mode'].append(i[12])
				data['Main Activity'].append(i[23])
				data['Validated?'].append(i[16])

				data['ID'].append(j[0])
				data['Trip ID'].append(tripID)
				data['Trip distance'].append(dist)
				data['Travel/Stop'].append('Travel')
				data['userID'].append(j[1])
				data['Start time'].append(j[2])
				data['End time'].append(j[3])
				data['duration'].append(j[5])	
				data['Start lat'].append(j[6])
				data['Start lon'].append(j[7])
				data['End lat'].append(j[8])
				data['End lon'].append(j[9])
				data['Mode'].append(j[10])
				data['Main Activity'].append('')
				data['Validated?'].append(j[13])

				# outputWriter.writerow([i[0],tripID,'','Stop',i[1],i[2],i[3],i[7],'','',i[8],i[9],i[12],i[23],i[16]])
				# outputWriter.writerow([j[0],tripID,dist,'Travel',j[1],j[2],j[3],j[5],j[6],j[7],j[8],j[9],j[10],'',j[13]])
				break
			elif i[0]==j[0]:
				k=1
				tripID+=1
				try:
					dist=get_distance(j[6]+','+j[7],j[8]+','+j[9],j[10])
				except:
					dist=0
				data['ID'].append(i[0])
				data['Trip ID'].append('')
				data['Trip distance'].append('')
				data['Travel/Stop'].append('Stop')
				data['userID'].append(i[1])
				data['Start time'].append(i[2])
				data['End time'].append(i[3])
				data['duration'].append(i[7])	
				data['Start lat'].append('')
				data['Start lon'].append('')
				data['End lat'].append(i[8])
				data['End lon'].append(i[9])
				data['Mode'].append(i[12])
				data['Main Activity'].append(i[23])
				data['Validated?'].append(i[16])

				data['ID'].append(j[0])
				data['Trip ID'].append(tripID)
				data['Trip distance'].append(dist)
				data['Travel/Stop'].append('Travel')
				data['userID'].append(j[1])
				data['Start time'].append(j[2])
				data['End time'].append(j[3])
				data['duration'].append(j[5])	
				data['Start lat'].append(j[6])
				data['Start lon'].append(j[7])
				data['End lat'].append(j[8])
				data['End lon'].append(j[9])
				data['Mode'].append(j[10])
				data['Main Activity'].append('')
				data['Validated?'].append(j[13])
				# outputWriter.writerow([i[0],'','','Stop',i[1],i[2],i[3],i[7],'','',i[8],i[9],i[12],i[23],i[16]])
				# outputWriter.writerow([j[0],tripID,dist,'Travel',j[1],j[2],j[3],j[5],j[6],j[7],j[8],j[9],j[10],'',j[13]])
				break
		if k==0 and i[23]=='Change Mode/Transfer':
				data['ID'].append(i[0])
				data['Trip ID'].append(tripID)
				data['Trip distance'].append('')
				data['Travel/Stop'].append('Stop')
				data['userID'].append(i[1])
				data['Start time'].append(i[2])
				data['End time'].append(i[3])
				data['duration'].append(i[7])	
				data['Start lat'].append('')
				data['Start lon'].append('')
				data['End lat'].append(i[8])
				data['End lon'].append(i[9])
				data['Mode'].append(i[12])
				data['Main Activity'].append(i[23])
				data['Validated?'].append(i[16])
			# outputWriter.writerow([i[0],tripID,'','Stop',i[1],i[2],i[3],i[7],'','',i[8],i[9],i[12],i[23],i[16]])
		elif k==0:
			tripID+=1
			data['ID'].append(i[0])
			data['Trip ID'].append('')
			data['Trip distance'].append('')
			data['Travel/Stop'].append('Stop')
			data['userID'].append(i[1])
			data['Start time'].append(i[2])
			data['End time'].append(i[3])
			data['duration'].append(i[7])	
			data['Start lat'].append('')
			data['Start lon'].append('')
			data['End lat'].append(i[8])
			data['End lon'].append(i[9])
			data['Mode'].append(i[12])
			data['Main Activity'].append(i[23])
			data['Validated?'].append(i[16])
			# outputWriter.writerow([i[0],'','','Stop',i[1],i[2],i[3],i[7],'','',i[8],i[9],i[12],i[23],i[16]])

	return data

def output(data):
	output=open('output.csv','w')
	outputWriter=csv.writer(output)
	outputWriter.writerow(data.keys())
	for i,item in enumerate(data['ID']):
		trans=[]
		for key in data.keys():
			trans.append(data[key][i])
		outputWriter.writerow(trans)
	output.close()

data=read_data('stops_summary_all_2016-02-09_2016-06-06.csv','travel_summary_all_2016-02-09_2016-06-06.csv')
output(data)