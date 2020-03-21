import os

class DatabaseUtility:
	def __init__(self, database = None):
		self.database = database
		# FIXME
		# in the C driver, there's a function which returns
		# the current user path: char * home_path()
		# please use it instead of hardcoding this
		self.database_path = "/home/doublea/var/iDDB/database"

	def get_all_databases(self):
		"""Returns all existing databases"""

		folders = list(filter(lambda x: os.path.isdir \
				(os.path.join(self.database_path, x)), \
				os.listdir(self.database_path)))
		if len(folders) == 0:
			return "There are no databases yet"
		else:
			return folders
	
	
	
	
		

d = DatabaseUtility()
d.get_all_databases()


		
