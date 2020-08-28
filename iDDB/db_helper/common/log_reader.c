#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include <pwd.h>
//#include "../c_helper/file_helper/dir_file_helper.c"

const char *home_path_local() {
	char *homedir;
	if ((homedir = getenv("HOME")) == NULL) {
    		homedir = getpwuid(getuid())->pw_dir;
	}
	strcat(homedir, "/");
	return homedir;
}	

// Returns 1 if DEBUG logs should be added into the "system.log" file
// or 0 otherwise
int is_debug() {
    char *file = (char *) malloc(MIN_STREAM_LENGTH/4 * sizeof(char));
    if(file == NULL){
        return DEBUG_NO;
    }
    strcpy(file, home_path_local());
    strcat(file, "iddb_v1/iDDB/db_helper/common/log_level.txt");
    char comment_start = '#';
    char *LOCAL_DEBUG = "DEBUG";
    
    int fd = open(file, O_RDONLY);
    if (fd < 0) {
        return DEBUG_NO;
    }

    int file_size = lseek(fd, 0, SEEK_END);

    if (file_size <= 0) {
        close(fd);
        return DEBUG_NO;
    }

    lseek(fd, 0, SEEK_SET);
    
    char *file_buffer = (char *) malloc (file_size * sizeof(char));
    if(file_buffer == NULL){
        close(fd);
        return DEBUG_NO;
    }

    if (read(fd, file_buffer, file_size) <= 0) {
        free (file_buffer);
        close(fd);
        return DEBUG_NO;
    }
    
    u_short new_line = 0;
    u_short debug_iterator = 0;
    char debug_arr[DEBUG_ARRAY_LENGTH];

    while(*file_buffer != '\0') {
        if(!new_line && *file_buffer != comment_start && *file_buffer != ' '){
            debug_arr[debug_iterator++] = *file_buffer;
        }
        if (*file_buffer == comment_start) {
            new_line = 1;
        }
        if (*file_buffer == '\n'){
            new_line = 0;
        }
        
        *file_buffer++;
    }

    close(fd);
    debug_arr[debug_iterator] = '\0';
    if(strstr(debug_arr, "TRUE") != NULL) {
        return DEBUG_YES;
    }
    return DEBUG_NO;
}
