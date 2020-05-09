#!/bin/bash

echo -e "###################################"
echo -e "Setting up the iddb. Please wait...\n"
# let's create needed directories...
create_directories(){
    DB_DIR="$HOME/var/iDDB/database/"
    if [ ! -d "$DB_DIR" ]; then
        echo "Shell: Setting up directories..."
        mkdir ~/var
        mkdir ~/var/log
        mkdir ~/var/log/iDDB
        sleep 1
        mkdir ~/var/iDDB
        mkdir ~/var/iDDB/database
        echo "Shell: Done with directories"
    else
        echo "Shell: it seems the iddb is already installed..."
    fi
}

echo "Shell: compiling so files..."
cd ../out/so_files/; sh build_so.sh
echo "Shell: Done with so files..."

# get back to the current PWD
cd - >/dev/null

# do the job here
create_directories
python set_requirements.py

echo -e "###################################"