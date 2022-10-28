#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
char string[5000];
char reversedstring[5000];
int x = 0;
int j = 0;
int i = 0;
int k;
int previousspaceindex;
int lastspaceindex;
int linewidth;
int charcount;
int skipspace;
char totalstring[5000];
char word[5000];
int charsleft;
char reversedword[5000];
char temp[5000];
int chars;
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
    scanf("%d", &linewidth);
    printf("Enter your text (control-d to exit):\n\n");
    charsleft = linewidth;
    scanf("%s", word);
    while(word != NULL)
    {
        //print("lol");
        if(strlen(word) <= charsleft)
        {
            chars = strlen(word);
            strcat(word, " ");
            j = 0;
            for(k = strlen(word) - 1; k >= strlen(word)/2; k--)
            {   
                *temp = word[j];
                word[j] = word[k];
                word[k] = *temp;
                j++;
            }
            strcat(word, totalstring);
            strcpy(totalstring, word);
            charsleft = charsleft - chars -1;
            scanf("%s", word);
        }
        else
        {
            for(i = 0; i < charsleft+1; i++)
            {
                printf(" ");
            }
            char* printword = totalstring + 1;
            printf("%s\n", printword);
            strcpy(totalstring, "");
            charsleft = linewidth;
        }
    }
    
    for(k = 1; k <= linewidth; k++)
    {
        printf("%d", k%10);
    }
    printf("\n");

    return 0;
    //Iterate backwards through the string
    //Keep track of the char count
    //When at a space, save it's index 
    //If you hit 10 chars, print from current space index to the previous space index
}