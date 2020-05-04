# the scope of this file
# python bulk_insert.py table_name csv_file.csv
import sys

NO_OF_PARAMETERS = 4
ERROR_CODE = -1
CSV_FILE = None
FILE_FORMAT = ".csv"
IS_OK_FORMAT = False
MAXIMUM_NUMBER_OF_COLUMNS = 50
TABLE_NAME = None
DATABASE_NAME = None

if len(sys.argv) != NO_OF_PARAMETERS:
    print("Invalid number of parameters.\nUsage: python bulk_insert.py database_name table_name csv_file.csv")
    sys.exit(ERROR_CODE)

CSV_FILE = sys.argv[3]
if CSV_FILE.endswith(FILE_FORMAT):
    IS_OK_FORMAT = True

if IS_OK_FORMAT is False:
    print ("Invalid data file provide - " + str(CSV_FILE) + "...")
    sys.exit(ERROR_CODE)

DATABASE_NAME = sys.argv[1]
TABLE_NAME = sys.argv[2]

# we should never reach here
if DATABASE_NAME is None or TABLE_NAME is None:
    print ("Invalid parameter provided!")
    sys.exit(ERROR_CODE)

import threading
import csv
import os.path
from os import path

column_names = []
column_types = []

def find_between(s, start, end):
		"""Utility function used to extract the desired substring
		from a given string. Needed, for example, to extract the table name"""
		try:
  			return (s.split(start))[1].split(end)[0]
		except IndexError:
			return None

def get_columns_from_specified_table():
    global DATABASE_NAME
    global TABLE_NAME
    global ERROR_CODE
    global column_names
    global column_types

    root_db_path = "/home/doublea/var/iDDB/database/"
    db_name = root_db_path + DATABASE_NAME + "/"
    table_name = db_name + TABLE_NAME + ".iddb"
    if path.exists(table_name) is False:
        print("Table provided does not exist!")
        sys.exit(ERROR_CODE)
    
    columns = []
    stop_reading = "###########################################"
    stop_reading1 = "table_name:"
    counter = 0
    f_table = open(table_name, "r")
    l_table = f_table.readlines()
    for line in l_table:
        temp_line = line.strip()
        if stop_reading1 in temp_line:
            break
        if counter == 2:
            break
        if temp_line == stop_reading:
            counter += 1
            continue
        
        columns.append(temp_line)
        
    for i in range(0, len(columns)):
        column_names.append(find_between(columns[i], ":", "-"))
        column_types.append(find_between(columns[i], "-", " "))



try:
    rows = []
    table_columns_from_csv = []
    table_content = []
    number_of_rows = 0
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            table_columns_from_csv.append(row)
            break
        for rows in reader:
            table_content.append(rows)
            number_of_rows += 1

    dont_math_error = "The file '" + CSV_FILE + "' does not contain a valid format - its columns don't match with the ones from the specified table. Exiting..."
    
    # let's populate needed data
    get_columns_from_specified_table()
    if len(table_columns_from_csv[0]) != len(column_names):
        print (dont_math_error)
        sys.exit(ERROR_CODE)
        
    for index in range(0, MAXIMUM_NUMBER_OF_COLUMNS):
        try:
            # let's check columns match
            if table_columns_from_csv[0][index].lower() != column_names[index]:
                print (dont_math_error)
                sys.exit(ERROR_CODE)
        except IndexError:
            # that's it, we close this loop by raising an exception...
            break

    print("Validating the schema. Please wait...")

    for i in range(0, number_of_rows):
        for j in range(0, len(column_names)):
            # VALIDATE THE DATA
            print("HERE: " + table_content[i][j])
        

except IOError:
    print ("No such file or directory: '" + CSV_FILE + "'")
