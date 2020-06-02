import socket
import sys
import time
from ctypes import *
from threading import Thread

sys.path.insert(0, "../../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

# doesn't work - FIXME
"""
sys.path.insert(0, "../../db_core/python_work/table_work")
from table_manipulation import TableUtility
"""

from helping_server import HelpingServer

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
        self.protocol_name = "TalkTalkProtocol - Server: "

        # maximum buffer that client can send to this server
        self.MAX_RECV_BUFFER = 1024

        """
        TalkTalkProtocol has the following header:
        <identifier>|[identifier|identifier|...]#$body

        Here are the main identifiers:
        1. create_db => create new database
        2. remove_db => remove existing database
        3. create_tb => create new table
        4. remove_tb => remove existing table

        5. insert_tb => insert data into table
        (in this case, the body must have the following format:
        db_name!table_name!data)
        6. truncate_tb => remove all data from table

        For all identifiers above, the Server will create a new thread (if possible, if not,
        all work will be done in the Server thread) which is
        responsable with executing specific task AND the Server MUST reply to the 
        client following messages:
        1. OK => all operations were successfully executed
        2. NOK => at least one operation failed

        If an invalid message (header and/or body) is received, NOK must be sent back

        The body can contain multiple "parts", these parts must be separated by "!", 
        otherwise, NOK Must be sent back
        """
        self.OK_MSG = "OK"
        self.NOK_MSG = "NOK"
        
    def change_server_status(self, running_status):
        self.running = running_status
        logger = PythonLogger("INFO")
        logger.write_log(self.protocol_name + "Changing the server status to " + str(self.running))
    
    def get_server_status(self):
        return self.running

    def start_server_preconditions(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                
                # we know that the client sent an action
                # so we should handle it here, depending on the
                # header message
                data = c.recv(self.MAX_RECV_BUFFER).decode()
                if len(data) > 0 :
                    identifier = data.split("#$")[0]
                    body = data.split("#$")[1]
                    
                    isTalkTalkProtocolMessageOK = False 
                    try:
                        unknown_part = data.split("#$")[2]
                    except IndexError:
                        isTalkTalkProtocolMessageOK = True
                    
                    if isTalkTalkProtocolMessageOK is False:
                        c.send(self.NOK_MSG)
                    else:

                        # get a reference to the C driver
                        so_file = '../out/so_files/database_manipulation.so'
                        c_db = CDLL(so_file)
                        if "create_db" in identifier:
                            c_return = c_db.create_database(str(body))
                            if c_return != 1:
                                c.send(self.NOK_MSG)
                            else:
                                c.send(self.OK_MSG) 
                        elif "remove_db" in identifier:
                            c_return = c_db.delete_empty_database(str(body))
                            if c_return != 1:
                                c.send(self.NOK_MSG)
                            else:
                                c.send(self.OK_MSG)
                        elif "create_tb" in identifier:
                            body_parts = body.split("!")
                            isBodyPartOk = False
                            try:
                                aux_part = body_parts[3]
                            except IndexError:
                                isBodyPartOk = True

                            if isBodyPartOk:
                                # we must override this because
                                # there's another section from the C driver
                                # which handles table operations
                                so_file = '../out/so_files/table_manipulation.so'
                                c_db = CDLL(so_file)
                                c_return = c_db.create_empty_table(str(body_parts[0]), str(body_parts[1]), str(body_parts[2]))
                                if c_return != 1:
                                   c.send(self.NOK_MSG)
                                else:
                                    c.send(self.OK_MSG)
                            else:
                                c.send(self.NOK_MSG)
                            #print ("We should create new table")
                        elif "remove_tb" in identifier:
                            body_parts = body.split("!")
                            isBodyPartOk = False
                            try:
                                aux_part = body_parts[2]
                            except IndexError:
                                isBodyPartOk = True

                            if isBodyPartOk:
                                # we must override this because
                                # there's another section from the C driver
                                # which handles table operations
                                so_file = '../out/so_files/table_manipulation.so'
                                c_db = CDLL(so_file)
                                c_return = c_db.remove_table(str(body_parts[0]), str(body_parts[1]))
                                if c_return != 1:
                                   c.send(self.NOK_MSG)
                                else:
                                    c.send(self.OK_MSG)
                            else:
                                c.send(self.NOK_MSG)
                        elif "insert_tb" in identifier:
                            # we don't need to validate input here because
                            # we did this in the user_cli.py phase (if we insert
                            # data via CLI)
                            message_to_be_inserted = body.split("&*()")

                            for i in range(0, len(message_to_be_inserted)):
                                body_parts = message_to_be_inserted[i].split("!")
                                db_name = body_parts[0]
                                table_name = body_parts[1]
                                if db_name is None or table_name is None:
                                    c.send(self.NOK_MSG)
                                else:
                                    content = body_parts[2]
                                    try:
                                        aux_content = body_parts[3]
                                        c.send(self.NOK_MSG)
                                    except IndexError:
                                        # we should go here, otherwise something is really wrong
                                        # and send NOK to the client
                                        so_file = '../out/so_files/table_manipulation.so'
                                        c_db = CDLL(so_file)
                                        c_return = c_db.do_insert_db(str(db_name), 
                                                            str(table_name), str(content))

                                        if c_return != 1:
                                            c.send(self.NOK_MSG)
                                        else:
                                            c.send(self.OK_MSG)
                            
                        elif "truncate_tb" in identifier:
                            # FIXME - when enabling the failing import
                            # enable also the following line (this is the correct way
                            # to truncate a table, now we only use a hacky way)
                            #tb_utility = TableUtility(None)

                            tb_utility = HelpingServer()
                            helper_obj = DirFileHelper()
                            table_path = helper_obj.get_home_path() + body
                            if tb_utility.delete_from_table(table_path) == 0:
                                c.send(self.NOK_MSG)
                            else:
                                c.send(self.OK_MSG)
                        else:
                            c.send(self.NOK_MSG)
                
                logger = PythonLogger("DEBUG")
                logger.write_log(self.protocol_name + "Got connection from " + str(addr))
                c.close()
                
        else:
            logger = PythonLogger("ERROR")
            logger.write_log(self.protocol_name + "Communication error...")

"""
a = ServerWorker()
a.change_server_status(True)
a.start_server_preconditions()
thread = Thread(target=a.start_real_server, args=())
thread.start()
"""
#time.sleep(10)
#a.change_server_status(False)
#print("HERE2:" + str(a.get_server_status()))
#time.sleep(10)
