/**
###
The purpose of this file is to create a mechanism that will be used to handle
the location of all databases/tables (each db/table will be located in a specific
dir/file).
###
**/
#include <stdio.h>
#include <dirent.h> 
#include <stdlib.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"

  
// Returns all files (only files) from a given directory or an error message
// if the directory does not eixts or its name if not ok
char * get_all_files_from_dir(char *dir) {
	// make sure the dir name is ok and it exists
	if (!check_null_argument(dir)) {
		return FAILURE_STR;
	}
	if (!check_dir_exists(dir)) {
		return FAILURE_STR;
	}
	
	short only_files = 0;
	char *all_tables_from_dir = (char*) malloc 
					(sizeof (char *) * MAX_STREAM_LENGTH);
	strcpy(all_tables_from_dir, "");

	// try to open the mentioned dir
	DIR *dr = opendir(dir); 
	struct dirent *de;
	while ((de = readdir(dr)) != NULL) {
		if(!strcmp(de->d_name, "..") && only_files == 0) {
			only_files = 1;
			continue;
		}
		
		if (only_files) {
			char * temp = (char *) malloc 
					(sizeof(char *) * MIN_STREAM_LENGTH);
			strcpy (temp, de->d_name);
			strcat (temp, ", ");
			strcat(all_tables_from_dir, temp);
			free (temp);
		}
	}

	// close the dir
	closedir(dr);
	all_tables_from_dir[strlen(all_tables_from_dir) - 2] = 0;
	printf("HERE:  %s\n", all_tables_from_dir);
	return all_tables_from_dir;
}



// TODO - remove this, only for test
int main(void) 
{ 
	char *result;
	result = get_all_files_from_dir("/home/doublea/ana");
    	printf("%s\n", result);
	free(result);
    	return 0; 
} 

