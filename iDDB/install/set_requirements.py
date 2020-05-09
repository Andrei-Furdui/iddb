import sys

sys.path.insert(0, "../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

PYTHON_LOGGER_INIT = "Python: "
# get $HOME path
print (PYTHON_LOGGER_INIT + "Getting the $HOME path...")
dir_file_helper_object = DirFileHelper()
home_path = dir_file_helper_object.get_home_path()

