# This script is used to track the background task
# which is responsible for bulk insert into remote 
# nodes

import sys
import csv
import time
import socket
import os   

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
            data = _client_socket.recv(8192).decode()
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

# let's do our job from now on...
def find_between(s, start, end):
		"""Utility function used to extract the desired substring
		from a given string. Needed, for example, to extract the table name"""
		try:
  			return (s.split(start))[1].split(end)[0]
		except IndexError:
			return None
            
if len(sys.argv) != 4:
    print ("Unexpected error occurred. Exiting...")
    sys.exit(-1)

helper_obj = DirFileHelper()
CACHE_CSV_PATH = helper_obj.get_home_path() + "var/iDDB/" + sys.argv[3]
DATABASE_NAME = sys.argv[1]
TABLE_NAME = sys.argv[2]

# we'll wait between iterations 3 sec, in this way we make
# sure that the remotes can handle this request
WAIT_BEFORE_CACHE_ITERATION = 3

def remove_cached_csv(csv_file):
    command = os.popen("rm -rf " + csv_file)

def handle_csv_file():
    bulk_string_protocol = ""
    cache_content = []
    with open(CACHE_CSV_PATH, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        # skip csv file header
        next(reader)
        for row in reader:
            temp_content = ""
            for i in range(0, len(row)):
                temp_content += row[i] + "|"
            temp_content = temp_content[:-1] + "\n"

            protocol_string = DATABASE_NAME + "!" + TABLE_NAME + "!" + temp_content[:-1]                    
            bulk_string_protocol += protocol_string + "&*()"

            # here, the MTU is limited at 1500, so let's make sure we don't send
            # a message longer than that value   
            if len(bulk_string_protocol) > 1000:
                protocol_header = "insert_tb_bulk#$"
                final_message = protocol_header + bulk_string_protocol
                cache_content.append(final_message)
                bulk_string_protocol = ""
            else:
                continue
        protocol_header = "insert_tb_bulk#$"
        final_message = protocol_header + bulk_string_protocol
        cache_content.append(final_message)

        for c in range(0, len(cache_content)):
            cache_content += "\n"
            send_to_server(cache_content[c])
            time.sleep(WAIT_BEFORE_CACHE_ITERATION/2)

    remove_cached_csv(CACHE_CSV_PATH)

handle_csv_file()

