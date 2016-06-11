
import googlemaps
from googlemaps import Client


gmaps = Client('AIzaSyDdipvR3QRKC2NF4ueiculh8LuT-061zPQ')
def get_distance(start,end,mode):
	directions = gmaps.directions(start,end,mode=match_mode(mode),transit_mode=match_transit_mode(mode))
	if directions!=[]:
		dist=directions[0]['legs'][0]['distance']['value']
		return dist
	else:
		return 'NA'

def get_directions(start,end,mode):
	directions = gmaps.directions(start,end,mode=match_mode(mode),transit_mode=match_transit_mode(mode))
	steps=[]
	if directions!=[]:
		for step in directions[0]['legs'][0]['steps']:
			steps.append((step['html_instructions'],step['distance']['text']))
		return steps
		# for step in directions[0]['legs'][0]['steps']:
		# 	print step['html_instructions'],step['distance']['text']
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

#test data
start='1.340103225,103.9601385'
end='1.353448427,103.9453669'
mode='transit'
print get_directions(start,end,mode)