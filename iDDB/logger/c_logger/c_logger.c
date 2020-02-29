#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include "../../db_helper/c_helper/file_helper/dir_file_cons.h"

// See ../python_logger/python_logger.py for more info
void write_log(char *log_level, char *info) {
	int fd;

	int hours;
	char *c_hours = (char *) malloc (sizeof (char*) * DATE_LENGTH);

	int minutes;
	char *c_minutes = (char *) malloc (sizeof (char*) * DATE_LENGTH);

	int seconds;
	char *c_seconds = (char *) malloc (sizeof (char*) * DATE_LENGTH);
	
	int day;
	char *c_day = (char *) malloc (sizeof (char*) * DATE_LENGTH);
	
	int month;
	char *c_month = (char *) malloc (sizeof (char*) * DATE_LENGTH);

	int year;
	char *c_year = (char *) malloc (sizeof (char*) * DATE_LENGTH);
	
	char *system_log_path = "/home/doublea/var/log/iDDB/";
	char *system_file_log = "system.log";
	char *log_file = (char *) malloc (sizeof (char *) * MIN_STREAM_LENGTH/2);

	// decide the log level accepted
	if (strcmp(log_level, INFO) && strcmp(log_level, DEBUG) && 
		strcmp(log_level, WARN) && strcmp(log_level, ERROR)) {
		strcpy(log_level, INFO);
	}

	// build the file path... (as it is specified in the python logger file
	// see ../python_logger/python_logger.py)
	strcpy(log_file, system_log_path);
	strcat(log_file, system_file_log);

	fd = open(log_file, O_RDWR | O_APPEND | O_CREAT);
	if (fd < 0) {
		// TODO - take action???
	}	
	
	if (write(fd, info, strlen(info)) == 0) {
		// FIXME - take action...
	}


	// obtain current time
	time_t now;
	time(&now);
	struct tm *local = localtime(&now);
	hours = local->tm_hour;      	
    	minutes = local->tm_min;     	
    	seconds = local->tm_sec;     	

    	day = local->tm_mday;        	
    	month = local->tm_mon + 1;   	
    	year = local->tm_year + 1900;
	
	// convert all utilities to *char
	sprintf(c_hours, "%02d", hours);
	sprintf(c_minutes, "%02d", minutes);
	sprintf(c_seconds, "%02d", seconds);
	sprintf(c_day, "%02d", day);
	sprintf(c_month, "%02d", month);
	sprintf(c_year, "%02d", year);
	// end of current time ...
	
	printf("Time is : %d:%d:%d\n", hours, minutes, seconds);
	printf("Date is : %d-%02d-%d\n", day, month, year);
	
	// TO CONTINUE WITH - format the log line
	
	free (log_file);
	free (c_hours);
	free (c_minutes);
	free (c_seconds);
	free (c_day);
	free (c_month);
	free (c_year);
}

void main() {
	write_log(INFO, "a");  
}
