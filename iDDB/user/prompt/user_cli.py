# This file is responsible with CLI to the end user
# It contains and decodes all user actions
# It is the entry point to the db

import sys
import six

# needed for calling the C driver
from ctypes import *

sys.path.insert(0, "../../logger/python_logger/")
from python_logger import PythonLogger

sys.path.insert(0, "../../db_core/python_work/table_work/")
from database_manipulation import DatabaseUtility

# TODO TO CONTINUE WITH - to handle table commands
# database ones are done

class UserPrompt:
	def __init__(self, cli_version, dbi_version):
		self.cli_version = cli_version
		self.dbi_version = dbi_version
		self.running_prompt = True
    
	def prompt_message(self):
		# add info into system.log file
		logger = PythonLogger("INFO")
		logger.write_log("An user is trying to connect to the database (CLI - entry point)...")

		init_message = "Welcome to iDDB, version " + self.dbi_version
		cli_version = "CLI Version: " + self.cli_version
		temp_solution = "\nTemporary solution: each command must be specified using ONLY one line, this will be improved in the future\n"
		final_welcome_message = init_message + "\n" + cli_version#the invalid command is + temp_solution
		return final_welcome_message

    	# this is the main method - entry point on the app (cli)
    	def create_prompt(self):
		################################
		# FIXME - improve this
		# it's not working in all cases
		# the command to be specified using multiple lines
		##################################
		full_command = ""
		while self.running_prompt:
		    	user_value = raw_input('iDDB> ')
			full_command += " " + str(user_value)
			if self.end_of_command(user_value):
				self.execute_command(full_command)
				#print ("To be executed... " + str(full_command))
				full_command = ""
		    	if user_value == "end" or user_value == "bye" or user_value == "exit":
		        	print ("\n\nBye, have a nice day!")
		        	self.running_prompt = False
				logger = PythonLogger("INFO")
				logger.write_log("The user ends current CLI session...")
	
	# An user command must have on the last position(s):
	# 1. ;
	#    OR
	# 2. \g
	def end_of_command(self, command):
		"""Returns True is the user wants to execute its command,
		 False otherwise"""
		
		if ";" in command or "\g" in command:
			return True
		return False
			
	def execute_command(self, user_command):
		obj = AvailableCommands("available_commands.txt")
		command = []
		command = obj.parse_commands()

		DATABASE = "DATABASE"
		TABLE = "TABLE"

		# let's check the command's purpose
		# e.g. if it's a database command
		# or a table one
		database_command = False
		table_command = False
	
		# remove this character ; from the user command
		actual_user_command = user_command[:-1]
	
		# TODO - remove in the future...
		#print ("Current user command: " + actual_user_command)

		for current_command in command:
			if current_command.lower() in actual_user_command.lower():
				if DATABASE.lower() in user_command.lower():
					database_command = True
					break
				elif TABLE.lower() in user_command.lower():
					table_command = True
					break
		
		# we'll know if the command is correct or not (first requirment)
		if database_command is False and table_command is False:
			print ("Invalid command. Status (-1).\n")
			logger = PythonLogger("ERROR")
			logger.write_log("An user tried to execute a command but\
				 fails, the invalid command is: " + actual_user_command + " ...")
			# stop the parsing operation since no requirment
			# is satisfied
			return
		
		# this variable represents the current database - the one which
		# the user wants to do his job
		current_database = None
		
		# in this moment we now for sure what's the purpose of
		# every command
		
		# let's handle database commands here
		db_utility = DatabaseUtility()	
		# TODO - create a python dictionary for all commands below
		if database_command:
			# 1. display all existing DBs
			if "LS".lower() in actual_user_command.lower():
				# let's parse the list received
				temp_list = db_utility.get_all_databases()
				if isinstance(temp_list, six.string_types):
					print (temp_list)
				else:
					print ("All existing databases...")
					for iterator in temp_list:
						print("Database name: " + iterator)
					print ("\n")
			
			so_file = '../../out/so_files/database_manipulation.so'
			c_db = CDLL(so_file)

			# 2. create a new database (an empty one)
			if "MKDIR".lower() in actual_user_command.lower():
				db_name = self.find_between(actual_user_command, \
								"database ", ";")
				
				# even if the C driver doesn't allow an empty db name
				# make sure it doesn't reach that point if so
				if db_name is None:
					print ("Invalid command. Status (-1).\n")
					return
				c_return = c_db.create_database(db_name)
				if c_return != 1:
					print ("Database creation has failed, check log file for details. Status (-1).")
					return
			
			# 3. remove a database (no matter if it's empty or not)
			if "RMDIR".lower() in actual_user_command.lower():
				db_name = self.find_between(actual_user_command, \
								"database ", ";")
				
				# even if the C driver doesn't allow an empty db name
				# make sure it doesn't reach that point if so
				if db_name is None:
					print ("Invalid command. Status (-1).\n")
					return
				c_return = c_db.delete_empty_database(db_name)
				if c_return != 1:
					print ("Database deletion has failed, check log file for details. Status (-1).")
					return
			
			if "USE".lower() in actual_user_command.lower():
				db_name = self.find_between(actual_user_command, \
								"database ", ";")
				# even if the C driver doesn't allow an empty db name
				# make sure it doesn't reach that point if so
				if db_name is None:
					print ("Invalid command. Status (-1).\n")
					return

				temp_list = db_utility.get_all_databases()
				if isinstance(temp_list, six.string_types):
					logger = PythonLogger("ERROR")
					logger.write_log("An user tried to use a database, but there are no any. Exiting!")
					print (temp_list)
					print ("You must create a database first. Status (-1).")
					return
				else:
					for iterator in temp_list:
						if iterator == db_name:
							current_database = db_name
							break
						# make sure no database is set-up when the 
						# specified one doesn't exist
						current_database = None
					if current_database is None:
						logger = PythonLogger("ERROR")
						logger.write_log("The user wants to use the database: " + str(db_name) + " but it doesn't exist...")
						print ("The specified database does not exist. Status (-1).")
						return
					logger = PythonLogger("DEBUG")
					logger.write_log("Current database is: " + str(current_database) + " ...")
	
		# let's handle table commands here
		if table_command:
			utility_command = self.find_between(actual_user_command, \
								"table ", ";")
			print ("Table command " + utility_command)
			
		print ("Command successfully executed. Status (0).\n")
	
	def find_between(self, s, start, end):
		"""Utility function used to extract the desired substring
		from a given string. Needed, for example, to extract the table name"""
		try:
  			return (s.split(start))[1].split(end)[0]
		except IndexError:
			return None
		


class AvailableCommands:
	def __init__(self, commands_file_path):
		self.commands_file_path = commands_file_path
		self.comment = "#"
		self.space = " "

	def obtain_commands_from_file(self):
		try:
			with open(self.commands_file_path) as file:
				all_list = [l.strip() for l in file]
				return all_list
		except IOError:
			logger = PythonLogger("ERROR")
			logger.write_log("Invalid file with accepted commands\
				 provided - '" + self.commands_file_path + "'. The CLI database is closing now")
			print ("Unexpected error occured. See log file for details")
			sys.exit(-1)

	# Returns all commands accepted by the database driver
	# as they are specified into the given file
	# usually that file is located in the same location as this 
	# python file and its name is: available_commands.txt

	# TODO - what happens if the *.txt file doesn't exist???
	# let's fix that in future commits
	def parse_commands(self):
		initial_commands_list = self.obtain_commands_from_file()
		all_commands = []
		for line in initial_commands_list:
			if self.comment == "#" in line or self.space == line[0]:
				continue
			all_commands.append(line)
		return all_commands
		
			
        
if __name__ == "__main__":
    	k = UserPrompt("1.0", "0.1")
    	prompt_info = k.prompt_message()
    	print (prompt_info)
    	k.create_prompt()
	
