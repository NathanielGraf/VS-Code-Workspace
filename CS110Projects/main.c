#include <stdio.h>
#include <math.h>

int inputYear; 



int leapYear() 
{
    if (inputYear % 4 == 0)
    {
        if (inputYear % 100 == 0)
        {
            if (inputYear % 400 == 0)
            {
                printf("%d - leap year\n", inputYear);
            }
            else
            {
                printf("%d - not a leap year\n", inputYear);
            }
        }
        else
        {
            printf("%d - leap year\n", inputYear);
        }
    }
    else
    {
        printf("%d - not a leap year\n", inputYear);
    }
   
   return 0;
}
