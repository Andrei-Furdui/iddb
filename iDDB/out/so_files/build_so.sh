#!/bin/bash

#This file is used to track all C work from python
#In order to achieve this, every time a new C file is added
#it must be specified this as well

echo "Compiling... please wait!"

cc -fPIC -shared -o database_manipulation.so ../../db_core/c_work/table_work/database_manipulation.c #2>/dev/null
sleep 1
cc -fPIC -shared -o table_manipulation.so ../../db_core/c_work/table_work/table_manipulation.c #2>/dev/null
sleep 1
cc -fPIC -shared -o help_command.so ../../db_helper/c_helper/user_helper/help_command.c #2>/dev/null
sleep 1
cc -fPIC -shared -o log_reader.so ../../db_helper/common/log_reader.c #2>/dev/null

echo "Compilation finished!"
