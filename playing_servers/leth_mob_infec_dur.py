#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest
import os

filepath='../collected_data/{__file__.split(".")[0]}.csv'

pathogenPriority=['lethality','mobility','infectivity','duration']
pathogenPriorityExponent=[1,1,1,1]
cityPriority=['population','connections','economy','government','hygiene','awareness' """,'events','longitude','latitude'"""]
symbolValues ={'++': 4,'+': 3,'o': 2,'-':1, '--':0}

DEBUG = False
ROUNDCHOSEN = False
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
		print( 'closeConnection' )
	return {"type": "closeConnection" , "fromCity"	 : fromcity['name'] , "toCity" : tocity['name'] , "rounds" : rounds}

def closeAirport( city , rounds ):
	if ROUNDCHOSEN :
		print( 'closeAirport' )	
	return {"type": "closeAirport", "city" : city['name']  , "rounds" : rounds}

def putUnderQuarantine( city , rounds ):
	if ROUNDCHOSEN :
		print( 'putUnderQuarantine' )	
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
	
	#for key in data :
	#	print( key )  # round, outcome, points, cities, events, error

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

def vaccineDeployed( pathogen , city , rounds ):
	for ev in city['events'] :
		if ev['type'] == 'vaccineDeployed' :
			if ev['pathogen']['name'] == pathogen['name'] :
				return True
	return False



@post("/")
def index():
	game = request.json
	if ( game['outcome'] != 'pending' ):	
#		print(f'round: {game["round"]}, outcome: {game["outcome"]}')
		with open( '../collected_data/leth_mob_infec_dur.csv' , 'a' ) as f :
			f.write( f'{game["round"]},{game["outcome"]}' )

#	if 'error' in game.keys() :	
#		print ( 'error : ' , game['error'] ) 

