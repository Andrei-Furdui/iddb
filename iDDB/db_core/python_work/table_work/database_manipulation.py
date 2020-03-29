import os
import base64
import sys

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

class DatabaseUtility:
	def __init__(self, database = None):
		self.database = database
		# FIXME - very important
		# in the C driver, there's a function which returns
		# the current user path: char * home_path()
		# please use it instead of hardcoding this
		self.database_path = "/home/doublea/var/iDDB/database"
		self.current_database_file = "/home/doublea/repo_iDDB/iddb_v1/iDDB/db_core/python_work/table_work/current_database.idbb"

	def get_all_databases(self):
		"""Returns all existing databases"""

		folders = list(filter(lambda x: os.path.isdir \
				(os.path.join(self.database_path, x)), \
				os.listdir(self.database_path)))
		if len(folders) == 0:
			return "There are no databases yet"
		else:
			return folders

	def convert_to_binary(self, db_name):
		message_bytes = str(db_name).encode('ascii')
		base64_bytes = base64.b64encode(message_bytes)
		base64_db_name = base64_bytes.decode('ascii')
		return base64_db_name


	def save_current_database(self, db_name):
		# we want to overwrite the file content
		# so every time the database will change
		f = open (self.current_database_file, "w")
		f.write (self.convert_to_binary(db_name))
		f.close()

	def get_current_database(self):
		try:
			f = open(self.current_database_file, "r")
			file_content = f.read()
			f.close()
			base64_bytes = str(file_content).encode('ascii')
			message_bytes = base64.b64decode(base64_bytes)
			message = message_bytes.decode('ascii')
			return message

		except IOError:
			return None

	def remove_database_file_content(self):
		if os.path.exists(self.current_database_file):
  			os.remove(self.current_database_file)
			logger = PythonLogger("DEBUG")
			logger.write_log("Current/existing database reference was removed...")




'''
d = DatabaseUtility()
d.save_current_database("exempluqwe")
d.get_current_database()
'''
