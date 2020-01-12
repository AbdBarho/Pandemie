#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest
import os
import sys , getopt
filepath='../collected_data/{__file__.split(".")[0]}.csv'

pathogenPriority=['lethality','mobility','infectivity','duration']
pathogenPriorityExponent=[1,1,1,1]
cityPriority=['population','connections','economy','government','hygiene','awareness' """,'events','longitude','latitude'"""]
symbolValues ={'++': 4,'+': 3,'o': 2,'-':1, '--':0}

DEBUG = True
ROUNDCHOSEN = True 
PREVELANECETHRESHOLD = 0.1
# actions in a round 
def deployMedication( pathogen , city ):
	if ROUNDCHOSEN :
		print ( 'deployMedication ' , pathogen['name'] , ' ' , city['name'] )
	return {"type": "deployMedication", "pathogen": pathogen['name'], "city": city['name']}

def developMedication( pathogen ):
	if ROUNDCHOSEN :
		print( 'developMedication' , pathogen['name'] )
	return {"type": "developMedication", "pathogen": pathogen['name']}

def deployVaccine( pathogen , city ):
	if ROUNDCHOSEN :
		print( 'devployVaccine ' , pathogen['name'] , ' ' , city['name'] )
	return {"type": "deployVaccine", "pathogen": pathogen['name'], "city": city['name']}

def developVaccine( pathogen ):
	if ROUNDCHOSEN :
		print( 'developVaccine' , pathogen['name'] )
	return {"type": "developVaccine", "pathogen": pathogen['name']}

def closeConnection( fromcity , tocity , rounds ):
	if ROUNDCHOSEN :
		print( f'closeConnection from : {fromcity} to: {tocity} for {rounds} rounds' )
	return {"type": "closeConnection" , "fromCity"	 : fromcity['name'] , "toCity" : tocity['name'] , "rounds" : rounds}

def closeAirport( city , rounds ):
	if ROUNDCHOSEN :
		print( 'closeAirport' )	
	return {"type": "closeAirport", "city" : city['name']  , "rounds" : rounds}

def putUnderQuarantine( city , rounds ):
	if ROUNDCHOSEN :
		print( f'putUnderQuarantine {rounds} ' )	
	return {"type": "putUnderQuarantine",	"city": city['name'] , "rounds": rounds }

def endRound():
	if ROUNDCHOSEN :
		print( 'endRound' )	
	return {"type" : "endRound"} 


## processing the rounddata to make it more readable 
def preprocessInput( data ) :
	cityList = []
	for city in data['cities'] :
		if 'events' in data['cities'][city].keys() :
			cityList.append( data['cities'][city]  )
	cityList.sort( key=lambda x : int(x['population'] ) )
	amountOfPathogensList = {}
	pathogenList = []
	for city in cityList :
		if 'events' in city :
			for event in city['events']:
				if event['type'] == 'outbreak' :
					if not event['pathogen'] in pathogenList :
						pathogenList.append( event['pathogen'] )
						amountOfPathogensList[event['pathogen']['name']] = 1
					else:
						amountOfPathogensList[event['pathogen']['name']] += 1
	
	#sort pathogenList by given filter
	pathogenListPrioritySorted = sortPathogenList( pathogenList ) 
	return pathogenListPrioritySorted, amountOfPathogensList , cityList 
	
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
	if not 'events' in city.keys() :
		return False
	for ev in city['events'] :
		if ev['type'] == 'quarantine' :
			return True
	return False 

def alreadyAirportClosed( city ) :
	if 'events' in city.keys() :
		for ev in city['events'] :
			if ev['type'] == 'airportClosed' : 
				return True
	return False 

def medicationInDevelopment( pathogen , data ) :
	if 'events' in data.keys() :
		for ev in data['events'] :
			if ( ev['type'] == 'medicationInDevelopment' and ev['pathogen']['name'] == pathogen['name'] ) :
				return True 
	return False

def medicationAvailable( pathogen , data ) : 
	if 'events' in data.keys() :
		for ev in data['events'] :
			if ( ev['type'] == 'medicationAvailable' and ev['pathogen']['name'] == pathogen['name'] ) :
				return True
	return False

def medicationNotInDevAndNotAvail( pathogen , data ) : 
	return not medicationInDevelopment( pathogen , data ) and not medicationAvailable( pathogen , data ) 

def medicationDeployed( pathogen , city , rounds ) :
	for ev in city['events'] :
		if ev['type'] == 'medicationDeployed' :
			if ev['pathogen']['name'] == pathogen['name'] :
				return True
	return False	

