#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
char string[1000];
int size;
int i;
int x;
int int1;
int int2;
int main(int argc, char* argv[]) 
{
    FILE *input1 = fopen(argv[1], "r");
    FILE *input2 = fopen(argv[2], "r");

    fscanf(input1, "%d", int1);
    fscanf(input2, "%d", int2);

    while(input1 != EOF && input2 != EOF)
    {
        if(int1 < int2)
        {
            printf("%d", int1);
            fscanf(input1, "%d", int1);
        }
        else if(int1 > int2)
        {
            printf("%d", int2);
            fscanf(input2, "%d", int2);
        }
        else
        {
            printf("%d", int1);
            fscanf(input1, "%d", int1);
            fscanf(input2, "%d", int2);
        }
    }
    return 0;

    while(input1 != EOF)
    {
        printf("%d", int1);
        fscanf(input1, "%d", int1);
    }

    while(input2 != EOF)
    {
        printf("%d", int2);
        fscanf(input2, "%d", int2);
    }


}



/*
Read number1 from file1
Read number2 from file2
While ( not EOF for file1 AND not EOF for file2 )
    If number1 is less than number2
       Print number1 and read the next number from file1
    Else if number1 is greater than number2
       Print number2 and read the next number from file2
    Else (the numbers are the same)
       Print the number and read the next number from both files
End while
// at most one of the following two while statements will be true
While( file1 has not yet hit EOF)
   Print number1 and read the next number from file1
End while
While( file2 has not yet hit EOF)
   Print number2 and read the next number from file2
End while









*/