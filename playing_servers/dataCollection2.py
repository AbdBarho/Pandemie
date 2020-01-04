#!/bin/python3
import os
import argparse
import subprocess
import random

game_seed_path='../collected_data/endRound.csv'

filepath='../collected_data/leth_mob_infec_dur.csv'


if __name__ == "__main__" :
		with open( game_seed_path , 'r' ) as inF :  
			line = inF.readline()
			cnt = 0 
			while line:
				line = inF.readline() 
				cnt += 1
				if cnt % 10 == 0:
					print( f'{cnt} of 10000 done , {cnt/100}\%\n')
				
				i = line.split(',')[0]
				k = line.split(',')[1]
				print(cnt , ' ' ,  line , ' ' , i , ' ' , k ) 
				if os.path.exists(filepath) :
					with open( filepath , 'a' ) as f :
						f.write( f'{i},{k},') 
				else :
					with open( filepath , 'w' ) as f :
						f.write( f'seed,numerRuns,rounds,outcome\n' )
						f.write( f'{i},{k},' ) 
				client = subprocess.run( args=['../game_binaries/ic20_linux','-s',f'{i}','-o','/dev/null'] ) 

