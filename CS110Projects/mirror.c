#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
char string[1000];
char reversedstring[1000];

char outputString[100];
int x = 0;
int j = 0;
int i = 0;
int previousspaceindex;
int lastspaceindex;
int linewidth;
int charcount;

//Read in reverse string
//Iterate backwards until space is found
//Save index of the space
//Continue until char count = line width
//Subtract last space index from previous space index
//Subtract that count from line width
//Print that many spaces
//Print from last space index to previous space index
int main()
{   
    printf("Enter the width of an output line:\n");
    scanf("%d ", &linewidth);
    printf("Enter your text (control-d to exit):\n");
    fgets(string, 1000, stdin);
    string[strlen(string) - 1] = '\0';
    for(int i = strlen(string)-1; i >= 0; i--)
    {
        reversedstring[j] = string[i];
        j = j + 1;
    }
    charcount = 0;
    previousspaceindex = strlen(reversedstring)-1;
    for(int i = strlen(reversedstring)-1; i >= 0; i--)
    {
        charcount = charcount + 1;
        if(reversedstring[i] == ' ')
        {
            lastspaceindex = i;
        }

        if(charcount == linewidth)
        {
            for(int k = 0; k < (previousspaceindex - lastspaceindex); k++)
            {
                printf(" ");
            }
            for(int k = lastspaceindex; k < previousspaceindex; k++)
            {
                printf("%c", reversedstring[k]);
            }
            printf("\n");
            charcount = 0;
            previousspaceindex = lastspaceindex;
        }
    }
    for(int k = 0; k <= linewidth; k++)
    {
        printf("%d", k%10);
    }









}