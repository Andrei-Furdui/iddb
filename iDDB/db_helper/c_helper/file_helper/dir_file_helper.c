#include<string.h>
#include<dirent.h> 
//#include<stdio.h>
#include "dir_file_cons.h"


// Returns True if the specified argument contains at least 1 character,
// False otherwise
int check_null_argument (char *argument) {
	return strlen(argument) == 0 ? FALSE:TRUE;
}

// Returns True if the specified dir exists, false otherwise
int check_dir_exists (char *dir) {  
   	DIR *dr = opendir(dir); 
    	if (dr == NULL) {
    		// FIXME - add this line to logs
        	//printf("Could not open current directory" ); 
		closedir(dr); 
        	return FALSE;
    	} 
	closedir(dr); 
	return TRUE;
}

// test - TODO - remove when project is done
/*
void main() {
	//printf("%d\n", check_null_argument(""));
	printf ("HERE - %d\n", check_dir_exists("/home/doublea/ana1"));
}
*/