#	if 'events' in game.keys() :
#		for ev in game['events'] :
#			if ev['type'] != 'pathogenEncountered' :
#				print( 'game events : ' ,  ev )

	if ( game['outcome'] == 'pending' ) :	
		currentPoints = int( game['points'] ) 
		# not enough points 
		if ( game["points"] < 3 ):
			return endRound() 

		# processing request 
		pathogenList, amountOfPathogensList, cityList = preprocessInput( game )	
		if len( pathogenList ) != 0 :
			 
			chosenPathogen = pickPathogen( pathogenList , amountOfPathogensList )
			breakOuterLoop = False
			chosenCity = cityList[0] 
			for city in cityList :
				if 'events' in city.keys() :
					for event in city['events'] :	
						if event['type'] == 'outbreak' and event['pathogen']['name'] == chosenPathogen['name'] :
							chosenCity = city
							breakOuterLoop = True
							break
				if breakOuterLoop :
					break


				# quarantine the dangerous ones 
				if DEBUG :
					print ( 'gewählte Stadt' , chosenCity )
					print ( 'gewählter Keim' ,chosenPathogen ) 
					print ( 'ist es gefährlich',  pathogenIsDangerous( chosenPathogen ) )	
				if ( pathogenIsDangerous( chosenPathogen ) and amountOfPathogensList[chosenPathogen['name']] == 1 ) :
					if symbolValues[chosenPathogen['mobility']] > 3 :
						#if currentPoints < 40 :
						#	return endRound() 
					#	print( 'checking if quarantine already active : ' , alreadyUnderQuarantine( chosenCity ) )
						# only do a quarantine, if none is active and enough points are available 
						if (not alreadyUnderQuarantine( chosenCity )) and currentPoints >= 40 :
							return putUnderQuarantine( chosenCity , min( ( currentPoints-20)//10 , 5 )  )
						# if one is active do we have to safe points ?  ( if we had quarantine up we need to but not enough points for next quarantine )
						if alreadyUnderQuarantine( chosenCity ) and currentPoints < 40 :
							return endRound() ;
						if alreadyUnderQuarantine( chosenCity ) and currentPoints > 80 and not vaccineInDevelopment( chosenPathogen , game ) and not vaccineAvailable( chosenPathogen , game ) : 
							return developVaccine( chosenPathogen ) 
						if alreadyUnderQuarantine( chosenCity ) and currentPoints > 60 and not medicationAvailable( chosenPathogen , game ) and not medicationInDevelopment( chosenPathogen , game ) :
							return developMedication( chosenPathogen )
							# check if something else is to do
					else :	
						#if currentPoints < 30 :
						#	return endRound() 
						#print( 'checking if quarantine already active : ' , alreadyAirportClosed( chosenCity ) )
						# only do a quarantine, if none is active and enough points are available 
						if (not alreadyAirportClosed( chosenCity )) and currentPoints >= 30 :
							return closeAirport( chosenCity , min( ( currentPoints-15)//5 , 5 )  )
						# if one is active do we have to safe points ?  ( if we had quarantine up we need to but not enough points for next quarantine )
						if alreadyAirportClosed( chosenCity ) and currentPoints < 30 :
							return endRound() ;
						if alreadyAirportClosed( chosenCity ) and currentPoints > 60 and not vaccineInDevelopment( chosenPathogen , game ) and not vaccineAvailable( chosenPathogen , game ) : 
							return developVaccine( chosenPathogen ) 
						if alreadyAirportClosed( chosenCity ) and currentPoints > 50 and not medicationAvailable( chosenPathogen , game ) and not medicationInDevelopment( chosenPathogen , game ) :
							return developMedication( chosenPathogen )
							
				if ( pathogenIsDangerous( chosenPathogen ) and amountOfPathogensList[chosenPathogen['name']] > 1 ) :
					#print( 'pathogen chosen : ' , chosenPathogen , '\nis Dangerous : ' , pathogenIsDangerous( chosenPathogen) , '\npathogenList : ' , amountOfPathogensList ) 
					if symbolValues[ chosenPathogen['infectivity']]  > symbolValues[chosenPathogen['duration'] ] :
						if not medicationAvailable( chosenPathogen , game ) and not medicationInDevelopment( chosenPathogen , game ) and currentPoints > 20 :
							return developMedication( chosenPathogen ) 
						else :
							if not vaccineInDevelopment( chosenPathogen , game ) and not vaccineAvailable( chosenPathogen , game ) and currentPoints > 40 :
							 	return developVaccine( chosenPathogen ) 
						if medicationAvailable( chosenPathogen , game ) :
							if currentPoints > 0 :
								event = None
								for ev in chosenCity['events'] :
									if ev['type'] == 'outbreak' :
										event = ev
								if event != None :
									if event['prevalence'] > PREVELANECETHRESHOLD :
										return deployMedication( chosenPathogen , chosenCity ) 
								else : 
									if vaccineDeployed( chosenPathogen , chosenCity , game['round'] ) :
										return deployVaccine( chosenPathogen , chosenCity ) 
					else :								
						if not vaccineInDevelopment( chosenPathogen , game  ) and not vaccineAvailable( chosenPathogen , game ) and currentPoints > 40 :
							return developVaccine( chosenPathogen ) 
						else :
							if not medicationAvailable( chosenPathogen , game ) and not medicationInDevelopment(chosenPathogen, game ) and currentPoints > 20 :
								return developMedication( chosenPathogen )						
						if medicationAvailable( chosenPathogen , game ) :
							event = None
							for ev in chosenCity['events'] :
								if ev['type'] == 'outbreak' :
									event = ev
							if event != None : 
								if event['prevalence'] > PREVELANECETHRESHOLD :
									return deployMedication( chosenPathogen , chosenCity) 
							else : 
								if vaccineDeployed( chosenPathogen , chosenCity , game['round'] ) :	
									return deployVaccine( chosenPathogen , chosenCity ) 
							return endRound() 
		#print( 'nothing has been done -> no loop, points : ', currentPoints )
		return endRound()

BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host="0.0.0.0", port=50123, quiet=True)
