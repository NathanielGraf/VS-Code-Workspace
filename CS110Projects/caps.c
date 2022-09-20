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
int wordcount;
char outputString[100];
int x = 0;


int main()
{
    
    printf("Enter how many words:\n");
    scanf("%d", &wordcount);
    printf("Enter %d words:\n", wordcount);

    while (scanf("%s", string) != EOF);
    {
        if(strlen(string) > 3)
        {
            for(int i = 0; i < strlen(string); i++)
            {
                if (isupper(string[i]))
                {
                    outputString[x] = string[i];
                    x = x + 1;
                }
            }

        }
    }
    printf("The result is: %s








}