#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest
import os
import sys , getopt
filepath='../collected_data/{__file__.split(".")[0]}.csv'

pathogenPriority=['lethality','mobility','infectivity','duration']
pathogenPriorityExponent=[1,1,1,1]
cityPriority=['population','connections','economy','government','hygiene','awareness' """,'events','longitude','latitude'"""]
symbolValues ={'++': 4,'+': 3,'o': 2,'-':1, '--':0}

DEBUG = False
PREVELANECETHRESHOLD = 0.1

def p(*args):
	if DEBUG:
		print(*args)

# actions in a round
def deployMedication( pathogen , city ):
	p('deployMedication ', pathogen['name'], ' ', city['name'])
	return {"type": "deployMedication", "pathogen": pathogen['name'], "city": city['name']}

def developMedication( pathogen ):
	p('developMedication', pathogen['name'])
	return {"type": "developMedication", "pathogen": pathogen['name']}

def deployVaccine( pathogen , city ):
	p('deployVaccine ', pathogen['name'], ' ', city['name'])
	return {"type": "deployVaccine", "pathogen": pathogen['name'], "city": city['name']}

def developVaccine( pathogen ):
	p('developVaccine', pathogen['name'])
	return {"type": "developVaccine", "pathogen": pathogen['name']}

def closeConnection( fromcity , toCity , rounds ):
	p(f'closeConnection from : {fromcity} to: {toCity} for {rounds} rounds')
	return {"type": "closeConnection", "fromCity": fromcity['name'], "toCity": toCity['name'], "rounds": rounds}

def closeAirport(city, rounds):
	p('closeAirport')
	return {"type": "closeAirport", "city" : city['name']  , "rounds" : rounds}

def putUnderQuarantine( city , rounds ):
	p(f'putUnderQuarantine {rounds} ')
	return {"type": "putUnderQuarantine",	"city": city['name'] , "rounds": rounds }

def endRound():
	p('endRound\n-----')
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

	if 'error' in game.keys() :
		print( '******\nERROR IN REQUEST\n', game[ 'error' ], '\n*****' )

	if (game['outcome'] != 'pending'):
		print('outcome', game['outcome'])
		return endRound()

	currentPoints = int( game['points'] )
	# not enough points
	if ( currentPoints < 3 ):
		return endRound()

	# processing request
	pathogenList, amountOfPathogensList, cityList = preprocessInput(game)

	if len(pathogenList) == 0:
		p('no pathogens? should have already won')
		return endRound()

	# chose most important pathogen
	chosenPathogen = pickPathogen( pathogenList , amountOfPathogensList )

	breakOuterLoop = False
	# init chosen City
	chosenCity = cityList[0]

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
		if symbolValues[chosenPathogen['mobility']] >= 3 :
			if alreadyUnderQuarantine( chosenCity ) :
				# saving points to be able to keep quarantine up
				currentPoints -= 20
				p('saving 20 for next round to quarantine')

				# not able to to something
				if currentPoints <= 0 :
					return endRound()
			else :
				return putUnderQuarantine( chosenCity , min ( (currentPoints-20) // 10 , 5 ) )

		# if pathogen is not mobile
		else :
			if alreadyAirportClosed( chosenCity ) :
				# saving points to be able to keep airport closed
				currentPoints -= 10
				p('saving 10 for next round to keep airport closed')
				# saving points for next round
				if currentPoints <= 0 :
					return endRound()
			else :
				return closeAirport( chosenCity , min ( ( currentPoints -15 )  // 5 , 5 ) )

	### nether quarantine nor airport is closed or spare points
	p('decided against quarantine')
	if currentPoints > 100 :
		for pathogen in pathogenList :
			if vaccineNotInDevAndNotAvail ( pathogen , game ) :
				return developVaccine( pathogen )
			if medicationNotInDevAndNotAvail( pathogen , game ) :
				return developMedication( pathogen )

	if currentPoints > 60 :
		for pathogen in pathogenList :
			p(f'pathogen : {pathogen}')
			p(f'chosen pathogen : {chosenPathogen} , {pathogen == chosenPathogen}')

	p('more than 100 points:', currentPoints > 100)

	# saving points  ?
	if not pathogenIsDangerous( chosenPathogen ) :
		currentPoints -= 40
		p('saving 40 points ?')

	# infectivity bigger than duration prefers vaccine
	if symbolValues[ chosenPathogen [ 'infectivity' ] ] > symbolValues[ chosenPathogen [ 'duration' ] ] :

		# if possible develop Vaccine
		if currentPoints >= 40 and vaccineNotInDevAndNotAvail( chosenPathogen , game ) :
			return developVaccine( chosenPathogen )

		# if possible develop Medication
		if currentPoints >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return developMedication( chosenPathogen )

	# duration bigger than infectivity
	else :

		# if possible develop Medication
		if currentPoints >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return developMedication( chosenPathogen )

		# if possible develop Vaccine
		if currentPoints >= 40 and vaccineNotInDevAndNotAvail( chosenPathogen , game ) :
			return developVaccine( chosenPathogen )

	# Medication and Vaccine already developed

	# infectivity bigger than duration prefers vaccine
	if symbolValues[ chosenPathogen [ 'infectivity' ] ] > symbolValues[ chosenPathogen [ 'duration' ] ] :

		# if possible develop Vaccine
		if currentPoints >= 5 and vaccineAvailable( chosenPathogen , game ) :
			return deployVaccine( chosenPathogen , chosenCity )

	# duration bigger than infectivity
	else :

		# if possible develop Medication
		if currentPoints >= 20 and medicationNotInDevAndNotAvail( chosenPathogen , game ) :
			return deployMedication( chosenPathogen , chosenCity )


	if currentPoints > 40 :
		for pathogen in pathogenList :
			if vaccineInDevelopment( pathogen , game ) :
				continue
			if vaccineAvailable( pathogen , game ) :
				continue
			return developVaccine( pathogen )

	if currentPoints > 20 :
		for pathogen in pathogenList :
			if medicationInDevelopment( pathogen , game ) :
				continue
			if medicationAvailable( pathogen , game ) :
				continue
			return developMedication( pathogen )


	# deploy vaccine if plenty of points are available
	if currentPoints > 10 :
		for city in cityList :
			for ev in city.get('events', []) :
				if ev['type'] == 'outbreak' and vaccineAvailable( ev['pathogen'] , game ) and not vaccineDeployed ( ev['pathogen'] , city) :
					return deployVaccine(ev['pathogen'], city)

	# deploy medication if plenty of points are available
	if currentPoints > 5 :
		for city in cityList :
			for ev in city.get('events', []):
				if ev['type'] == 'outbreak' and medicationAvailable( ev['pathogen'] , game ) and ev['prevalence'] > PREVELANECETHRESHOLD :
					return deployMedication(ev['pathogen'], city)

	p(f'nothing has been done -> no loop, points : {game["points"]}, amount of pathogens: {len(pathogenList)}')
	return endRound()

args , vals = getopt.getopt( sys.argv[1:] , ["i:p:"] , ["ip=" , "port="] )
ip = "0.0.0.0"
port = 50123
for arg , val in args :
	if arg in ["-i" , "--ip" ] :
		ip=val
	elif arg in ["-p" , "--port" ] :
		port=int ( val )

BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host=ip, port=port, quiet=True)
