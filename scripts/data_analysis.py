#!/usr/bin/env python3

import os
import sys
import time
import json
import getopt
import random  # generate seeds if needed 
import subprocess as sp # spawning servers and client 


### globale variables
# paths for server generated data
base_data_path = '../collected_data/'
basedatafile='endRound.csv' # baseline data for evaluation

# path for servers
base_server_path = '../playing_servers/'  
baseserver='endRound.py' # baseline server

# client path
clientPath = '../game_binaries/ic20_linux' 
argumentOrderString = f'seed,numerRuns,rounds,outcome\n'

# pathogen List path
pathogenPath = base_data_path + 'pathogen.json'

# amount of seeds
AMOUNTSEEDS = 2000
MAXSEED =  9223372036854775807
ROUNDNUMS = 1  
BASEPORT = 50123

def read_Pathogen_List() :
	pathogenNames = []
	with open ( pathogenPath , encoding='utf-8-sig' ) as fh :
		text = json.loads ( fh.read() )
	for i in text :
		if i.count( 'Mori' ) > 0 :
			pathogenNames.append( 'Moricillus' ) 	
		else :
			pathogenNames.append( i ) 
	return pathogenNames
	
	
def analyse( fileNamesArr) :
	print( fileNamesArr )	
	data_arr = {}
	
	for path in fileNamesArr :
		cur_file_data_arr = {} 
		with open( base_data_path + path + '.csv' , 'r' ) as fh :
			line = fh.readline().split(',')	
			line = fh.readline().split(',')
			while line and line != [''] :
				cur_file_data_arr[line[0]] = [int ( line[2] ) , line[3] == 'win\n' or line[3] == 'win'  ]
				
				line = fh.readline().split(',')		
		data_arr[path + '.csv'] = cur_file_data_arr 

	data_lenth = len( data_arr[ basedatafile ] ) 
	
	eval_arr = {}
	for key in data_arr.keys() :
		win_ctr = 0
		round_ctr = 0
		more_rounds = 0
		less_rounds = 0
		diff_wins_more = 0
		diff_wins_less = 0
		wins_equal = 0
		loss_equal = 0
		for data in data_arr[key] :
			cur_data = data_arr[key][data] 
			print ( f'{key} , data : {cur_data}' } 
			if cur_data[1] :
				win_ctr += 1 
			round_ctr += cur_data[0]
			if key != basedatafile :
				cur_diff_round = data_arr[key][data][0] - data_arr[basedatafile][data][0]
				if cur_diff_round > 0 :
					more_rounds += cur_diff_round
				else:
					less_rounds -= cur_diff_round
				
				if data_arr[basedatafile][data][1] and not cur_data[1] :
					diff_wins_less += 1
				elif not data_arr[basedatafile][data][1] and cur_data[1] :
					diff_wins_more += 1
				elif not data_arr[basedatafile][data][1] and not cur_data[1] :
					loss_equal += 1
				else :
					wins_equal += 1
#		if key != basedatafile :
		print( f'{key} analysis\ngames played : {len(data_arr[key])}\n games won: {win_ctr/20}%  ,abs: {win_ctr}\n compared to endRound\n needed more rounds : {more_rounds}\nneeded less rounds {less_rounds}\ngames where won too { wins_equal},\nlost too {loss_equal}\n lost instead of won {diff_wins_less}\n won instead of lost {diff_wins_more}' )

				
		eval_arr[key] = [ win_ctr , round_ctr ]
				
	print( eval_arr ) 

def extract_seeds_from_csv( path ) :
	with open ( path , 'r' ) as fh :
		last_seed = '' 
		seed_collection = []
		line = fh.readline()
		line = fh.readline()
		while line : 
			line = line.split(',')


			if line[0] == last_seed :
				line = fh.readline() 
				continue
			last_seed = line[0]
			seed_collection.append( line[0] ) 
			
			line = fh.readline()
	return seed_collection

# function to retrieve the server files and data files 
def get_file_names() :
	serverFileBaseNames , dataFileBaseName = [] , [] 
	
	dataFileBaseNames = [ filename.split('.')[0] for filename in sp.check_output( ['ls' , base_data_path ] ).decode( 'utf-8' ).split( '\n' ) if 'csv' in filename ]
	# extract file base names for different servers
	serverFileBaseNames = [ filename.split('.')[0] for filename in sp.check_output( ['ls' , base_server_path ] ).decode( 'utf-8' ).split( '\n' ) if 'py' in filename ]

	# check if datafile already exists for a specific server 
	alreadyGeneratedDataFiles , missingDataFiles = [] , [] 
	for serverFileBaseName in serverFileBaseNames :
		if not serverFileBaseName in dataFileBaseNames :
			missingDataFiles.append( serverFileBaseName ) 
		else :
			alreadyGeneratedDataFiles.append( serverFileBaseName) 
	
	# if baseline data not in data source, 
	# all has to be generated 
	if not 'endRound' in alreadyGeneratedDataFiles :
		missingDataFiles.extend( alreadyGeneratedDataFiles ) 
	else:
		#checking if data generated is of equal length to the baseline for proper weighting
		pass #TODO optional


	return missingDataFiles , alreadyGeneratedDataFiles 

