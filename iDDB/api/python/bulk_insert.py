# the scope of this file
# python bulk_insert.py table_name csv_file.csv
import sys
import time
import socket
import os
from threading import Thread

sys.path.insert(0, "../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper


# SOCKET AREA
# THIS IMPLEMENTATION IS COPIED FROM THE client_core.py FILE
# WE DID THIS BECAUSE WE DO NOT NEED ALL THAT FUNCTION

def send_to_server(message):
    all_ips = get_server_ip_address()
    local_ip_addr = get_local_ip()
    server_result = []
    for i in range(0, len(all_ips)):
        try:
            _client_socket = socket.socket()

            # we do not want lookup in this machine
            # so, we try to avoid sending data to the Server 
            # which is running in this host
            if local_ip_addr in all_ips[i]:
                continue
                
            _client_socket.connect((all_ips[i], 9001))
            _client_socket.send(message.encode())
            data = _client_socket.recv(1024).decode()
            server_result.append(data)
            _client_socket.close()
            
            # socket exception (e.g. connection failed)
        except:
            server_result.append("NOK")
        
    return server_result


def get_server_ip_address():
    all_ip = []
    # get yaml file path, if doesn't exist, exit script...
    file_helper = DirFileHelper()
    yaml_file_path = file_helper.get_home_path() + "var/iDDB/iddb.yaml"
    try:
        with open(yaml_file_path) as f:
            for line in f:
                curr_line = line.strip()
                if "#" in curr_line or len(curr_line) <= 0:
                    continue

                # this is what we need
                if "ip_node=" in curr_line:
                    temp_result = find_between(curr_line, "=", " ")
                    all_ip = temp_result.split(";")
                    break
    except IOError:
        print ("It looks like iddb is not installed in this system or the yaml config file is missing. Please resolve them before executing this script")
        print ("Nothing inserted...")
        sys.exit(ERROR_CODE)
    return all_ip

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
# END OF SOCKET AREA







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

# if the CSV file contains more than 100 records than we'll
# cache them (all) and will be send later to remotes
MAXIMUM_RECORDS_BEFORE_CACHE = 100
helper_obj = DirFileHelper()
CACHE_CSV_PATH = helper_obj.get_home_path() + "var/iDDB/"
NO_OF_THREADS = -1
WAIT_BEFORE_CACHE_ITERATION = 1 # at each 1 sec we send data

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

    helper_obj = DirFileHelper()
    root_db_path = helper_obj.get_home_path() + "var/iDDB/database/"
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

def cache_csv_file(file_name):
    command = os.popen("cp " + file_name + " " + CACHE_CSV_PATH + "/" + file_name)

def read_csv_file(start_line, stop_lines, table_name):
    global CSV_FILE

    #if (start_line >= stop_lines) or (start_line <= 0 or stop_lines <= 0):
    #    print ("Something is wrong. Exiting...")
    #    sys.exit(ERROR_CODE)

    start_time = time.time()
    local_table = ""
    try:
        local_table = open(table_name, "a")
    except IOError:
        print ("Something is wrong. Exiting...")
        sys.exit(ERROR_CODE)
    
    counter = 0
    if NUMBER_OF_LINES_FROM_CSV < 5000:

        # if the CSV file contains more than 100 records, 
        # we must save its content in cache and that cache will
        # be send to remotes later 
        if NUMBER_OF_LINES_FROM_CSV > 100:
            cache_csv_file(CSV_FILE)

            if NUMBER_OF_LINES_FROM_CSV < 1000:
                NO_OF_THREADS = 5
            elif NUMBER_OF_LINES_FROM_CSV > 1000 and NUMBER_OF_LINES_FROM_CSV < 10000:
                NO_OF_THREADS = 10
            elif NUMBER_OF_LINES_FROM_CSV > 10001 and NUMBER_OF_LINES_FROM_CSV < 100000:
                NO_OF_THREADS = 20
            else:
                NO_OF_THREADS = 30

            print ("The insert operation was started. It uses " + str(NO_OF_THREADS) + " threads...")

            bulk_string_protocol = ""
            stop = 0
            # TODO, to create 10 threads HERE
            with open(CACHE_CSV_PATH + CSV_FILE , 'r') as file:
                reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                # skip csv file header
                next(reader)
                for row in reader:
                    temp_content = ""
                    for i in range(0, len(row)):
                        temp_content += row[i] + "|"
                    temp_content = temp_content[:-1] + "\n"
                    #local_table.write(temp_content)

                    protocol_string = DATABASE_NAME + "!" + TABLE_NAME + "!" + temp_content[:-1]                    
                    bulk_string_protocol += protocol_string + "&*()"

                    #protocol_string = "insert_tb#$" + DATABASE_NAME + "!" + TABLE_NAME + "!" + temp_content[:-1]                    
                    #thread1 = Thread(target = send_to_server, args = (protocol_string, ))
                    #thread1.start()
                    #send_to_server("insert_tb#$" + DATABASE_NAME + "!" + TABLE_NAME + "!" + temp_content[:-1])
                    counter += 1
                    #time.sleep(WAIT_BEFORE_CACHE_ITERATION)
                    if counter % 3 == 0:
                        protocol_header = "insert_tb#$"
                        final_message = protocol_header + bulk_string_protocol
                        thread1 = Thread(target = send_to_server, args = (final_message, ))
                        thread1.start()
                        break

                    stop += 1
                    if stop == 6:
                        break

        else:
            with open(CSV_FILE, 'r') as file:
                reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
                # skip csv file header
                next(reader)
                for row in reader:
                    temp_content = ""
                    for i in range(0, len(row)):
                        temp_content += row[i] + "|"
                    temp_content = temp_content[:-1] + "\n"
                    send_to_server("insert_tb#$" + DATABASE_NAME + "!" + TABLE_NAME + "!" + temp_content[:-1])
                    local_table.write(temp_content) 
                    counter += 1

    floating_value = time.time() - start_time
    if int(floating_value) < 1:
        #time.sleep(0.5)
        pass

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

