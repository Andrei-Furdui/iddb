#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../file_helper/dir_file_cons.h"
#include "../../../logger/c_logger/c_logger.c"

// This method prints the output for the help commands
// inserted by the client
void help_command() {
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
  write_log(DEBUG, "Displaying the help section...");

  free (final_message);
}
