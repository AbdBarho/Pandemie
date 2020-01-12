#!/usr/bin/env python3

import os
import sys
import getopt
from bottle import post, request, run, BaseRequest


@post("/")
def index():
	action = {"type": "endRound"}
	return action

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
