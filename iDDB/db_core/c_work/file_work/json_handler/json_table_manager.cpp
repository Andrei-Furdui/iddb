#include <iostream>
#include "json_global_header.h"

namespace helper {
    [[deprecated]]
    inline bool is_table_available(std::string table_name) {
        char *C_supported_table_name = new char[table_name.size()+1];
        strcpy(C_supported_table_name, table_name.c_str());
        return check_file_exists(C_supported_table_name) == 1? true:false;
    }
    
    inline char* convert_string_to_char_pointer(std::string str){
        char *C_supported_table_name = new char[str.size()+1];
        strcpy(C_supported_table_name, str.c_str());
        return C_supported_table_name;
    }
    
    bool is_table_available_improved(std::string table_name) {
        char *temp_table_name = convert_string_to_char_pointer(table_name);
        int fd = open(temp_table_name, O_RDONLY);
        close (fd);
        return fd > 0;
    }
    
    inline std::string build_table_path(std::string table_name) {
        std::string final_path = home_path();
        final_path += DB_PATH + table_name;
        return final_path;
    }
}

int main(){
    std::string test = helper::build_table_path("system12.log");
    std::cout << "HELLO " + test << std::endl;
    bool result = helper::is_table_available_improved(test);
    printf("AICI %d\n", result);
    return 0;
}