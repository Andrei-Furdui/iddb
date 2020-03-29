#!/bin/bash

#This file is used to track all C work from python
#In order to achieve this, every time a new C file is added
#it must be specified this as well

echo "Compiling... please wait!"

cc -fPIC -shared -o database_manipulation.so ../../db_core/c_work/table_work/database_manipulation.c #2>/dev/null
sleep 1
cc -fPIC -shared -o table_manipulation.so ../../db_core/c_work/table_work/table_manipulation.c #2>/dev/null

echo "Compilation finished!"
