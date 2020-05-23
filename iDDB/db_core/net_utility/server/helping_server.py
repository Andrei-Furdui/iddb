import sys

sys.path.insert(0, "../../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

class HelpingServer:

	def __init__(self):
		pass

	# Method copied from TableUtility class - this is a hacky way to obtain
	# truncate table, it must be changed in the future
	def delete_from_table(self, table_name):
		"""Executes the command: delete from table
		Removes all content from the specified table
		Returns 1 if everything is ok, 0 otherwise

		TODO - this should be a C specific implementation...
		FIXME = this violates the arhitecture of this db
		"""

		if table_name is None:
			return 0
		
		try:
			start_point = "###########################################"
			column_index = "column #"
			table_name1 = "table_name:"
			with open(table_name, "r+") as f:
    			    d = f.readlines()
    			    f.seek(0)
    			    for i in d:
        			if (start_point in i) or (column_index in i) or (table_name1 in i):
            			    f.write(i)
    			    f.truncate()
			logger = PythonLogger("INFO")
			logger.write_log("An user's trying to remove all data from " + str(table_name) + " result: TRUE")
			return 1
		except IOError:
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - An user's trying to remove all data from the table " + str(table_name) + " but it doesn't exist...")
			print ("You must specify an existing table to remove data from. Status (-1).")
			return 0
