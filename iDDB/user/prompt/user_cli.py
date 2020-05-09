#!/usr/bin/python
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

sys.path.insert(0, "../../db_core/python_work/table_work/")
from table_manipulation import TableUtility

sys.path.insert(0, "../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper


class UserPrompt:
	def __init__(self, cli_version, dbi_version):
		self.cli_version = cli_version
		self.dbi_version = dbi_version
		self.running_prompt = True

	def prompt_message(self):
		# add info into system.log file
		try:
			logger = PythonLogger("INFO")
			logger.write_log("An user is trying to connect to the database (CLI - entry point)...")
		except IOError:
			print ("Something's wrong with requirements. Exiting...")
			sys.exit(-1)

		# make sure no old database exists
		db_utility = DatabaseUtility()
		db_utility.remove_database_file_content()

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
				# treat help command - special cases
			if str(user_value) == "help;": # the only way to achieve the
				# help section - so use this harcoded word in this case
				so_file = '../../out/so_files/help_command.so'
				c_db = CDLL(so_file)
				c_db.help_command()
				continue

			full_command += " " + str(user_value)
			if self.end_of_command(user_value):
				self.execute_command(full_command)
				#print ("To be executed... " + str(full_command))
				full_command = ""
		    	if user_value == "end" or user_value == "bye" or user_value == "exit":
		        	print ("\n\nBye, have a nice day!")
		        	self.running_prompt = False
				db_utility = DatabaseUtility()
				db_utility.remove_database_file_content()
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

		# this is a special case - for select command
		select_command = False

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
		
		if "select" in user_command.lower():
			select_command = True

		if select_command is False:
			# we'll know if the command is correct or not (first requirment)
			if database_command is False and table_command is False:
				print ("Invalid command. Status (-1).\n")
				logger = PythonLogger("ERROR")
				logger.write_log("An user tried to execute a command but fails, the invalid command is: " + actual_user_command + " ...")
				# stop the parsing operation since no requirment
				# is satisfied
				return
		else:
			# continue with the SELECT command
			pass 

		

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

					db_utility.save_current_database(str(current_database))
					logger = PythonLogger("DEBUG")
					logger.write_log("Current database is: " + str(current_database) + " ...")

		# let's handle table commands here

		if table_command or select_command:
			utility_command = self.find_between(actual_user_command, \
								"table ", ";")

			# call the C driver table manipulation!
			so_file = '../../out/so_files/table_manipulation.so'
			c_db = CDLL(so_file)

			# call the tableUtility driver - a python one
			tb_utility = TableUtility(utility_command)

			if "CREATE".lower() in actual_user_command.lower():

				column_validity_result = tb_utility.check_column_name_validity()
				if column_validity_result == 1:
					logger = PythonLogger("ERROR")
					logger.write_log("An user's trying to create a new table but fails because he used multiple columns with the same name...")
					print ("Table creation has failed, check log file for details. Status (-1). ")
					return;

				elif column_validity_result == 2:
					logger = PythonLogger("ERROR")
					logger.write_log("An user's trying to create a new table but fails because he used an invalid data type...")
					print ("Table creation has failed, check log file for details. Status (-1). ")
					return

				elif column_validity_result == 3:
					current_database = db_utility.get_current_database()
					if current_database is None:
						print ("You must use a database first. Status (-1).")
						return

					c_return = c_db.create_empty_table(str(current_database), str(tb_utility.get_table_name()), str(tb_utility.get_column_and_types() + ","))
					if c_return != 1:
						print ("Table creation has failed, check log file for details. Status (-1). ")
						return

			if "LS TABLE".lower() in actual_user_command.lower():

				# if a specific table is given here - error
				# since we're displaying all tables, not a single one
				# here
				if utility_command is not None:
					print ("Invalid command. Status (-1).\n")
					return

				if tb_utility.get_all_tables(db_utility.get_current_database(), None) == 1:
					return

			if "DELETE TABLE".lower() in actual_user_command.lower():

				if utility_command is None:
					print ("You must specify a table to be removed. Status (-1).")
					return

				c_return = c_db.remove_table(utility_command, str(db_utility.get_current_database()))
				if c_return != 1:
					print ("Table deletion has failed, check log file for details. Status (-1).")
					return

			if "DESC TABLE".lower() in actual_user_command.lower():

				if utility_command is None:
					print ("You must specify a table to be described. Status (-1).")
					return

				if db_utility.get_current_database() is None:
					print ("You must specify a database which contains the table to be describer. Status (-1).")
					return

				python_helper = DirFileHelper()
				db_name = python_helper.get_home_path() + "var/iDDB/database/" + db_utility.get_current_database() + "/"
				table_display = db_name + utility_command
				result = tb_utility.describe_table(table_display, db_utility.get_current_database())
				if result != 0:
					return

			if "INSERT INTO".lower() in actual_user_command.lower():
				logger = PythonLogger("DEBUG")
				logger.write_log("Preparing preconditions for the insert operation...")

				if db_utility.get_current_database() is None:
					print ("You must specify a database which contains the table to insert data into. Status (-1).")
					return

				if utility_command is None:
					print ("You must specify a table to insert data into. Status (-1).")
					return

				python_helper = DirFileHelper()
				db_name = python_helper.get_home_path() + "var/iDDB/database/" + db_utility.get_current_database() + "/"
				
				# let's manipulate usefull info

				###############################
				#1 - table name
				table_name = ""
				for c in utility_command:
					if c == "(":
						break
					table_name += c
				table_name = table_name.replace(" ", "")

				if len(table_name) < 1:
					print ("You must specify a table to insert data into. Status (-1).")
					return

				# let's check if the table exists
				if tb_utility.get_all_tables(db_utility.get_current_database(), table_name) == 4:
					print ("Specified table doesn't exist. Status (-1).")
					return
				# end of precondition 1
				################################

				###################################
				#2 - get columns from that table and check they exist

				# we should have 2 open_brackets and 2 closed
				open_brackets = 0
				closed_brackest = 0
				for c in utility_command:
					if c == "(":
						open_brackets += 1
					elif c == ")":
						closed_brackest += 1
				
				if open_brackets != 2 and closed_brackest != 2:
					logger = PythonLogger("ERROR")
					logger.write_log("An user's trying to insert data into '" + table_name + 
					"' but fails because didn't specify the required number of open/closed brackets...")
					print ("Insert operation has failed due to a syntax error. Check log file for details. Status (-1).")
					return

				columns_from_user = []
				first_index = utility_command.find("(")
				last_index = utility_command.find(")")

				valid_columns = utility_command[first_index + 1:last_index]
				valid_columns += ","
				aux = ""

				for c in valid_columns:
					if c == " ":
						continue
					if c != ",":
						aux += c
					else:
						columns_from_user.append(aux)
						aux = ""

				db_name = python_helper.get_home_path() + "var/iDDB/database/" + db_utility.get_current_database() + "/"
				full_table_path = db_name + table_name + ".iddb"

				# this contains all columns from the current table - it's a list
				all_columns_from_table = tb_utility.get_only_columns_name_from_table(full_table_path)
				
				# test if the number of given columns is greater than the number of existing
				# columns - if so, error
				if len(columns_from_user) > len(all_columns_from_table):
					print("Insert operation has failed since more than needed columns were specified. Status (-1).")
					return
				
				# save what columns are used to insert data, the others are filled up with null value (probably)
				# feature AI: THE USER CAN INSERT SOME COLUMNS WHICH DON'T EXIST, THEY ARE NOT TAKEN INTO 
				# CONSIDERATION AT ALL  
				final_columns = []
				for i in range(0, len(columns_from_user)):
					temp = columns_from_user[i]
					for j in range(0, len(all_columns_from_table)):
						if temp == all_columns_from_table[j]:
							final_columns.append(temp)
							break

				all_types_from_tabel = tb_utility.get_only_columns_types_from_table(full_table_path, final_columns)
				
				if len(final_columns) == 0 or len(all_types_from_tabel) == 0:
					print ("Insert operation has failed since you must specify at least one valid column for inserting value. Status (-1).")
					return

				# end of precondition 2
				################################

				###################################
				#3 - manipulate values section
				go_next = False
				if "VALUES".lower() in utility_command:
					go_next = True

				if go_next is False:
					logger = PythonLogger("ERROR")
					logger.write_log("An user's trying to data into '" + table_name + 
					"' but fails because the VALUES keyword is missing...")
					print ("Insert operation has failed due to a syntax error. Check log file for details. Status (-1).")
					return
				
				counter = 0
				index_second_open_bracket = 0
				index_second_closed_bracket = 0
				for c in utility_command:
					if counter == 2:
						break
					if c == "(":
						counter += 1
					index_second_open_bracket += 1
				
				counter = 0
				for c in utility_command:
					if counter == 2:
						break
					if c == ")":
						counter += 1
					index_second_closed_bracket += 1
				
				values = []
				usefull_value = utility_command[index_second_open_bracket:index_second_closed_bracket - 1]
				usefull_value += ","
				aux = ""
				for c in usefull_value:
					#if c == " ":
					#	continue
					if c != ",":
						aux += c
					else:
						values.append(aux)
						aux = ""
					
				if len(final_columns) != len(values):
					print ("You must specify the same number of columns and values to be inserted or you a syntax error. Status (-1).")
					return
				
				# final columns specified by the user: final_columns
				# final values specified by the user: values (they correspund with final_columns)

				# contains all columns which will have the default values (e.g. all non-specified 
				# columns by the user)
				non_inserted_columns = []
				for i in range(0, len(all_columns_from_table)):
					exists = False
					temp_column = all_columns_from_table[i]
					for j in range(0, len(final_columns)):
						if temp_column == final_columns[j]:
							exists = True
							break
					if exists is False:
						non_inserted_columns.append(temp_column)
				
				# let's check what will have the default value or not
				error_message = "Insert operation has failed because one/more column(s) contains an invalid value. Status (-1)."
				final_string = ""
				for i in range(0, len(all_columns_from_table)):
					temp_column = all_columns_from_table[i]
					inserted = False
					for j in range(0, len(final_columns)):
						if temp_column == final_columns[j]:

							# let's check columns type
							# valid_type = type (values[j]) is  all_types_from_tabel[j]
							if all_types_from_tabel[j] == "int":
								try:
									temp = int(values[j])
								except ValueError:
									print("INTEGER VALIDATION: " + error_message)
									return
							elif all_types_from_tabel[j] == "boolean":
								aux_boolean_value = values[j].replace(" ", "")
								if aux_boolean_value != "true" and aux_boolean_value != "false":
									print ("BOOLEAN VALIDATION: " + error_message)
									return

							# for this case, we can consider everything as being a string
							# TODO - is that correct?
							elif all_types_from_tabel[j] == "string":
								pass

							final_string += values[j] + "|"
							inserted = True
							break
					if inserted is False:
						final_string += "EMPTY" + "|"

				if len(final_string) < 1:
					logger = PythonLogger("ERROR")
					logger.write_log("The string to be inserted is NULL - we don't know the reason...")
					print ("Unexpected error occurred. Check log file for details. Status (-1).")
					return
				
				# end of precondition 3
				################################
				logger = PythonLogger("DEBUG")
				logger.write_log("Done with preconditions for the insert operation...")
				
				# now, since we worked out all preconditions, it's time to pass this string
				# to the C driver

				if db_utility.get_current_database() is None:
					print ("You must specify a database before inserting data. Status (-1).")
					return
				
				final_content = final_string[:-1]
				final_content = final_content.replace("| ", "|")
				final_content = final_content.replace(" |", "|")

				# check if there're any empty space between/after separator |
				# TODO - enable this at some point...
				#for i in range(0, len(final_content)):
				#	if final_content[i] == "|" and i < len(final_content) and i > 0:
				#		if final_content[i + 1] == " " or final_content[i - 1]:
				#			print ("Insert operation has failed since multiple spaces were specified between values. Status (-1).")
				#			return

				c_return = c_db.do_insert_db(str(db_utility.get_current_database()), 
													 	table_name, final_content)

				if c_return != 1:
					print ("Insert operation has failed. Check log file for details. Status (-1).")
					return

			if "SELECT".lower() in actual_user_command.lower():
				if db_utility.get_current_database() is None:
					print ("You must specify a database which contains the table to select data from. Status (-1).")
					return
				
				if "from" not in actual_user_command.lower():
					logger = PythonLogger("ERROR")
					logger.write_log("An user's trying to do a select but fails because the FROM keyword is missing...")
					print("Select operation has failed due to a syntax error. Check log file for details. Status (-1).")
					return

				# unfortunately we treat each hardcoded case one by one
				# in this way, the complexity is increased but for now
				# let's do that in this way...
				#1 TREAT CASE SELECT * FROM ..
				if "select * from " in actual_user_command.lower():
					s_asterix_table = self.find_between(actual_user_command, "from ", " ")

					if tb_utility.get_all_tables(db_utility.get_current_database(), s_asterix_table) == 4:
						print ("Specified table doesn't exist. Status (-1).")
						return

					db_name = db_utility.get_current_database()
					c_return = c_db.select_all_from_table(str(db_name), str(s_asterix_table), 1)
					if c_return != 1:
						print ("Select operation has failed. Check log file for details. Status (-1).")
						return
				
				#2 TREAT CASE SELECT COUNT(*) FROM ...
				elif "select count(*) from " in actual_user_command.lower():
					s_asterix_table = self.find_between(actual_user_command, "from ", " ")
					if tb_utility.get_all_tables(db_utility.get_current_database(), s_asterix_table) == 4:
						print ("Specified table doesn't exist. Status (-1).")
						return
					db_name = db_utility.get_current_database()
					c_return = c_db.select_all_from_table(str(db_name), str(s_asterix_table), 2)
					if c_return != 1:
						print ("Select operation has failed. Check log file for details. Status (-1).")
						return
				
				#3 TREAT CASE SELECT ... FROM ... WHERE...
				#3.1 select column from table
				elif "select " in actual_user_command and "from " in actual_user_command:

					columns_select = self.find_between(actual_user_command, "select ", " from")

					if (columns_select is None) or "from" in columns_select:
						print ("You must provide at least one column to be selected. Status (-1).")
						return
					
					table_name1 = self.find_between(actual_user_command, "from ", " ")
					if table_name1 is None:
						table_name1 = self.find_between(actual_user_command, "from ", ";")

					columns_select += " "
					list_columns = []
					temp = ""
					for c in columns_select:
						if c != " ":
							temp += c
						else:
							list_columns.append(temp)
							temp = ""
					
					

			if "TRUNCATE ".lower() in actual_user_command.lower():
				if db_utility.get_current_database() is None:
					print ("You must specify a database which contains the table to remove from. Status (-1).")
					return

				removing_table = self.find_between(actual_user_command, "table ", " ")

				if tb_utility.get_all_tables(db_utility.get_current_database(), removing_table) == 4:
						print ("Specified table doesn't exist. Status (-1).")
						return

				helper_obj = DirFileHelper()
				table_path = helper_obj.get_home_path() + "var/iDDB/database/" + db_utility.get_current_database()
				table_path += "/" + removing_table + ".iddb"
				if tb_utility.delete_from_table(table_path) == 0:
					print ("Removing operation has failed. Check log file for details. Status(-1).")
					return
							
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
