#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

// if the RAM memory usage cannot be determined 
// then we'rw assuming that the minimum remaining
// room of the RAM memory is 512 MB
#define MAX_RAM 512

// values for the RAM quantity (kB)
#define _512MB_RAM 524288
#define _1GB_RAM 1048576

// this is the pattern of the available RAM memory from the 
// /proc/meminfo file
#define MEM_FREE "MemFree:"

/******************** HELPER ********************/
/*** Name: get_free_ram                         */
/*** Return type: long                          */
/*** Purpose: returns the amount of the Random  */
/***          Access Memory available on the    */
/***          device where it is called         */
/*** Parameter(s): N/A                          */
/************************************************/
long get_free_ram();

/******************** HELPER ********************/
/*** Name: allocate_ram_for_database            */
/*** Return type: long                          */
/*** Purpose: from the total amount of RAM      */
/***          obtained with get_free_ram()      */
/***          a lower value will be extracted - */
/***          in this way making sure that the  */
/***          total amount of RAM is enough for */
/***          the system                        */
/*** Parameter(s): N/A                          */
/************************************************/
long allocate_ram_for_database();

/******************** HELPER ********************/
/*** Name: kB_to_bytes                          */
/*** Return type: long long                     */
/*** Purpose: converts from kB to bytes         */
/*** Parameter(s):                              */
/***              - kB = value in kB that will  */
/***                     converted              */
/************************************************/
inline long long kB_to_bytes(long kB);
