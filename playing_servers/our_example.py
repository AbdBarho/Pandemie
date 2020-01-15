#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest
import os
import sys , getopt

pathogenPriority=['lethality','mobility','infectivity','duration']
cityPriority=['population','connections','economy','government','hygiene','awareness' ]
symbolValues ={'++': 4,'+': 3,'o': 2,'-':1, '--':0}

PREVELANECETHRESHOLD = 0.1

# actions in a round
def deployMedication( pathogen , city ):
	return {"type": "deployMedication", "pathogen": pathogen['name'], "city": city['name']}

def developMedication( pathogen ):
	return {"type": "developMedication", "pathogen": pathogen['name']}

def deployVaccine( pathogen , city ):
	return {"type": "deployVaccine", "pathogen": pathogen['name'], "city": city['name']}

def developVaccine( pathogen ):
	return {"type": "developVaccine", "pathogen": pathogen['name']}

def closeConnection( fromcity , toCity , rounds ):
	return {"type": "closeConnection", "fromCity": fromcity['name'], "toCity": toCity['name'], "rounds": rounds}

def closeAirport(city, rounds):
	return {"type": "closeAirport", "city" : city['name']  , "rounds" : rounds}

def putUnderQuarantine( city , rounds ):
	return {"type": "putUnderQuarantine",	"city": city['name'] , "rounds": rounds }

def endRound():
	return {"type" : "endRound"}


## processing the rounddata to make it more readable
def preprocessInput( data ) :
	cityList = []
	for city in data['cities'] :
		if 'events' in data['cities'][city].keys() :
			cityList.append( data['cities'][city]  )
	cityList.sort( key=lambda x : int(x['population'] ) )
	numOccurrences = {}
	pathogenList = []
	for city in cityList :
		for event in city.get('events', []):
			if event['type'] == 'outbreak':
				pathogenName = event['pathogen']['name']
				if not event['pathogen'] in pathogenList:
					pathogenList.append(event['pathogen'])
				numOccurrences[pathogenName] = numOccurrences.get(pathogenName, 0) + 1

	#sort pathogenList by given filter
	pathogenListPrioritySorted = sortPathogenList( pathogenList )
	return pathogenListPrioritySorted, numOccurrences, cityList

# sort pathogens by priority list
def sortPathogenList( arr ) :
	for attr in pathogenPriority[::-1] :
		arr.sort( key=lambda x : symbolValues[x[attr]] , reverse=True)
	return arr

# definition of dangerous pathogens
def pathogenIsDangerous( pathogen ):
	for attr in pathogenPriority[:1] :
		if symbolValues[pathogen[attr]] < 3 :
			return False
	return True

#
def pickPathogen( pathogenArr , amountOfPathogensList ) :
	# check if current Pathogen is dangerous
	if len ( amountOfPathogensList ) > 1 :
		if ( pathogenIsDangerous( pathogenArr[0] ) and pathogenIsDangerous( pathogenArr[1] ) ) :
			if amountOfPathogensList[ pathogenArr[0]['name'] ] > amountOfPathogensList[ pathogenArr[1]['name']] and amountOfPathogensList[pathogenArr[1]['name']] == 1 :
				return pathogenArr[1]
	return pathogenArr[0]

def alreadyUnderQuarantine( city ) :
	for ev in city.get('events', []) :
		if ev['type'] == 'quarantine' :
			return True
	return False

def alreadyAirportClosed( city ) :
	for ev in city.get('events', []) :
		if ev['type'] == 'airportClosed' :
			return True
	return False

def medicationInDevelopment( pathogen , data ) :
	for ev in data.get('events', []) :
		if ( ev['type'] == 'medicationInDevelopment' and ev['pathogen']['name'] == pathogen['name'] ) :
			return True
	return False

def medicationAvailable( pathogen , data ) :
	for ev in data.get('events', []) :
		if ( ev['type'] == 'medicationAvailable' and ev['pathogen']['name'] == pathogen['name'] ) :
			return True
	return False

def medicationNotInDevAndNotAvail( pathogen , data ) :
	return not medicationInDevelopment( pathogen , data ) and not medicationAvailable( pathogen , data )

def medicationDeployed( pathogen , city , rounds ) :
	for ev in city.get('events', []) :
		if ev['type'] == 'medicationDeployed' :
			if ev['pathogen']['name'] == pathogen['name'] :
				return True
	return False

def vaccineInDevelopment( pathogen , data ):
	for ev in data.get('events', []) :
		if ( ev['type'] == 'vaccineInDevelopment' and ev['pathogen']['name'] == pathogen['name'] ) :
			return True
	return False

def vaccineAvailable( pathogen , data ) :
	for ev in data.get('events', []) :
		if ( ev['type'] == 'vaccineAvailable' and ev['pathogen']['name'] == pathogen['name'] ) :
			return True
	return False

def vaccineNotInDevAndNotAvail( pathogen ,data ) :
	return not vaccineInDevelopment( pathogen , data ) and not vaccineAvailable( pathogen , data )

def vaccineDeployed( pathogen , city ):
	for ev in city.get('events', []) :
		if ev['type'] == 'vaccineDeployed' :
			if ev['pathogen']['name'] == pathogen['name'] :
				return True
	return False



