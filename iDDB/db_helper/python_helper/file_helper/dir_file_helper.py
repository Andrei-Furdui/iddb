import os
import sys

# TODO - enable logging...
#sys.path.insert(0, "../../../logger/python_logger/")
#from python_logger import PythonLogger


class DirFileHelper:

    def __init__(self):
        self.home_var = "HOME"

    def get_home_path(self):
        """Returns the $HOME variable from the OS"""

        if self.home_var in os.environ:
            return os.environ['HOME'] + "/"
        else:
            print("You're trying to install iddb into unsupported OS. Exiting...")
            sys.exit(-1)
            #logger = PythonLogger("ERROR")
    	    #logger.write_log("Trying to list the $HOME variable but doesn't exist...")
