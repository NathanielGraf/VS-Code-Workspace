#include <stdio.h>
#include <math.h>
#include <string.h>
int numtosum = 1234;
int nextdig;
int sum = 0;
int main()
{
    //scanf("%d", &numtosum);
    while(numtosum > 0);
    {
        nextdig = numtosum % 10;
        sum = sum + nextdig;
        numtosum = numtosum / 10;
    }
    printf("%d", sum);
    return 0;





}