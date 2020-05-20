import sys
import time
import os
import subprocess
from threading import Thread

sys.path.insert(0, "../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../logger/python_logger/")
from python_logger import PythonLogger

sys.path.insert(0, "../db_core/net_utility/server/")
from server_core import ServerWorker

if len(sys.argv) != 2:
    print ("\nError. Usage: python setup_server_client.py <true|false>")
    print ("*********************************************************")
    print ("\ntrue - means that this Server will start as well as other network stuff related to the TalkTalk Protocol")
    print ("false - means that all network stuff will be stopped (including this Server)...")
    print ("\n*********************************************************")
    sys.exit(-1)

running_test_client = False
WAILT_CLIENT_TEST_CONNECTION = 5 # 5 seconds

def write_value():
    f = open("virtual_value.privat", "w")
    f.write(str(running_test_client))
    f.close()

arg_value = sys.argv[1]
_server = ServerWorker()
arg_value.lower
if arg_value == "true":

    print ("Check logs while starting up the server. Note:")
    print ("Sometimes, your server doesn't start because the port is already in use")
    print ("Please use the following command to kill the process which uses that port: sudo ss -tulpn | grep :9001")
    print ("\nIf you want to stop this Server as well as other networking stuff, please run: python setup_server_client.py false\n")
    running_test_client = True
    write_value()
    os.system('python fake_client_test.py &')

    _server.change_server_status(True)
    _server.start_server_preconditions()
    thread = Thread(target = _server.start_real_server, args = ( ))
    thread.start()

    # start client testing connection
    

elif arg_value == "false":
    print ("The server will stop at the next request...")
    _server.change_server_status(False)
    running_test_client = False

    # if this python layer is not able to stop the Server...
    # force stopping it by using native Linux layer
    subprocess.call("./helper_stopping_server.sh", shell=True)
    write_value()
else:
    print("Unknown parameter. Please use <true|false>!")

