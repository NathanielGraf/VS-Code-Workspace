#include <stdio.h>
#include <math.h>
#include <string.h>
int num;
int nextdig;
int digarray[100];
int seendigits[10];
int i = 0;
int count = 0;
int inarray = 1;
int arethereduplicatedigitsinnumber()
{

    printf("Enter a number: ");
    scanf("%d", &num);
    while (num > 0)
    {
        nextdig = num % 10;
        digarray[i] = nextdig;
        num = num / 10;
        i = i + 1;
    }
    while (count < i)
    {
        if (seendigits[digarray[count]] == 1)
        {
            inarray = 0;
        }
        else
        {
            seendigits[digarray[count]] = 1;
        }
        count = count + 1;
    }
    if(inarray == 0)
    {
        printf("Duplicate digits found");
    }
    else
    {
        printf("No duplicate digits found");
    }
    




}