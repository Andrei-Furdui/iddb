#!/bin/bash

# sometimes, python layer is unable to stop this Server, so, 
# we force stopping it by killing its process...
# this script must be called from the python layer

killPid=`ss -tulpn | grep :9001 | tr -s " " ":" | cut -d ":" -f 10 | cut -d "," -f2 | cut -d "=" -f2`
kill -9 $killPid 2> /dev/null
