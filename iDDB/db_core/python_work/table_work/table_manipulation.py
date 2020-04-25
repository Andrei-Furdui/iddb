import sys
import traceback
import os

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

class TableUtility:
	def __init__(self, full_table_command):

		# this should have the following format
		# example(c1-int, c2-string)
		self.full_table_command = full_table_command
		try:
			if len(self.full_table_command) == 0 :
				logger = PythonLogger("ERROR")
				logger.write_log("TableUtility class - received None full_table_command. Take action!")
		except TypeError:
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - " + traceback.format_exc() +
			"Probably the table was not specified - this is an accepted exception (only in some cases!)")

	def find_between(self, s, start, end):
		"""Utility function used to extract the desired substring
		from a given string. Needed, for example, to extract the table name"""
		try:
  			return (s.split(start))[1].split(end)[0]
		except IndexError:
			return None

	def get_table_name(self):
		"""Returns the real table name from the gived
		constructor parameter"""
		end_of_table_name = "("
		end_of_table_name_space = " "
		table_name = ""

		for character in self.full_table_command:
			if character == end_of_table_name or \
				character == end_of_table_name_space:
				break
			table_name += character
		return table_name


	def get_column_and_types(self):
		space = " "
		not_space = False
		temp_result = self.find_between(self.full_table_command, "(", ")")
		final_result = ""
		try:
			for character in temp_result:
				if character != space:
					not_space = True

				if not_space is False and character is space:
					character = ""
				final_result += character
			return final_result.rstrip()
		except TypeError:
			return ""


	def get_duplicated(self, items):
		"""Returns True if there are duplicates in this list
		or false otherwise"""
		for elem in items:
			if items.count(elem) > 1:
				return True
		return False


	def get_actual_info(self):
		TYPE_INT = "int"
		TYPE_STRING = "string"
		TYPE_BOOLEAN = "boolean"
		comma = ","

		#this should have the following format
		#c1-int, c2-string, c3-boolean

		info = str(self.get_column_and_types()).replace(" ", "")
		info += comma

		current_column = ""

		# this should contain the actual usefull info
		# e.g. columnName-columnType
		actual_list = []

		for character in info:
			if character == comma:
				current_column = current_column.replace(comma, "")
				actual_list.append(current_column)
				current_column = ""
			current_column += character

		# let's check if the columnType is the right one
		for i in range(0, len(actual_list)):
			temp_item = actual_list[i]
			if (TYPE_INT in temp_item) or (TYPE_STRING in temp_item) \
				or (TYPE_BOOLEAN in temp_item):
					pass
			else:
				logger = PythonLogger("ERROR")
				logger.write_log("Creation table failed! Invalid column type provided!")
				return None

		# TODO - to check the situation: string1 for instance - it's considered
		# passed which is not correct

		return actual_list


	def check_column_name_validity(self):
		"""Return 1 is there're columns which are duplicated,
		2 if an invalid data type is provided or 3 otherwise"""

		actual_list = self.get_actual_info()
		column_name_list = []
		temp_c = ""
		try:
			for i in range (0, len(actual_list)):
				for character in actual_list[i]:
					if character != "-":
						temp_c += character
					else:
						column_name_list.append(temp_c)
						temp_c = ""
						break
		except TypeError:
			return 2

		if self.get_duplicated(column_name_list):
			return 1

		return 3

	def get_all_tables(self, database_name, table_to_compare_to_insert):
		"""Displays all existing tables from an existing database.
		Returns 1 if an error occured, 2 otherwise and we don't do an insert
		operation - just listing tables, 3 if the table for the insert operation exists,
		4 if the table for the insert operation does not exist"""

		error = False
		try:
			if len(database_name) == 0 or database_name is None:
				error = True
		except:

				error = True

		if error:
			print ("You must specify a database first. Status (-1).\n")
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - an user's trying to \
			list all tables but without specifying an existing database")
			return 1

		# FIXME  - change this hardcoded path
		root_db_path = "/home/doublea/var/iDDB/database/"
		db_name = root_db_path + database_name
		all_table = []
		for root, dirs, files in os.walk(db_name):
    			for file in files:
        			if file.endswith('.iddb'):
						all_table.append(file)

		if len(all_table) == 0:
			print ("There are no tables yet")
		else:
			# we don't want to display also the file extension
			no_extension = 5

			if table_to_compare_to_insert is None:
				print("All existing tables from database '" + database_name + "'...")
				for i in range(0, len(all_table)):
					print all_table[i][:-no_extension]
			else:
				for i in range(0, len(all_table)):
					if all_table[i][:-no_extension] == table_to_compare_to_insert:
						return 3
				return 4

		return 2

	#TODO - when adding new properties to a table
	#add them here as well
	def describe_table(self, table_name, db_name):
		"""Describes an existing table. If the specified table
		doesn't exist, an except is raised and it is mentioned
		to the user. If an error occurs, 1 is returned, 0 otherwise"""

		# this has exaclty the same length as the constant defined
		# in the C driver (see dir_file_cons.h, #TABLE_PROPERTIES_COMMENT)
		stop_reading = "###########################################"
		count_stop_reading = 0

		# let's get current table name from the full path
		slash = 0
		temp_slash = 0
		curr_pos = 0
		position = 0

		for i in table_name:
			if i == "/":
				slash += 1
		
		for c in table_name:
			if temp_slash == slash:
				curr_pos = position
				break
			if c == "/":
				temp_slash += 1
			position += 1

		real_table_name = table_name[curr_pos:]
		final_message = "\nDatabase: " + db_name + "\nTable: " + real_table_name + " =("

		table_temp_read = table_name + ".iddb"
		try:
			content = []
			with open(table_temp_read) as f:
				for line in f:
					if count_stop_reading >= 2:
						break
					temp_line = line[:-1]
					if temp_line == stop_reading:
						count_stop_reading += 1
						continue
					content.append(temp_line.split(":"))

			temp_list = []
			for i in range(0, len(content)):
				temp_list.append(content[i][1])
	
			column_name = []
			column_type = []
			for i in range(0, len(temp_list) - 1):
				column_name.append(temp_list[i].split("-")[0])
				column_type.append(temp_list[i].split("-")[1])
			
				
			if len(column_name) != len(column_type):
				logger = PythonLogger("ERROR")
				logger.write_log("TableUtility class - " +
				"Trying to describe a table: number of columns is different the number of column types")
				print ("Unknown error has occurred. Check log file for details. Status (-1).")
				return 1
			
			temp_message = ""
			for i in range(0, len(column_name)):
				if i == len(column_name) - 1:
					temp_message += "\n" + column_name[i] + ": " + column_type[i]
				else:
					temp_message += "\n" + column_name[i] + ": " + column_type[i] + ","
			
			final_message += temp_message + ")\n"

			logger = PythonLogger("DEBUG")
			logger.write_log("Describing table: " + real_table_name + " ...")
			print final_message
			
			return 0
		except IOError:
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - " + traceback.format_exc() +
			"Trying to describe a table: the specified table name doesn't exist")
			print ("You must specify an existing table to be describer. Status (-1).")
		except:
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - " + traceback.format_exc() +
			"Trying to describe a table - unknown exception occured")
			print ("Unknown error has occurred. Check log file for details. Status (-1).")
			
		return 1

	def get_only_columns_name_from_table(self, table_name):
		"""Returns all columns from a given table - only columns name
		not their type"""

		# this has exaclty the same length as the constant defined
		# in the C driver (see dir_file_cons.h, #TABLE_PROPERTIES_COMMENT)
		stop_reading = "###########################################"
		verify_reading = 0
		table_name_in_file = "table_name"
		all_columns_from_this_table = []
		try:
			file_table = open(table_name, "r")
			for line in file_table:
				if verify_reading == 2:
					break
				if stop_reading in line:
					verify_reading += 1
					continue

				# we have 2 variants to end this process of reading from file
				# let's try both and hope the current one works
				# if not, the one with stop_reading will do the job
				if table_name_in_file in line:
					break
				usefull_line = self.find_between(line.strip(), ":", "-")
				all_columns_from_this_table.append(usefull_line)

			file_table.close()
		except IOError:
			# we should NEVER reach this because all preconditions are done
			# into the user_cli.py file
			# IF WE END UP HERE - THERE'S A PROBLEM
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - " + traceback.format_exc() +
			"Trying to insert data: the specified table name doesn't exist")
			print ("You must specify an existing table to insert data into. Status (-1).")

		return all_columns_from_this_table

	def get_only_columns_types_from_table(self, table_name, columns):
		"""Returns all columns types from a given table - only columns types
		not their name"""

		# this has exaclty the same length as the constant defined
		# in the C driver (see dir_file_cons.h, #TABLE_PROPERTIES_COMMENT)
		stop_reading = "###########################################"
		table_name_in_file = "table_name"
		verify_reading = 0
		all_columns_type_from_this_table = []

		file_table = open(table_name, "r")
		for line in file_table:
			if verify_reading == 2:
				break
			if stop_reading in line:
				verify_reading += 1
				continue

			# we have 2 variants to end this process of reading from file
			# let's try both and hope the current one works
			# if not, the one with stop_reading will do the job
			if table_name_in_file in line:
				break 

			current_line = line.strip()
			for j in range(0, len(columns)):
				if columns[j] in current_line:
					index = current_line.find("-")
					if index == -1:
						break
					else:
						temp = ""
						for i in range(index + 1, len(current_line)):
							temp += current_line[i]
						all_columns_type_from_this_table.append(temp)

		file_table.close()	
		return all_columns_type_from_this_table	


	# TODO - move this to the helper dir
	def get_longest_value (self, list_to_check):
		max_len = -1
		for ele in list_to_check: 
    			if len(ele) > max_len: 
        			max_len = len(ele) 
        			res = ele
		return res



