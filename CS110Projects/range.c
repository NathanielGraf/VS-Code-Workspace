#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
char string[1000] = "test";
int size;
int i;
int comma;
double lowest;
double highest; 
double dub;
int main(int argc, char* argv[]) 
{

    int i;

    // Prints argc and argv values
    printf("argc: %d\n", argc);
    for (i = 1; i < argc; ++i) 
    {   
        dub = atof(argv[i]);
        if(dub < lowest)
            lowest = dub;

        if(dub < highest)
            highest = dub; 
        printf("The range of these %d values is %lf", argc, highest - lowest);
    }

   return 0;
}