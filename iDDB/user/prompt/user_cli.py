# This file is responsible with CLI to the end user
# It contains and decodes all user actions
# It is the entry point to the db

import sys
sys.path.insert(0, "../../logger/python_logger/")
from python_logger import PythonLogger

class UserPrompt:
	def __init__(self, cli_version, dbi_version):
		self.cli_version = cli_version
		self.dbi_version = dbi_version
		self.running_prompt = True
    
	def prompt_message(self):
		# add info into system.log file
		logger = PythonLogger("INFO")
		logger.write_log("User tries to connect to the database...")

		init_message = "Welcome to iDDB, version " + self.dbi_version
		cli_version = "CLI Version: " + self.cli_version
		temp_solution = "\nTemporary solution: each command must be specified using ONLY one line, this will be improved in the future\n"
		final_welcome_message = init_message + "\n" + cli_version + temp_solution
		return final_welcome_message

    	# this is the main method - entry point on the app (cli)
    	def create_prompt(self):
		while self.running_prompt:
		    	user_value = raw_input('iDDB> ')
			if self.end_of_command(user_value):
				print ("To be executed...")
		    	if user_value == "end" or user_value == "bye" or user_value == "exit":
		        	print ("\n\nBye, have a nice day!")
		        	self.running_prompt = False
		    	else:
		        	print (user_value)
	
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


class AvailableCommands:
	def __init__(self, commands_file_path):
		self.commands_file_path = commands_file_path
		self.comment = "#"
		self.space = " "

	def obtain_commands_from_file(self):
		with open(self.commands_file_path) as file:
			all_list = [l.strip() for l in file]
			return all_list

	# Returns all commands accepted by the database driver
	# as they are specified into the given file
	# usually that file is located in the same location as this 
	# python file and its name is: available_commands.txt
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
	
	#test = AvailableCommands("available_commands.txt")
	#p = []
	#p = test.parse_commands()
	#for i in p:
	#	print (i)



