#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "../../db_helper/c_helper/file_helper/dir_file_helper.c"

void generate_file_output(){

    char *final_message = (char *)malloc(1024 * sizeof(char));
    char *yaml_file_name = (char *)malloc(128 * sizeof(char));
    char *error_message = "*** ERROR while setting up the environment. Contact an administrator or try again!*** \n";

    char *initial_message = "################################################ \
    \n#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!# \
    \n#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!# \
    \n#This file is auto-gerenarted and should not be# \
    \n#edited by hand without authorization!!!!!!!!!!# \
    \n################################################";

    char *ip_node="\n#specify a list of servers (all nodes from this \
                    \n#deployment). The following is an example: \
                    \nip_node=a.b.c.d;e.f.g.h";
    
    char *port =   "\n#specify the port used by all nodes - this must \
                    \n#be the same for each node. \
                    \nport=9001\n";

    strcpy(final_message, initial_message);
    strcat(final_message, ip_node);
    strcat(final_message, port);
    strcpy(yaml_file_name,home_path());
    strcat(yaml_file_name, "var/iDDB/iddb.yaml");
    int fd = open(yaml_file_name, O_CREAT | O_WRONLY, 0600);
    if (fd <= 0){
        printf("%s\n", error_message);
        return;
    }

    if (write(fd, final_message, strlen(final_message)) <= 0){
        printf("%s\n", error_message);
        return; 
    }

    close(fd);
    free(final_message);
    free(yaml_file_name);
}

void main(void){
    generate_file_output();
}
