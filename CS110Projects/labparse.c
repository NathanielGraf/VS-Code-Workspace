#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
char string[1000] = "test";
int size;
int i;
int comma;
int main() 
{

    while(strlen(string) > 1)
    {
        printf("Enter input string:\n");
        fgets(string, 1000, stdin);
        size = strlen(string);
        string[size - 1] = '\0';

        for(i = 0; i < size-1; i++)
        {
           printf("%c", string[i]);
        }
        printf("\n");

        for(i = 0; i < size; i++)
        {
            if(string[i] == ',')
            {
                comma = i;
            }

            else if(i == size - 1)
            {
                comma = 0;
                printf("Error: No comma in string.\n\n");
            }
        }
        
        if(comma != 0)
        {
            printf("First word: ");
            for(i = 0; i < comma; i++)
            {
                printf("%c", string[i]);
            }
            printf("\nSecond word: ");
            for(i = comma + 1; i < size; i++)
            {
                if (string[i] == ' ')
                {
                    continue;
                }
                else
                {
                    printf("%c", string[i]);
                }
            }
            printf("\n");
        }
    }
    return 0;

}
