#!/usr/bin/env python3 

import time
import argparse 	
import subprocess as sp

base_data_path = '../collected_data/'

basefile='endRound.csv' 
file1 = 'leth_mob_infec_dur.csv'
file2 = 'leth_mob_infec_dur_quarantine_only.csv'

base_server_path = './playing_servers/'  

baseserver='endRound.py'
server1 = 'leth_mob_infec_dur_quarantine_only.py'
server2 = 'leth_mob_infec_dur.py'

fileList = [basefile] #,file1,file2]

serverlist= [baseserver] #,server1,server2]

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

def process_ic20_output( string ) :
		string = str( string )
		outcome = [] 
		num = string.count ( 'outcome' , 0 , len(string)  )
		while num > 0 : 
			string = string[string.index('outcome')+len('outcome'):]
			num -=1
		string = string[:20] 
		
		if string.count( 'loss' , 0 , len(string) ) > 0 :
			outcome = False
		else:
			outcome = True	

		rounds = int (string[string.index( 'round' )+len('round')+2:].split(',')[0])  

		return outcome , rounds 


def get_basefile_seeds() :
	seeds = [] 
	for fh in fileList : 
		seeds.append( extract_seeds_from_csv( fh ) ) 
		print (f'{list( map( len , seeds )) }' ) 
		
def run() :
	for idx , path in enumerate ( serverlist ) :
		cur_process = sp.Popen( ['python3' , path ] )
		output = ''
		try :
			while len( output ) < 1  :
				try:
					while sp.Popen.poll( cur_process ) != None :
						pass 
					output = sp.check_output( ['../game_binaries/ic20_linux'] )
				except Exception as e:
					pass
		except Exception as e:
			pass 
		finally:	
			sp.Popen.terminate( cur_process )
		outcome , rounds =	process_ic20( output ) 
		print( outcome , ' ' , rounds ) 
		while sp.Popen.poll( cur_process ) == None :
			time.sleep( .01 ) 

def is_file_there() :
	
	## extract file base names for already existing csv files
	dataFileBaseNames = [ filename.split('.')[0] for filename in sp.check_output( ['ls' , base_data_path ] ).decode( 'utf-8' ).split( '\n' ) if 'csv' in filename ]
	# extract file base names for different servers
	serverFileBaseNames = [ filename.split('.')[0] for filename in sp.check_output( ['ls' , base_server_path ] ).decode( 'utf-8' ).split( '\n' ) if 'py' in filename ]

	# check if datafile already exists for a specific server 
	alreadyGeneratedDataFiles , missingDataFiles = [] , [] 
	for it in serveFileBaseNames :
		if not it in dataFileBaseNames :
			missingDataFiles.append( it ) 
		else :
			alreadyGeneratedDataFiles.append( it ) 
	
	## if baseline data not in data source, all has to be generated
	# else just 
	if not 'endRound' in alreadyGeneratedDataFiles :
		missingDataFiles.extend( alreadyGeneratedDataFiles ) 
	else:
		
		#checking if data generated is of equal length to the baseline for proper weighting
		pass #TODO optional

	return missingDataFiles 

def do_Seeds_already_exist() :
	


if __name__ == "__main__" :
	get_data() 