def process_ic20_output( string ) :
	pathogenNames = read_Pathogen_List() 
	pathogens = [] 
	string = str( string )
	for patho in pathogenNames :
		if string.count( patho , 0 , len(string) ) > 0 :
			pathogens.append( patho )

	outcome = '' 
	num = string.count ( 'outcome' , 0 , len(string) )
	while num > 0 : 
		string = string[string.index('outcome')+len('outcome'):]
		num -=1
	if string.count( 'loss' , 0 , len(string) ) > 0 :
		outcome = 'loss'
	else:
		outcome = 'win'
	rounds = int (string[string.index( 'round' )+len('round')+2:].split(',')[0]	)
	return rounds , outcome , pathogens

def generate_seeds ( amount ) :
	seedList = []
	cnt = 0
	while cnt < amount :
		i = random.randint( 1 , MAXSEED ) 
		while i in seedList : 
			i =  random.randint( 1 , MAXSEED ) 
		seedList.append( i ) 
		cnt += 1 
	return seedList

def generate_data( seedList , fileBaseNameList ) :
		
	serverPaths , dataFilePaths = []  , [] 
	# generate server paths and corresponding data file paths
	for serverBasename in fileBaseNameList :
		serverPaths.append( base_server_path + serverBasename + '.py' )
		dataFilePaths.append( base_data_path + serverBasename + '.csv'  )


	# start all servers with own port
	clientPaths = []
	cnt = 0
	serverProcesses  = []  
	try :
		for server in fileBaseNameList :
			curServerPath = base_server_path + server + '.py'
			port = BASEPORT + cnt
			serverProcesses.append( sp.Popen( ['python3' , curServerPath , '--port' ,  f'{port}'] ) )
			while sp.Popen.poll( serverProcesses[ cnt ] ) != None :
				print( sp.Popen.poll( serverProcesses[ cnt ] ) ) 
				continue
			cnt += 1

		# creating Data array
		data = [ [] ] * len ( fileBaseNameList ) 
		
		for path in dataFilePaths :
			with open ( path , 'w' ) as fh :
				fh.write( 'seed,count,rounds,outcome,pathogens\n' )
		# going through seeds 
		for prog , seed in enumerate ( seedList ) :
			if prog % 20 == 0 :
				print ( f'{int ( prog / len( seedList  )  *100)}% done'  )
			
			# cycle through Rounds
			for k in range(1,ROUNDNUMS + 1) :
				output = ''
				
				# cycle through severs with same seed
				for idx , fileBaseName in enumerate ( fileBaseNameList ) :
					#	if no output is generated  
					try:
						while len( output ) < 1 :
							
						# starting client for given seed 
							try:
								output = str ( sp.check_output( [ clientPath , '-s' , f'{seed}' , '-u' , f'http://0.0.0.0:{BASEPORT+idx}' ] ) )
							except sp.CalledProcessError as grepexc:
								continue
							
							# parsing values from client output
						rounds , outcome , pathogens = -1 , 'pending' , [] 
						
						rounds , outcome , pathogens = process_ic20_output ( output )
					#	print ( f'{seed},{k},{rounds},{outcome},{pathogens}' )
						try :
							with open ( dataFilePaths[ idx ] , 'a' ) as fh :
								fh.write( f'{seed},{k},{rounds},{outcome},{pathogens}\n' ) 
						except Exception as e:
							print ( f'open file exception: {e}' )
							pass
							
						data[idx].append(  [rounds , outcome , pathogens]  )
						# catch if something goes worng
					except Exception as e :
						print( 'some sprun exception : ' , e ) 
						continue
					
	except Exception as e:
		print( 'server creating error: ' ,  e ) 
		pass
	finally :
		for process in serverProcesses :
			sp.Popen.terminate( process ) 
			while sp.Popen.poll( process ) == None :
				pass

	# export data into their files 
	#	print ( 'export data to files' ) 	
	#generate_data_files( seedList , dataFilePaths] , data ) 
		
	return dataFilePaths 


def generate_data_files( seedList , pathList , data ) :
	print ( 'starting data export' )
	dataIndex = 0
	for idx , path in enumerate ( pathList ) :
		with open( path , 'w' ) as f :
			f.write( argumentOrderString ) 
			for idc , (rounds , outcome , pathogens ) in enumerate ( data[idx] ) :
				line = f'{seedList[idc]},{idc},{rounds},{outcome},'
				for idk , i in enumerate(pathogens) :
					line += f'{i}'  
					if idk != len( pathogens ) :
						line += ','
				f.write( line )
				 
	

def run() :

	# check which server files and data files
	missingDataFiles , alreadyGeneratedDataFiles = get_file_names() 
	# check if base file is there
	if baseserver[:-3] not in alreadyGeneratedDataFiles :
		missingDataFiles.extend( alreadyGeneratedDataFiles )

	seedList = [] 
	# if base file is not there generate sedes 
	if baseserver[:-3] in missingDataFiles :
		seedList = generate_seeds( AMOUNTSEEDS ) 	
 
	# else import seeds form base file 
	else :
		print( f'extracting seeds from {base_data_path + basedatafile}' ) 
		seedList = extract_seeds_from_csv( base_data_path + basedatafile ) 

	# create missing data files for server files
	if len ( missingDataFiles ) > 0 :
		datafilePaths = generate_data( seedList , missingDataFiles ) 
	
	# data analysis  
	_ , dataFiles = get_file_names() 
	analyse( dataFiles ) 

if __name__ == "__main__" :
	run()	
