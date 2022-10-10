#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char string[1000];
int size;

int isNegativeInteger(char string[], int size)
{
    int i = 0;
    if(string[0] != '-')
    {
        return 0;
    }
    else
    {
        for(i = 1; i < size; i++)
        {
            if (string[i] < '0' || string[i] > '9')
            {
                return 0;
            }
        }
    }
    return 1;
}

int isBinary(char string[], int size)
{
    int i = 0;
    
    if(string[0] != '0')
    {
        return 0;
    }
    else if(string[1] != 'b')
    {
        return 0;
    }
    else
    {
        for(i = 2; i < size; i++)
        {
            if (string[i] != '0' && string[i] != '1')
            {
                return 0;
            }
        }
    }
    return 1;
}

int isInteger(char string[], int size)
{
    int i = 0;
    for(i = 0; i < size; i++)
    {
        if (string[i] < '0' || string[i] > '9')
        {
            return 0;
        }
    }
    return 1;
}

int isGUID(char string[], int size)
{
    int i = 0;
    if(string[8] != '-' || string[13] != '-' || string[18] != '-' || string[23] != '-')
    {
        return 0;
    }
    else
    {
        for(i = 0; i < size; i++)
        {
            if (i == 8 || i == 13 || i == 18 || i == 23)
            {
                continue;
            }
            else if (string[i] != '0' && string[i] != '1' && string[i] != '2' && string[i] != '3' && string[i] != '4' && string[i] != '5' && string[i] != '6' && string[i] != '7' && string[i] != '8' && string[i] != '9' && string[i] != 'a' && string[i] != 'b' && string[i] != 'c' && string[i] != 'd' && string[i] != 'e' && string[i] != 'f' && string[i] != 'A' && string[i] != 'B' && string[i] != 'C' && string[i] != 'D' && string[i] != 'E' && string[i] != 'F')
            {
                return 0;
            }
        }
    }
    return 1;
}

int isFloat()
{
    int i = 0;
    int decimal = 0;
    int decimalindex = 0;
    for(i = 0; i < size; i++)
    {
        if (string[i] == '.')
        {
            decimalindex = i;
            decimal++;
        }
        else if (string[i] < '0' || string[i] > '9')
        {
            return 0;
        }
    }
    if(decimal == 1)
    {
        if(string[decimalindex-1] < '0' || string[decimalindex-1] > '9' || string[decimalindex+1] < '0' || string[decimalindex+1] > '9')
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
}

int isNegativeFloat()
{
    int i = 0;
    int decimal = 0;
    int decimalindex = 0;
    if(string[0] != '-')
    {
        return 0;
    }
    for(i = 1; i < size; i++)
    {

        if (string[i] == '.')
        {
            decimalindex = i;
            decimal++;
        }
        else if (string[i] < '0' || string[i] > '9')
        {
            return 0;
        }
    }
    if(decimal == 1)
    {
        if(string[decimalindex-1] < '0' || string[decimalindex-1] > '9' || string[decimalindex+1] < '0' || string[decimalindex+1] > '9')
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
}

void main()
{
    printf("Enter a token to identify, EOF to stop:\n");
    while(scanf("%s", string) != EOF)
    {
        size = strlen(string);

        if(isNegativeInteger(string, size))
            printf("The token is a negative integer\n");
        
        else if(isInteger(string, size))
            printf("The token is a positive integer\n");

        else if(isGUID(string, size))
            printf("The token is a guid\n");

        else if(isBinary(string, size))
            printf("The token is a binary number\n");

        else if(isFloat(string, size))
            printf("The token is a positive floating-point number\n");
        
        else if(isNegativeFloat(string, size))
            printf("The token is a negative floating-point number\n");

        else
            printf("The token cannot be identified\n");

        printf("Enter a token to identify, EOF to stop:\n");


    }

}