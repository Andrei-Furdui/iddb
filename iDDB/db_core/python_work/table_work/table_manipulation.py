import sys

sys.path.insert(0, "../../../logger/python_logger/")
from python_logger import PythonLogger

class TableUtility:
	def __init__(self, full_table_command):

		# this should have the following format
		# example(c1-int, c2-string)
		self.full_table_command = full_table_command
		if len(self.full_table_command) == 0 :
			logger = PythonLogger("ERROR")
			logger.write_log("TableUtility class - received None full_table_command. Take action!")

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


'''
t = TableUtility("example(c1-int, c2-string, c9-int")
print (t.get_table_name())
#print (t.get_column_and_types())
print (t.check_column_name_validity())
'''