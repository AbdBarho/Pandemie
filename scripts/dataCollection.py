#!/bin/python3
import os
import argparse
import subprocess
import random

filepath='../collected_data/endRound.csv'


if __name__ == "__main__" :
		for _ in range(0,2000 ) :
			i = random.randint(1,9223372036854775807)
			for k in range(1,6):
				if os.path.exists(filepath) :
					with open( filepath , 'a' ) as f :
						f.write( f'{i},{k},') 
				else :
					with open( filepath , 'w' ) as f :
						f.write( f'seed,numerRuns,rounds,outcome\n' )
						f.write( f'{i},{k},' ) 
				client = subprocess.run( args=['../game_binaries/ic20_linux','-s',f'{i}','-o','/dev/null'] ) 

