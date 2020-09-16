#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include "../file_helper/dir_file_cons.h"
#include "../../../logger/c_logger/c_logger.c"
#include "../../common/log_reader.c"

void *how_use_command (void *my_command) {
  char *actual_command = (char *)my_command;
  
  char *final_message = (char *) malloc (sizeof(char *) * MIN_STREAM_LENGTH);

  // the pattern is the same for all commands
  strcpy(final_message, HELP_COMMAND_FIRST_PART);
  strcat(final_message, "'");
  strcat(final_message, actual_command);
  strcat(final_message, "'");
  strcat(final_message, "\n");

  // check what we want to display
  // based on the given command
  if (!strcmp(actual_command, LS_DATABASE)) {
    strcat(final_message, "--- Type 'ls database' OR 'ls databases'");
  }
  strcat(final_message, HELP_COMMAND_LAST_PART);

  // displaying the actual message
  printf("%s\n", final_message);

  if(final_message) {
    free(final_message);
  }
  return NULL;
}

// Implements the "EXAMPLE [command]" creating a new C thread with the output
void call_example_command_from_thread (char *command) {
  pthread_t how_to_thread;
  pthread_create(&how_to_thread, NULL, how_use_command, command);
  sleep (TIMEOUT_DISPLAYING_EXAMPLE_COMMAND);
  //pthread_exit(how_use_command);
}

// This method prints the output for the help command
// inserted by the client
void help_command () {
  char *final_message = (char *) malloc (sizeof(char *) * MAX_STREAM_LENGTH/50);

  if (final_message == NULL) {
    printf ("Error occured while displayed the help section - check logs for details!");
    write_log("ERROR", "Memory allocation error - help_command() function");
    return;
  }

  char *adm_message = "\nFor more information about iDDB, contact an administrator.\n";
  char *available_commands = "List of all available iDDB commands:\n";

  // database commands section
  char *ls_db = "1. LS DATABASE \t\t\t(core) Displayes all available databases\n";
  char *mk_db = "2. MKDIR DATABASE [db_name] \t(core) Creates a new (and empty) database\n";
  char *rm_db = "3. RMDIR DATABASE [db_name] \t(core) Removes an existing database\n";
  char *us_db = "4. USE DATABASE   [db_name] \t(core) Sets the current database (an existing one) for this session\n";

  // table commands section
  char *cr_tb = "\n5. CREATE TABLE [table_name (parameters...)]\t\t(core) Creates a new table\n";
  char *rm_tb = "6. DELETE TABLE [table_name]                   \t\t(core) Removes an existing table\n";
  char *de_tb = "7. DESC TABLE   [table_name]                   \t\t(core) Describes an existing table\n";
  char *up_tb = "8. UPDATE TABLE [table_name (parameters...)]   \t\t(core) Updates an existing table\n";

  char *in_tb = "\n9. INSERT INTO TABLE [table_name (parameters...)] \t\t(core) Inserts values into an existing table\n";
  char *se_tb = "10. SELECT [expr]|*|count(*) FROM [table_name (properties...)] \t(core) Selects specific data from an existing table\n";
  char *tr_tb = "11. TRUNCATE TABLE [table_name] \t\t\t\t(core) Removes all data from an existing table\n";
  char *exm_command = "\n12. EXAMPLE [command] \t\t (aux) Shows an example of how to use this command";
  
  // CAREFULL!!! - this should be the last command
  char *help = "\n13. HELP \t\t\t (aux) Displays this section\n";

  strcpy(final_message, adm_message);
  strcat(final_message, available_commands);
  strcat(final_message, ls_db);
  strcat(final_message, mk_db);
  strcat(final_message, rm_db);
  strcat(final_message, us_db);
  strcat(final_message, cr_tb);
  strcat(final_message, rm_tb);
  strcat(final_message, de_tb);
  strcat(final_message, up_tb);
  strcat(final_message, in_tb);
  strcat(final_message, se_tb);
  strcat(final_message, tr_tb);
  strcat(final_message, exm_command);
  strcat(final_message, help);

  printf ("%s\n", final_message);

  if(is_debug()) {
    write_log(DEBUG, "Displaying the help section...");
  }

  free (final_message);

}
