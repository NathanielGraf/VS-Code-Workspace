#include <stdio.h>
#include <math.h>

double rate;
int hours; 
double pay;


int main() 
{
    
    scanf("%lf %d", rate, hours);
    
    if (hours <= 40)
    { 
        pay = hours * rate;
    }
    else if (hours <= 50)
    {
        pay = (40 * rate) + ((hours - 40) * rate * 1.5);
    }
    else
    {
        pay = (40 * rate) + (10 * rate * 1.5) + ((hours - 50) * rate * 2);
    }

    printf("%f\n", pay);

   return 0;
}
