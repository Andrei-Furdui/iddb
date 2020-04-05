#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
//#include <stdio.h>
#include <time.h>
#include <unistd.h>
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

	// final date format
	// this should contain something like this:
	// year-month-day hour:min:sec
	// TODO - verify this
	char *c_final_date = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	char *c_final_day_moment = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	// this should contain all needed info before actual log
	char *c_final_format = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	// this should contain the final version of the log line
	char *c_final_log = (char *) malloc (sizeof(char *) * MAX_STREAM_LENGTH/2);

	char *system_log_path = "/home/doublea/var/log/iDDB/";
	char *system_file_log = "system.log";
	char *log_file = (char *) malloc (sizeof (char *) * MIN_STREAM_LENGTH/2);

	// decide the log level accepted
	if (strcmp(log_level, INFO) && strcmp(log_level, DEBUG) &&  -
		strcmp(log_level, WARN) && strcmp(log_level, ERROR)) {
		// be carefull - this can cause a segmentation fault!!!
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

	// these are temp variables - so they are declared here
	char *temp_date = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	char *temp_day_moment = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);

	// that's it, they are somehow hardcoded (following string operations)
	// we don't care about this right now
	// a TODO is left here because an improvment can be made in this sitaution
	// here
	strcpy(temp_date, c_year);
	strcat(temp_date, "-");
	strcat(temp_date, c_month);
	strcat(temp_date, "-");
	strcat(temp_date, c_day);
	strcat(temp_date, " ");

	// final date format stored into c_final_date
	strcpy(c_final_date, temp_date);


	strcpy(temp_day_moment, c_hours);
	strcat(temp_day_moment, ":");
	strcat(temp_day_moment, c_minutes);
	strcat(temp_day_moment, ":");
	strcat(temp_day_moment, c_seconds);

	// final day moment here
	strcpy(c_final_day_moment, temp_day_moment);

	// this should contain the first part of the log line
	// the one with actual moment
	strcpy(c_final_format, c_final_date);
	strcat(c_final_format, c_final_day_moment);
	strcat(c_final_format, "[");
	strcat(c_final_format, log_level);
	strcat(c_final_format, "]");
	strcat(c_final_format, ":");
	strcat(c_final_format, " ");

	strcpy(c_final_log, c_final_format);
	strcat(c_final_log, info);
	strcat(c_final_log, "\n");

	if (write(fd, c_final_log, strlen(c_final_log)) == 0) {
		// FIXME - take action...
		// e.g. retry this action
	}

	close (fd);

	free (temp_date);
	free (log_file);
	free (c_hours);
	free (c_minutes);
	free (c_seconds);
	free (c_day);
	free (c_month);
	free (c_year);
	free (c_final_date);
	free (c_final_day_moment);
	free (temp_day_moment);
	free (c_final_format);
	free (c_final_log);
}

//void main() {
//	write_log(INFO, "A log from the C level here");
//}
