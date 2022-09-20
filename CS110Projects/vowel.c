#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
char string[100];
int acount;
int ecount;
int icount;
int ocount;
int ucount;


int main()
{
    
    
    while (scanf("%s", string) != EOF);
    {
        for(int i = 0; i < strlen(string); i++)
        {
            if (toupper(string[i]) == 'A')
            {
                acount = acount + 1;
            }
            if (toupper(string[i]) == 'E')
            {
                ecount = ecount + 1;
            }
            if (toupper(string[i]) == 'I')
            {
                icount = icount + 1;
            }
            if (toupper(string[i]) == 'O')
            {
                ocount = ocount + 1;
            }
            if (toupper(string[i]) == 'U')
            {
                ucount = ucount + 1;
            }
        }
        
    } 
    printf("The vowel A occured %d times\n", acount);
    printf("The vowel E occured %d times\n", ecount);
    printf("The vowel I occured %d times\n", icount);
    printf("The vowel O occured %d times\n", ocount);
    printf("The vowel U occured %d times\n", ucount);









}