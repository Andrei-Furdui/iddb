#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
//#include <stdio.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"
// already included
//#include "../../../logger/c_logger/c_logger.c"

// Creates a new database (new directory)
// Returns 1 if the database was created successfully
// 0 otherwise (e.g. it already exists)
int create_database (char *db_name) {
	// make sure the database name is fine
	if (!check_null_argument(db_name)) {
		return FALSE;
	}

	char *log_info = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	// FIXME - deallocate memory for this variables
	char *database_path = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	strcpy(database_path, home_path());
	strcat(database_path, DB_PATH);
	strcat(database_path, db_name);
	printf("TEST %s\n", database_path);
	
	// most likely this is the case when the FALSE value
	// is returned, so no difference between invalid parameter or
	// db exists
	if (!check_dir_exists(database_path, 1)) {
		return FALSE;
	}

	int result = mkdir(database_path, 0776);
	
	strcpy(log_info, "An user's trying to create a new database: ");
	strcat(log_info, db_name);
	strcat(log_info, ", result: ");
	
	if (!result) {
		strcat(log_info, "TRUE");
	}
	else {
		strcat(log_info, "FALSE");
	}

	// TODO - make this debug
	write_log(INFO, log_info);

	return result == 0 ? TRUE:FALSE;
	//return mkdir(database_path, 0774) == 0 ? TRUE:FALSE;	
}

/*
void main() {
	printf("HERE- %d\n", create_database("test3"));
}
*/