@post("/")
def index():
	game = request.json

	if (game['outcome'] != 'pending'):
		return endRound()

	currentPoints = int( game['points'] )
	currentPointReduction = 0

	# not enough points to do anything
	if ( currentPoints < 3 ):
		return endRound()

	# processing request
	pathogenList, amountOfPathogensList, cityList = preprocessInput(game)

	# chose most important pathogen
	chosenPathogen = pickPathogen( pathogenList , amountOfPathogensList )

	breakOuterLoop = False
	# find chosen city with chosen pathogen in it
	for city in cityList :
		for event in city.get('events', []):
			if event['type'] == 'outbreak' and event['pathogen']['name'] == chosenPathogen['name'] :
				chosenCity = city
				breakOuterLoop = True
				break
		if breakOuterLoop :
			break

	# check if pathogen is dangerous, and is in one city
	if ( pathogenIsDangerous( chosenPathogen ) and amountOfPathogensList[chosenPathogen['name']] == 1 ) :

		# if pathogen is mobile: quarantine
		if alreadyUnderQuarantine( chosenCity ) or currentPoints - currentPointReduction < 40 :
			# saving points to be able to keep quarantine up
			currentPointReduction = max ( 20 , currentPointReduction )

			# not able to to something
			if currentPoints-currentPointReduction <= 0 :
				return endRound()
		else :
			return putUnderQuarantine( chosenCity , min ( max (  (currentPoints-20) // 10 , 2 ) , 5 )  )


	# no quarantine or spare points
	if currentPoints - currentPointReduction > 100 :
		for pathogen in pathogenList :
			if vaccineNotInDevAndNotAvail ( pathogen , game ) :
				return developVaccine( pathogen )
			if medicationNotInDevAndNotAvail( pathogen , game ) :
				return developMedication( pathogen )

	# saving points
	if not pathogenIsDangerous( chosenPathogen ) :
		currentPointReduction = max ( 40 , currentPointReduction )

	# infectivity bigger than duration prefers vaccine
	if symbolValues[ chosenPathogen [ 'infectivity' ] ] > symbolValues[ chosenPathogen [ 'duration' ] ] :

		# if possible develop Vaccine
		if currentPoints - currentPointReduction >= 40 and vaccineNotInDevAndNotAvail( chosenPathogen , game ) :
			return developVaccine( chosenPathogen )

		# if possible develop Medication
		if currentPoints - currentPointReduction >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return developMedication( chosenPathogen )

	# duration bigger than infectivity
	else :

		# if possible develop Medication
		if currentPoints - currentPointReduction >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return developMedication( chosenPathogen )

		# if possible develop Vaccine
		if currentPoints - currentPointReduction >= 40 and vaccineNotInDevAndNotAvail( chosenPathogen , game ) :
			return developVaccine( chosenPathogen )

	# Medication and Vaccine already developed

	# infectivity bigger than duration prefers vaccine
	if symbolValues[ chosenPathogen [ 'infectivity' ] ] > symbolValues[ chosenPathogen [ 'duration' ] ] :

		# if possible develop Vaccine
		if currentPoints - currentPointReduction >= 5 and vaccineAvailable( chosenPathogen , game ) :
			return deployVaccine( chosenPathogen , chosenCity )

	# duration bigger than infectivity
	else :

		# if possible develop Medication
		if currentPoints - currentPointReduction >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return deployMedication( chosenPathogen , chosenCity )

	# develop Vaccine if not available
	if currentPoints - currentPointReduction > 40 :
		for pathogen in pathogenList :
			if vaccineInDevelopment( pathogen , game ) :
				continue
			if vaccineAvailable( pathogen , game ) :
				continue
			return developVaccine( pathogen )
	
	# develop Medication if not available 
	if currentPoints - currentPointReduction > 20 :
		for pathogen in pathogenList :
			if medicationInDevelopment( pathogen , game ) :
				continue
			if medicationAvailable( pathogen , game ) :
				continue
			return developMedication( pathogen )


	# deploy vaccine if plenty of points are available
	if currentPoints - currentPointReduction > 10 :
		for city in cityList :
			for ev in city.get('events', []) :
				if ev['type'] == 'outbreak' and vaccineAvailable( ev['pathogen'] , game ) and not vaccineDeployed ( ev['pathogen'] , city) :
					return deployVaccine(ev['pathogen'], city)

	# deploy medication if plenty of points are available
	if currentPoints - currentPointReduction > 5 :
		for city in cityList :
			for ev in city.get('events', []):
				if ev['type'] == 'outbreak' and medicationAvailable( ev['pathogen'] , game ) and ev['prevalence'] > PREVELANECETHRESHOLD :
					return deployMedication(ev['pathogen'], city)

	return endRound()

# server config through argument parsing 
# port and ip modification
args , vals = getopt.getopt( sys.argv[1:] , ["i:p:"] , ["ip=" , "port="] )
ip = "0.0.0.0"
port = 50123
for arg , val in args :
	if arg in ["-i" , "--ip" ] :
		ip=val
	elif arg in ["-p" , "--port" ] :
		port=int ( val )

# server run 
BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host=ip, port=port, quiet=True)
