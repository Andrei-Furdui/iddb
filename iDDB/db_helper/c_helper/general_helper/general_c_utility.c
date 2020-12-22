#include <stdio.h>
#include "general_c_utility.h"

long get_free_ram() {
    int fd = open ("/proc/meminfo", O_RDONLY);
    if (fd < -1) {
        close (fd);
        return MAX_RAM;
    }
    

    int meminfo_file_length = 1024; //1024 is more than enough...
    short max_digits = 10; // (usually!) the primitive long type can store up to 10 digits
    long result = -1;
    
    char *buffer = (char *) malloc (meminfo_file_length * sizeof (char));
   
    if (buffer == NULL) {
        close (fd);
        return MAX_RAM;
    }

    if (read (fd, buffer, meminfo_file_length) <= 0) {
        free (buffer);
        close (fd);
        return MAX_RAM;
    }
    
    close (fd);
    
    char *token = strtok (buffer, "\n");
    
    while (token != NULL) {
        if (strstr(token, MEM_FREE)) {
            
            // get the numerical value from the token
            // and store it into another variable...
            char *str_digits = (char *) malloc (max_digits * sizeof(char));
            short local_counter = 0;
            if (str_digits == NULL) {
                free (token);
                free(buffer);
                return MAX_RAM;
            }
            for(; *token != '\0'; *token++){
                if (*token >= '0' && *token <= '9') {
                    str_digits[local_counter++] = *token;
                }
                
                // if the kB word is met then stop
                if (*token == 'k' || *token == 'B') {
                    break;
                }
                
            }
            str_digits[local_counter] = '\0';
            result = strtol(str_digits, &str_digits, max_digits);
            break;
        }
        token = strtok(NULL, "\n"); 
    }
    
    return result == -1? MAX_RAM: result;
}

long allocate_ram_for_database() {
    long total_ram = get_free_ram();
    long real_result = 0;
    if (total_ram <= _512MB_RAM) {
        real_result = _512MB_RAM/2; 
    }
    else if(total_ram <= _1GB_RAM) {
        real_result = _512MB_RAM;
    }
    else {
        real_result = total_ram - _1GB_RAM;
    }
    
    return real_result;
}

inline long long kB_to_bytes(long kB) {
    return kB * 1024;
}

void main() {
    printf ("%ld\n", get_free_ram());
    printf ("%ld\n", allocate_ram_for_database());
}
