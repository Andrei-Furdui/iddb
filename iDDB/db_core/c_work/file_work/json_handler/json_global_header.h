// by importing following we may get some warnings depending which
// compiler is used - acceptable for now
// FIXME
#include "../../../../db_helper/c_helper/file_helper/dir_file_helper.c"
#include <string>

#define LOCAL_TAG "JSON_MANIPULATION"

/********************* CORE *********************/
/*** Name: is_table_available                   */
/*** Return type: bool                          */
/*** Purpose: returns 1 (TRUE) if the mentioned */
/***          table (file) exists or 0 (FALSE)  */
/***          otherwise                         */
/*** Parameter(s):                              */
/***              - table_name                  */
/*** Note: the C driver already has a function  */
/***       for this functionality but let's     */
/***       translate it here into the CPP world */
/************************************************/
[[deprecated("Replaced by is_table_available_improved() which is a better version \
of the C driver implementation")]]
inline bool is_table_available(std::string table_name);

// No comment needed - same as for the is_table_available() function 
// (see above)
bool is_table_available_improved(std::string table_name);

/********************* CORE *********************/
/*** Name: string build_table_path              */
/*** Return type: string (CPP only)             */
/*** Purpose: returns the full path of the      */
/***          specified file                    */
/*** Parameter(s):                              */
/***              - table_name                  */
/************************************************/
inline std::string build_table_path(std::string table_name);

/********************* CORE *********************/
/*** Name: convert_string_to_char_pointe        */
/*** Return type: string (CPP only)             */
/*** Purpose: converts the string native type   */
/***          from CPP into the char * for C    */
/*** Parameter(s):                              */
/***              - str                         */
/************************************************/
inline char* convert_string_to_char_pointer(std::string str);
