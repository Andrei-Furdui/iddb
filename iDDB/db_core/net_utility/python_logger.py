import datetime
import time
import sys

sys.path.insert(0, "../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

class PythonLogger:
	def __init__(self, log_level, started_db = False):
		self.log_level = log_level
		
		if started_db == False:
			self.system_file_log = "system.log"
		else:
			self.system_file_log = "iDDB_init.log"

		# TODO - modify this path when available
		self.helper_obj = DirFileHelper()
		self.system_log_path = self.helper_obj.get_home_path() + "var/log/iDDB/"	
		self.log_file = self.system_log_path + self.system_file_log	
		
		"""
		Log levels accepted:
		1. INFO
		2. DEBUG
		3. WARN (WARNING)
		4. ERROR
		They must be specified for each info that will be added/appended
		into the log file (system.log)
		If an invalid log level will be specified the the INFO one will
		be considered being by default
		"""
		if self.log_level != "INFO" and self.log_level != "WARN" and \
			 self.log_level != "DEBUG" and self.log_level != "ERROR":
				self.log_level = "INFO"
			
	
	def write_log(self, info, mode="a"):
		"""
		This is the main method that will be used in this class - its aim is to
		write the actual info into the system.log file (the default one) or into 
		the iDDB_init.log file
		
		:info - actual information to be added into the specific file
		:mode - this can have the following values:
			1) a - append info
			2) w - truncate the file before adding new info in it (usually
			this will be used when thr database process starts)
	
		Returns: 
		"""
		
		if mode != "a" and mode != "w":
			mode = "a"
		if info is None or len(info) == 0:
			info = "Internal error occurred..."
		initial_info = self.get_current_timestamp() + "[" + self.log_level + "]" + ": "
		log_file = open(self.log_file, mode)
		usefull_info = initial_info + info + "\n"
		log_file.write(usefull_info)
		log_file.close()
	
	def get_current_timestamp(self):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		return timestamp
