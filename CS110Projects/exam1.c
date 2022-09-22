#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
char string[100];
int i;
int reversecasing(void) 
{
    scanf("%s", &string);
    for (int i = 0; i < strlen(string); i++)
    {
        if (string[i] >= 'A' && string[i] <= 'Z')
        {
            string[i] = tolower(string[i]);
        }
        else if (string[i] >= 'a' && string[i] <= 'z')
        {
            string[i] = toupper(string[i]);
        }
    }
   
   return 0;
}