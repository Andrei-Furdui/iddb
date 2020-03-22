#include <stdio.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"

int create_empty_table(char *db_name, char *table_name, char *table_properties) {
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
	
	// ADD HERE THE STRCUTURE IN THE TABLE FILE LIKE THIS:
	// table_name: xxx
	// 1_column: xxx (type)
	// 2_column: xxx (type)
	// example: 
	// 1_column: id (int)
	// 2_column: city (string)
	// content - decide this!!!	
	
	
	// the following represent the table structure stored
	// in the specific file

	char *table_name_f = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/2);
	strcpy(table_name_f, TABLE_NAME);
	


	// the table_properties parameter should have the following form:
	//table_name,column1_name-type, column2_name-type etc
	char *temp_table_name = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/2);
	char *temp_column_name = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/2);
	short counter = 0;
	
	// if this variable has value 0:
	// it means we're on the table name
	// 1 - column 1, 2 - column 2 etc
	short identifier = 0;
	while(*table_properties != '\0') {
		if(*table_properties == ',') {
			identifier++;
			temp_column_name[strlen(temp_column_name)] = '\0';
		
			// remove first character which is comma
			// TODO - why comma arrives here???
			temp_column_name++;
				
			// make sure the column_name is not empty
			if (strlen(temp_column_name)) {
				// TO CONTINUE WITH
				// get type from column and then write to file
				// the usefull info
				printf("Column %s\n", temp_column_name);
			}
			temp_column_name = (char *) calloc (TABLE_MANIPULATION_LENGTH/2, sizeof(char));
			counter = 0;
		}
		// treat table name
		if(!identifier) {
			temp_table_name[counter++] = *table_properties;	
		}	
		// treat columns here
		else {
			temp_column_name[counter++] = *table_properties;
		}
		table_properties++;
	}
	temp_table_name[strlen(temp_table_name)] = '\0';

	printf("HERE: %s\n", temp_table_name);





	fprintf(fp, "This is testing for fprintf...\n");
	

	fclose(fp);
	strcat (log_info, "TRUE");
	write_log(INFO, log_info);
	free (log_info);
	free (table_path);
	free (table_name_f);
	free (temp_table_name);
	free (temp_column_name);
	return TRUE;
}

void main() {
	printf("RESULT: %d\n", create_empty_table("test", "exemplu123.bat", "test,column1_name-type,column2_name-type,column3_name-type,"));
}
