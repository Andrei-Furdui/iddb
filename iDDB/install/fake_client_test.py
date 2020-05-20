import sys
import time
from threading import Thread

sys.path.insert(0, "../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../logger/python_logger/")
from python_logger import PythonLogger

sys.path.insert(0, "../db_core/net_utility/client/")
from client_core import ClientWorker

TIMEOUT = 30 # 30 seconds

def read_value():
	f = None
	try:
		f = open("virtual_value.privat", "r")
		return f.read().strip()
	except:
		print ("Fatal error occured - segmentation fault!")
		sys.exit(-1)
	finally:
		if f != None:
			f.close()


def run_test_client():
	while True:
		if "false" in read_value().lower():
			break
		_client_socket = ClientWorker()
		_client_socket.test_connection()
		time.sleep(TIMEOUT)

thread = Thread(target = run_test_client, args = ( ))

# very dangerous to make this thread as Daemon
#thread.setDaemon(True)

thread.start()

