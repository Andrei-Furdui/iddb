# Python file to test API implementation
# This is the first UT, next ones must be specified in order
# UT1.py, UT2.py etc...
 
import unittest 
import sys

sys.path.insert(0, "../../db_helper/python_helper/file_helper/")
from dir_file_helper import DirFileHelper

sys.path.insert(0, "../../logger/python_logger/")
from python_logger import PythonLogger

sys.path.insert(0, "../../db_core/python_work/table_work/")
from database_manipulation import DatabaseUtility

sys.path.insert(0, "../../db_core/python_work/table_work/")
from table_manipulation import TableUtility

class TestPythonHandlers(unittest.TestCase): 
      
    def setUp(self): 
        pass
  
    def test_home_path(self):
    # Tests if the Python API used for getting user's HOME
    # variable value (home path) works (e.g. it shouldn't return
    # an empty value)
        dir_helper = DirFileHelper()
        self.assertIsNotNone(dir_helper.get_home_path())
    
    def test_all_dbs(self):
    # Tests if the Python API used for getting all existing DBs
    # works as expected:
    # 1. if there's an existing database, the following message
    # should be obtained: There are no databases yet
    # 2. if there are databases, we should get a list of them
        db_helper = DatabaseUtility()

        db_exist = False
        all_dbs = db_helper.get_all_databases()

        for i in range(0, len(all_dbs)):
            if all_dbs[i] != None:
                db_exist = True
                break
        
        # if there aren't dbs, let's check the message we expect to have
        if db_exist is False:
            self.assertEqual(db_helper.get_all_databases(), "There are no databases yet")
    

    def test_convert_extract_binary(self):
    # Tests if the Python API for converting db name into binary and back
    # (from binary to string) works
    # we pass a dummy string, convert it into binary format and then
    # convert it again into string format and compare the result
    # with the first string
        db_helper = DatabaseUtility()
        dummy_db_name = "example_iddb"
        binary_db_name = db_helper.convert_to_binary(dummy_db_name)
        self.assertEqual(db_helper.get_current_database, dummy_db_name)
    
    def test_get_between(self):
    # Test the Python API find_between - used to get a substring from a string
    # This is very usefull for instance, to get the table name from the current database
    # We'll pass the string db_name!table|name, and we want to get the string table

        table_helper = TableUtility(None)
        dummy_str = table_helper.find_between("db_name!table|name", "!", "|")
        self.assertEqual(dummy_str, "table")
    

  
if __name__ == '__main__': 
    unittest.main() 