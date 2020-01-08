#!/bin/python3
import os
import argparse
import subprocess
import random

game_seed_path='../collected_data/endRound.csv'

filepath='../collected_data/leth_mob_infec_dur_quarantine_airportclose.csv'


if __name__ == "__main__" :
		with open( game_seed_path , 'r' ) as inF :  
			line = inF.readline()
			cnt = 0 
			old_seed = ''
			while line:
				line = inF.readline() 
				if cnt == 10 :
					break 
				if line[0] == old_seed  :
					continue	
				cnt += 1
				if cnt % 10 == 1:
					print( f'{cnt} of 2000 done , {cnt/100}\%\n')
				
				i = line.split(',')[0]
				k = line.split(',')[1]
				if os.path.exists(filepath) and cnt != 1  :
					with open( filepath , 'a' ) as f :
						f.write( f'{i},{k},') 
				else :
					with open( filepath , 'w' ) as f :
						f.write( f'seed,numerRuns,rounds,outcome\n' )
						f.write( f'{i},{k},' ) 
				client = subprocess.run( args=['../game_binaries/ic20_linux','-s',f'{i}','-o','/dev/null'] ) 
				old_seed = line[0] 
