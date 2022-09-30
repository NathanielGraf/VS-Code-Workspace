#include <stdio.h>
#include <math.h>
#include <string.h>
char line[1000];
int i;
char seenletters[26];
int missingletters()
{
    fgets(line, 1000, stdin);
    line[strlen(line)-1] = '\0';
    printf("Missing letters: ");
    for(i = 0; i < strlen(line); i++)
    {
        if(seenletters[line[i]] == 1)
        {
            continue;
        }
        else
        {
            seenletters[line[i]] = 1;
            printf("%c ", line[i]);
        }
    
    }
}