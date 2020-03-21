#include <stdio.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"

int create_empty_table(char *db_name, char *table_name) {
	// make sure the database name is fine
	if (!check_null_argument(table_name) || !strlen(table_name)) {
		return FALSE;
	}
	
	char *log_info = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	char *table_path = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	strcpy(table_path, home_path());
	strcat(table_path, DB_PATH);
	strcat(table_path, db_name);
	strcat(table_path, "/");
	strcat(table_path, table_name);
	
	strcpy(log_info, "An user's trying to create a table: ");
	strcat(log_info, table_name);
	strcat(log_info, ", result: ");
	
	if (check_file_exists(table_path)) {
		strcat (log_info, "FALSE - the table already exists");
		write_log(INFO, log_info);
		free (log_info);
		free (table_path);
		return FALSE;
	}
	
	FILE *fp;
	fp = fopen(table_path, "w+");
	if (fp == NULL) {
		strcat (log_info, "FALSE - the operation fails");
		write_log(INFO, log_info);
		free (log_info);
		free (table_path);
		return FALSE;
	}
	
	// TO CONTINUE WITH:
	// ADD HERE THE STRCUTURE IN THE TABLE FILE LIKE THIS:
	// table_name: xxx
	// 1_column: xxx (type)
	// 2_column: xxx (type)
	// example: 
	// 1_column: id (int)
	// 2_column: city (string)
	// content - decide this!!!	
	//fprintf(fp, "This is testing for fprintf...\n");
	
	

	fclose(fp);
	strcat (log_info, "TRUE");
	write_log(INFO, log_info);
	free (log_info);
	free (table_path);
	return TRUE;
}

void main() {
	printf("RESULT: %d\n", create_empty_table("test", "exemplu123456.txt"));
}
