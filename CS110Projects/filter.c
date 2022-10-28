#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
char string[1000];
int size;
int i;
int x;
int main(int argc, char* argv[]) 
{
    if(fopen(argv[1], "r") == 0)
        {
            printf("Cannot open file '%s'\n", argv[1]);
        }
    else if(fopen(argv[2], "w") == 0)
        {
            printf("Cannot open file '%s'\n", argv[2]);
        }
    else
    {
        FILE *input = fopen(argv[1], "r");
        FILE *output = fopen(argv[2], "w");
        while(fscanf(input, "%s", string) != EOF)
        {
            x = 0;

            for(i=0; i<strlen(string); i++)
            {
                if(isalpha(string[i]) == 0)
                {
                    x = 1;
                }
            }
            if(x == 0)
            {
                fprintf(output, "%s", string);
            } 
        }
    }

   return 0;
}