def vaccineInDevelopment( pathogen , data ):
	if 'events' in data.keys() :
		for ev in data['events'] :
			if ( ev['type'] == 'vaccineInDevelopment' and ev['pathogen']['name'] == pathogen['name'] ) :
				return True 
	return False
 
def vaccineAvailable( pathogen , data ) :
	if 'events' in data.keys() :
		for ev in data['events'] :
			if ( ev['type'] == 'vaccineAvailable' and ev['pathogen']['name'] == pathogen['name'] ) :
				return True
	return False 

def vaccineNotInDevAndNotAvail( pathogen ,data ) :
	return not vaccineInDevelopment( pathogen , data ) and not vaccineAvailable( pathogen , data ) 

def vaccineDeployed( pathogen , city , rounds ):
	for ev in city['events'] :
		if ev['type'] == 'vaccineDeployed' :
			if ev['pathogen']['name'] == pathogen['name'] :
				return True
	return False



@post("/")
def index():
	game = request.json

	if DEBUG :	
		if 'error' in game.keys() :
			print( game[ 'error' ] ) 

	if ( game['outcome'] == 'pending' ) :	
		currentPoints = int( game['points'] ) 
		# not enough points 
		if ( int ( game["points"] ) < 3 ):
			return endRound() 

		# processing request 
		pathogenList, amountOfPathogensList, cityList = preprocessInput( game )	
		if len( pathogenList ) != 0 :
			
			# chose most important pathogen  
			chosenPathogen = pickPathogen( pathogenList , amountOfPathogensList )

			breakOuterLoop = False
			# init chosen City
			chosenCity = cityList[0] 
			
			# find chosen city with chosen pathogen in it
			for city in cityList :
				if 'events' in city.keys() :
					for event in city['events'] :	
						if event['type'] == 'outbreak' and event['pathogen']['name'] == chosenPathogen['name'] :
							chosenCity = city
							breakOuterLoop = True
							break
				if breakOuterLoop :
					break

			# check if pathogen is dangerous 
			if ( pathogenIsDangerous( chosenPathogen ) and amountOfPathogensList[chosenPathogen['name']] == 1 ) :

				# if pathogen is mobile qarantine 
				if symbolValues[chosenPathogen['mobility']] >= 3 :
					
					if alreadyUnderQuarantine( chosenCity ) :
						
						# saving points to be able to keep qarantine up
						currentPoints -= 20 							
						
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
						
						# saving points for next round	
						if currentPoints <= 0 :
							return endRound() 
					
					else : 
						return closeAirport( chosenCity , min ( ( currentPoints -15 )  // 5 , 5 ) ) 
					
			### nether quarantine nor airport is closed or spare points 
			print ( f'decided against qarantine' )
			if int ( game['points']) > 100 : 
				for pathogen in pathogenList :
					if vaccineNotInDevAndNotAvail ( pathogen , game ) :
						return developVaccine( pathogen ) 
					if medicationNotInDevAndNotAvail( pathogen , game ) :
						return developMedication( pathogen )
			
			if int(game['points']) > 60 :
				for pathogen in pathogenList : 
					print ( f'pathogen : {pathogen}' )
					print ( f'chosen pathogen : {chosenPathogen} , {pathogen == chosenPathogen}'  )
					 	
			
			print ( int ( game['points'])  > 100  )	

			# saving points  ? 
			if not pathogenIsDangerous( chosenPathogen ) :
				currentPoints -= 40 
			
			# infectivity bigger than duration preferes vaccine
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
						
			# infectivity bigger than duration preferes vaccine
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
				if 'event' in city.keys() :
					for ev in city['events'] :
						if ev['type'] == 'outbreak' and vaccineAvailable( ev['pathogen'] , game ) and not vaccineDeployed ( ev['pathogen'] , city , ) :
							return deployVaccine( city , ev['pathogen'] ) 

		# deploy medication if plenty of points are available 
		if currentPoints > 5 :
			for city in cityList :
				if 'event' in city.keys() :
					for ev in city['events'] :
						if ev['type'] == 'outbreak' and medicationAvailable( ev['pathogen'] , game ) and ev['prevelance'] > PREVELANECETHRESHOLD :
							return deployMedication( city , ev['pathogen'] ) 
			
					
		
		if ROUNDCHOSEN :
			print( f'nothing has been done -> no loop, points : {game["points"]}  amount of pathogens: {len(pathogenList)}' )
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
