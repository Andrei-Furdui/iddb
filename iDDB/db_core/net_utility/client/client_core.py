import socket
import sys
import time
from threading import Thread

sys.path.insert(0, "../../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger



# this class is implemented in the same way as the server_core.py one
class ClientWorker:

    def __init__(self):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # do not change those information
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.PORT = 9001

        self._client_socket = None

        # this DB is using the TalkTalkProtocol
        # so each net log message should contain this tag
        self.protocol_name = "TalkTalkProtocol: "

        # if the target cannot be connected in 5 sec
        # then there is a problem
        self.socket_timeout = 5

        file_helper = DirFileHelper()
        self.yaml_file_path = file_helper.get_home_path() + "/var/iDDB/iddb.yaml"

    def get_server_ip_address(self):
        all_ip = []
        with open(self.yaml_file_path) as f:
            for line in f:
                curr_line = line.strip()
                if "#" in curr_line or len(curr_line) <= 0:
                    continue

                # this is what we need
                if "ip_node=" in curr_line:
                    temp_result = self.find_between(curr_line, "=", " ")
                    all_ip = temp_result.split(";")
                    break
        return all_ip
                
    
    def find_between(self, s, start, end):
		"""Utility function used to extract the desired substring
		from a given string. Needed, for example, to extract the table name"""
		try:
  			return (s.split(start))[1].split(end)[0]
		except IndexError:
			return None

    def get_local_ip(self):
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

    def test_connection(self):
        """
        Method used to test the connection to server
        This should be used as entry point for each message or
        should be used to check if the other node (server(s))
        is still alive, if not, we have a big issue here
        """

        all_ips = self.get_server_ip_address()
        for i in range(0, len(all_ips)):
            try:
                # dummy socket, not the original one
                # because it can be in-use at that time so
                # it's dangerous it
                dummy_socket = socket.socket()
                dummy_socket.settimeout(self.socket_timeout)
                dummy_socket.connect((all_ips[i], self.PORT))
                dummy_socket.close()
                logger = PythonLogger("DEBUG")
                ip_addr = self.get_local_ip()
                logger.write_log(self.protocol_name + " - test_connection(): This node: " + ip_addr + " successfully connected to " + all_ips[i])
            except:
                logger = PythonLogger("ERROR")
                ip_addr = self.get_local_ip()
                logger.write_log(self.protocol_name + " - test_connection(): This node: " + ip_addr + " is unable to connect to " + all_ips[i])

    def test(self):
        dummy_socket = socket.socket()
        dummy_socket.connect(("192.168.1.7", self.PORT))
        dummy_socket.close()

c = ClientWorker()
c.get_server_ip_address()
print (c.test_connection())