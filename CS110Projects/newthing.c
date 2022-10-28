#include <stdio.h>
#include <math.h>
#include <string.h>
int numtosum;
int range;
int currentmax = -100000;
int currentmin = 100000; 
int main()
{
    scanf("%d", &numtosum);
    while(numtosum != "CTRL-D")
    {
        if(numtosum > currentmax)
        {
            currentmax = numtosum;
        }
        else if(numtosum < currentmin)
        {
            currentmin = numtosum;
        }
        scanf("%d", &numtosum);

    }
    range = currentmax - currentmin;
    printf("%d", range);
    return 0;





}