#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"
// already included
//#include "../../../logger/c_logger/c_logger.c"

// Creates a new database (new directory)
// Returns 1 if the database was created successfully
// 0 otherwise (e.g. it already exists)
int create_database (char *db_name) {
	// make sure the database name is fine
	if (!check_null_argument(db_name) || !strlen(db_name)) {
		return FALSE;
	}

	char *log_info = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	char *database_path = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	strcpy(database_path, home_path());
	strcat(database_path, DB_PATH);
	strcat(database_path, db_name);
	
	// most likely this is the case when the FALSE value
	// is returned, so no difference between invalid parameter or
	// db exists
	if (!check_dir_exists(database_path, 1)) {
		free (log_info);
		free (database_path);
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
	free (log_info);
	free (database_path);
	return result == 0 ? TRUE:FALSE;
	//return mkdir(database_path, 0774) == 0 ? TRUE:FALSE;	
}

// Deletes a non-empty database
// Non returned type since it creates a new process
// responsable with this operation
// FIXME - doesn't work for now
int delete_non_empty_database (char *db_name) {
	execlp("rmdir -r", db_name, NULL);
}

// Deletes an EMPTY database
// Returns 1 if the database was successfully removed
// 0 otherwise (e.g. it's not empty or doesn't exist)
int delete_empty_database (char *db_name) {
	// make sure the database name is fine
	if (!check_null_argument(db_name)) {
		return FALSE;
	}
	
	char *log_info = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	char *database_path = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	strcpy(database_path, home_path());
	strcat(database_path, DB_PATH);
	strcat(database_path, db_name);

	// the database doesn't exist
	if (check_dir_exists(database_path, 1)) {
		free (log_info);
		free (database_path);
		return FALSE;
	}
	
	int result = rmdir(database_path);
	strcpy(log_info, "An user's trying to remove an empty database: ");
	strcat(log_info, db_name);
	strcat(log_info, ", result: ");
	
	if (!result) {
		strcat(log_info, "TRUE");
	}
	else {
		strcat(log_info, "FALSE (probably it's not empty)");
		// FIXME - doesn't work for now
		strcat(log_info, "- trying to go further with the removing operation...");
		delete_non_empty_database (database_path);
	}
	// TODO - make this debug
	write_log(INFO, log_info);
	free (log_info);
	free (database_path);
	return result == 0 ? TRUE:FALSE;

}
