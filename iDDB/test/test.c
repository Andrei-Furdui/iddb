#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void main () {
	char *t = (char *) malloc(sizeof(char));
	strcpy(t, "testasdasdasdasd");
	free (t);
	printf("%s\n", t);
	
}
