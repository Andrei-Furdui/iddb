# the scope of this file
# python bulk_insert.py table_name csv_file.csv
import sys
import time
from threading import Thread

NO_OF_PARAMETERS = 4
ERROR_CODE = -1
CSV_FILE = None
FILE_FORMAT = ".csv"
IS_OK_FORMAT = False
MAXIMUM_NUMBER_OF_COLUMNS = 50
TABLE_NAME = None
DATABASE_NAME = None
NUMBER_OF_LINES_FROM_CSV = -1
TABLE_FULL_PATH = ""

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
    global TABLE_FULL_PATH
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

    TABLE_FULL_PATH = table_name
    f_table.close()

def read_csv_file(start_line, stop_lines, table_name):
    global CSV_FILE

    #if (start_line >= stop_lines) or (start_line <= 0 or stop_lines <= 0):
    #    print ("Something is wrong. Exiting...")
    #    sys.exit(ERROR_CODE)

    start_time = time.time()
    local_table = ""
    try:
        local_table = open(table_name,"a")
    except IOError:
        print ("Something is wrong. Exiting...")
        sys.exit(ERROR_CODE)
    
    counter = 0
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        # skip csv file header
        next(reader)
        for row in reader:
            temp_content = ""
            for i in range(0, len(row)):
                temp_content += row[i] + "|"
            temp_content = temp_content[:-1] + "\n"
            local_table.write(temp_content)
            counter += 1

    floating_value = time.time() - start_time
    if int(floating_value) < 1:
        time.sleep(0.5)

    execution_time = "{:.5f}".format(time.time() - start_time)
    print("Inserted " + str(counter) + " values in " + str(execution_time) + " sec...")


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

    # get number of lines from file
    # that's it, we repeat ourself...
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        NUMBER_OF_LINES_FROM_CSV = sum(1 for row in reader)

    dont_math_error = "The file '" + CSV_FILE + "' does not contain a valid format - its columns don't match with the ones from the specified table. Exiting..."    
    # let's populate needed data
    get_columns_from_specified_table()
    try:
        if len(table_columns_from_csv[0]) != len(column_names):
            print (dont_math_error)
            sys.exit(ERROR_CODE)
    except:
        print ("Something is wrong. Exiting...")
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
    validate_data_type_error_message = "Some columns don't contain valid data based on table's columns. Exiting..."
    for i in range(0, number_of_rows):
        for j in range(0, len(column_names)):
            if column_types[j] == "int":
                try:
                    aux_int = int(table_content[i][j])
                except ValueError:
                    print (validate_data_type_error_message)
                    sys.exit(ERROR_CODE)
            elif column_types[j] == "boolean":
                if table_content[i][j].lower() != "true" and table_content[i][j].lower() != "false":
                    print (validate_data_type_error_message)
                    sys.exit(ERROR_CODE)
            # string case - we will consider everything as being string
            else:
                pass

    # we're done with data validation
    print("Validating the schema successfully. Starting the bulk insert...")

    
    # do insert here
    thread = Thread(target = read_csv_file, args = (1, 2, TABLE_FULL_PATH))
    thread.start()

except IOError:
    print ("No such file or directory: '" + CSV_FILE + "'")
