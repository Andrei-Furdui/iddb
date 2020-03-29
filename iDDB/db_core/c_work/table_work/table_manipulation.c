#include <stdio.h>
#include "../../../db_helper/c_helper/file_helper/dir_file_cons.h"
#include "../../../db_helper/c_helper/file_helper/dir_file_helper.c"

int create_empty_table(char *db_name, char *table_name, char *table_properties) {
	// make sure the database name is fine
	if (!check_null_argument(table_name) || !strlen(table_name)) {
		return FALSE;
	}

	char *log_info = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH/2);
	int result_fd = -3;
	char *table_path = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH);
	strcpy(table_path, home_path());
	strcat(table_path, DB_PATH);
	strcat(table_path, db_name);
	strcat(table_path, "/");
	strcat(table_path, table_name);
	strcat(table_path, TABLE_FILE_EXTENSION);

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
	fp = fopen(table_path, "a");
	if (fp == NULL) {
		strcat (log_info, "FALSE - the operation fails");
		write_log(INFO, log_info);
		free (log_info);
		free (table_path);
		return FALSE;
	}

	// let's mark the table's structure zone
	// the other zone is at the end of this function
	fprintf(fp, TABLE_PROPERTIES_COMMENT);

	// the table_properties parameter should have the following form:
	//table_name,column1_name-type, column2_name-type etc
	char *temp_column_name = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/2);
	short counter = 0;
	short column_number_id = 0;

	while (*table_properties != '\0') {

		if (*table_properties == ',') {
			column_number_id++;

			// end this string and write it to file
			temp_column_name[counter++] = '\0';

			// remove any extra white space
			while (*temp_column_name == ' ') {
				temp_column_name++;
			}

			char *aux_column_name = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/4);
			char *temp_id = (char* ) malloc (3 * sizeof(char *));

			if (aux_column_name == NULL || temp_id == NULL) {
				strcat (log_info, "FALSE - memory allocation failed(1)");
				write_log(INFO, log_info);
				free (log_info);
				free (table_path);
				free (aux_column_name);
				free (temp_id);
				free (temp_column_name);
				close (fp);
				return FALSE;
			}

			sprintf(temp_id, "%d", column_number_id);

			strcpy(aux_column_name, COLUMN_NUMBER);
			strcat(aux_column_name, temp_id);
			strcat(aux_column_name, ":");
			strcat(aux_column_name, temp_column_name);
			strcat(aux_column_name, "\n");

			result_fd = fprintf(fp, aux_column_name);
			if (!result) {
				strcat (log_info, "FALSE - writing to file operation failed");
				write_log(INFO, log_info);
				free (log_info);
				free (table_path);
				free (aux_column_name);
				free (temp_id);
				free (temp_column_name);
				close (fp);
				return FALSE;
			}

			// done writing to file, clear variables

			counter = 0;

			/*if (temp_column_name != NULL) {
				free (temp_column_name);
			}*/

			if (temp_column_name == NULL) {
				temp_column_name = (char *) realloc (TABLE_MANIPULATION_LENGTH/2, sizeof(char *));

				// since we're in a loop, check this
				if (temp_column_name == NULL) {
					strcat (log_info, "FALSE - memory allocation failed(2)");
					write_log(INFO, log_info);
					free (log_info);
					free (table_path);
					free (aux_column_name);
					free (temp_id);
					free (temp_column_name);
					close (fp);
					return FALSE;
				}
			}

			if (aux_column_name != NULL) {
				free (aux_column_name);
			}

			if (temp_id != NULL) {
				free (temp_id);
			}

		}
		else {
			temp_column_name[counter++] = *table_properties;
		}

		table_properties++;
	}

	char *write_to_file_table_name = (char *) malloc (sizeof(char *) * TABLE_MANIPULATION_LENGTH/2);
	strcpy (write_to_file_table_name, TABLE_NAME);
	strcat(write_to_file_table_name, table_name);
	strcat (write_to_file_table_name, "\n");
	fprintf(fp, write_to_file_table_name);

	// let's close the mark zone of the table
	fprintf(fp, TABLE_PROPERTIES_COMMENT);

	fclose(fp);
	strcat (log_info, "TRUE");
	write_log(INFO, log_info);

	if (log_info != NULL) {
		free (log_info);
	}

	if (table_path != NULL) {
		free (table_path);
	}

	if (write_to_file_table_name != NULL) {
		free (write_to_file_table_name);
	}

	return TRUE;
}

void main() {
	printf("RESULT: %d\n", create_empty_table("test", "exemplu12345.bat", "column1_name-type,column2_name-type,column3_name-type,"));
}
