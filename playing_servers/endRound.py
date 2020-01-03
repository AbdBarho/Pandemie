#!/usr/bin/env python3

import os
from bottle import post, request, run, BaseRequest

outputFile = f'../collected_data/endRound.csv' 

@post("/")
def index():
	game = request.json
	if ( game['outcome'] != 'pending' ) :
		if os.path.exists( outputFile ) :
			with open( outputFile , 'a' ) as f :
				line = f'{game["round"]},{game["outcome"]},\n'
				print( line ) 
				f.write( line ) 
		else: 
			with open( outputFile , 'w' ) as f :
				line = f'{game["round"]},{game["outcome"]},\n'
				f.write( line ) 

	action = {"type": "endRound"}
	return action


BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host="0.0.0.0", port=50123, quiet=True)
