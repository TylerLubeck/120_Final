#!/bin/bash
# This script will hit the server with a curl request until it is force quit
# (with ctrl+C). This can be used to test our rate limiting project.

COUNTER=0
while [ TRUE ]; do
	curl http://localhost:8000
	echo ""
    COUNTER=$(( COUNTER + 1 ))
	if ! (($COUNTER % 5000)); then
		echo "The server has been hit $COUNTER times."
	fi
done
