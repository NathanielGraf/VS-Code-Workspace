#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
int i = 0;
int digit = 0;
int upper = 0;
int lower = 0;

void main(int argc, char **argv)
{
    for(i = 0; i < argv[0]; i++)
    {
        if(isdigit(argv[0][i]) == 0)
        {
            digit = digit + 1;
        }
        if(isupper(argv[0][i]) == 0)
        {
            upper = upper + 1;
        }
        if(islower(argv[0][i]) == 0)
        {
            lower = lower + 1;
        }
    }
    printf("Uppers = %d", upper);
    printf("Lowers =  %d", lower);
    printf("Digits =  %d", digit);




}