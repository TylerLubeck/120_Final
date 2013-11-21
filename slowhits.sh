#!/bin/bash
# This script will hit the server with a curl request until it is force quit
# (with ctrl+C). It will only perform one curl request per 3 seconds, to 
# demonstrate how this project works with slower server hits.

COUNTER=0
while [ TRUE ]; do
	#curl http://localhost:8000
	let COUNTER=COUNTER+1
	echo "The server has been hit $COUNTER times."
	sleep 3
done