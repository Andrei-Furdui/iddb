#include <conio.h> 
#include <dir.h> 
#include <process.h> 
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"

int create_database (char *db_name) {
	// make sure the database name is fine
	if (!check_null_argument(dir)) {
		return FALSE;
	}
	return mkdir(db_name);
}
