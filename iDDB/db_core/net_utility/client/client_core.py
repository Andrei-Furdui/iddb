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
        self.protocol_name = "TalkTalkProtocol - Client: "

        # if the target cannot be connected in 10 sec
        # then there is a problem
        self.socket_timeout = 10

        file_helper = DirFileHelper()
        self.yaml_file_path = file_helper.get_home_path() + "/var/iDDB/iddb.yaml"

        # maximum buffer that server can send to this client
        self.MAX_RECV_BUFFER = 8192

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

    def send_to_server(self, message):

        if len(message) <=0 or message is None:
            logger = PythonLogger("ERROR")
            logger.write_log(self.protocol_name + " - send_to_server(): Invalid message to send")
            return

        all_ips = self.get_server_ip_address()
        local_ip_addr = self.get_local_ip()
        server_result = []

        if len(all_ips[0]) > 0:
            for i in range(0, len(all_ips)):
                try:
                    self._client_socket = socket.socket()
                    self._client_socket.settimeout(self.socket_timeout)
                    # we do not want lookup in this machine
                    # so, we try to avoid sending data to the Server 
                    # which is running in this host
                    if local_ip_addr in all_ips[i]:
                        continue
                    
                    self._client_socket.connect((all_ips[i], self.PORT))
                    self._client_socket.send(message.encode())
                    data = self._client_socket.recv(self.MAX_RECV_BUFFER).decode()
                    server_result.append(data)
                    self._client_socket.close()
                    
                # socket exception (e.g. connection failed)
                except:
                    server_result.append("NOK")
        else:
            # there's a case where we can have only one iddb node so we should just send a dummy "OK"
            # response meaning that the current node can do a lookup for its IP - even it's not "very" legal
            server_result.append("OK")

        return server_result
