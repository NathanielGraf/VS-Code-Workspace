#include <stdio.h>
#include <string.h>
#include <ctype.h>

void CreateAcronym(char userPhrase[], char userAcronym[])
{
    int i;
    int j = 0;
    for (i = 0; i < strlen(userPhrase); i++)
    {
        if (i == 0)
        {
            if(isupper(userPhrase[i]) != 0);
            {
                userAcronym[j] = userPhrase[i];
                j++;
            }
        }
        else if (userPhrase[i] == ' ')
        {
            if (isupper(userPhrase[i + 1]) != 0)
            {
                userAcronym[j] = userPhrase[i + 1];
                j++;
            }
        }
    }
}


int main() {
    char userPhrase[300];
    char userAcronym[100];
    int i;
    fgets(userPhrase, 300, stdin);
    userPhrase[strlen(userPhrase) - 1] = '\0';
    CreateAcronym(userPhrase, userAcronym);
    for(i=0; i<strlen(userAcronym); i++)
    {
        printf("%c.", userAcronym[i]);
    }   
    printf("The acronym is: %s", userAcronym);
    return 0;
}
