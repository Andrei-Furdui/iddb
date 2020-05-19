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

sleep 1
echo "Shell: compiling and firing up C files..."
# compile and execute the file which auto-gerenates the yaml
gcc -o ../out/so_files/generate_yaml_file ../out/so_files/generate_yaml_file.c
sleep 1
../out/so_files/generate_yaml_file
sleep 1
echo "Shell: done with C files..."
sleep 1

echo -e "###################################"
