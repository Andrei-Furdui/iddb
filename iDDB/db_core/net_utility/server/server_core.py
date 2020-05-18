import socket
import sys
import time
from threading import Thread

sys.path.insert(0, "../../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

class ServerWorker:
    
    def __init__(self):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # do not change those information
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.PORT = 9001

        # we must be sure everyone can reach this out
        # se we'll bind everyong here
        self.local_address = ''

        # initial, server is not running
        self.running = None

        # maximum clients 
        # FIXME - to be read from the config file
        self.number_of_clients = 3
    
        # global class object for this socket
        self._server_socket = None

        # this DB is using the TalkTalkProtocol
        # so each net log message should contain this tag
        self.protocol_name = "TalkTalkProtocol: "

    def change_server_status(self, running_status):
        self.running = running_status
        logger = PythonLogger("INFO")
        logger.write_log(self.protocol_name + "Changing the server status to " + str(self.running))
    
    def get_server_status(self):
        return self.running

    def start_server_preconditions(self):
        try:
            self._server_socket = socket.socket()
            self._server_socket.bind(('', self.PORT))
            self._server_socket.listen(self.number_of_clients)
            return True
        except:
            logger = PythonLogger("ERROR")
            logger.write_log(self.protocol_name + "socket.error: [Errno 98] Address already in use")
            return False

    def stop_real_server(self):
        self._server_socket.shutdown(socket.SHUT_RDWR)
        self._server_socket.close()
        logger = PythonLogger("INFO")
        logger.write_log(self.protocol_name + "Closed current socket...")

    def start_real_server(self):

        if self.start_server_preconditions():
            logger = PythonLogger("INFO")
            logger.write_log(self.protocol_name + "Starting the server...")
            while True:
                c, addr = self._server_socket.accept()
                if self.get_server_status() is False:
                    self.stop_real_server()
                    break
                logger = PythonLogger("DEBUG")
                logger.write_log(self.protocol_name + "Got connection from " + str(addr))
                c.send("Hello " + str(self.get_server_status()))
                c.close()
                
        else:
            logger = PythonLogger("ERROR")
            logger.write_log(self.protocol_name + "Communication error...")

"""
a = ServerWorker()
a.change_server_status(True)
a.start_server_preconditions()
print("HERE1:" + str(a.get_server_status()))
thread = Thread(target = a.start_real_server, args = ( ))
thread.start()
time.sleep(10)
a.change_server_status(False)
print("HERE2:" + str(a.get_server_status()))
time.sleep(10)
"""