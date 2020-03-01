import os

class DatabaseUtility:
	def __init__(self, database = None):
		self.database = database
		self.database_path = "/home/doublea/var/iDDB/database"

	def get_all_databases(self):
		folders = list(filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d)))
		print (folders)

d = DatabaseUtility()
d.get_all_databases()


		
