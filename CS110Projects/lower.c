#include <stdio.h>
#include <math.h>
#include <string.h>
char word1[];
char word2[];
int i=0;
int j=0;
int lowers1 = 0;
int lowers2 = 0;
int oneminustwo = 0;
int twominusone = 0;
int main()
{
    scanf("%d ", &word1);
    scanf("%d", &word2);
    while(i<strlen(word1))
    {
        if(islower(word1[i]) == 1)
        {
            lowers1 = lowers1 + 1;
        }
        i = i + 1;
    }
    while(i<strlen(word2))
    {
        if(islower(word2[i]) == 1)
        {
            lowers2 = lowers2 + 1;
        }
        i = i + 1;
    }
    oneminustwo = lowers1 - lowers2;
    twominusone = lowers2-lowers1;
    if (lowers1 > lowers2)
    {
        
    }
    else if (lowers2 > lowers1)
    {
        printf("'%s' contains %d more lowercase letter(s) than '%s'.", word2, twominusone, word1);
    }
    else if (lowers1 == lowers2)
    {
        printf("'%s' and '%s' both contain %d lowercase letter(s).", word1, word2, lowers1);
    }
    return 0;





}