#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int size;
char string[1000];
int integer;
void shiftLeft(char string[], int size)
{
    int i;
    char temp;
    temp = string[0];
    for(i = 0; i < size; i++)
    {
        string[i] = string[i+1];
    }
    string[size-1] = temp;
}

void shiftRight(char string[], int size)
{
    int i;
    char temp;
    temp = string[size-1];
    for(i = size-1; i > 0; i--)
    {
        string[i] = string[i-1];
    }
    string[0] = temp;
}

void decreaseChar(char string[], int size)
{
    int i;
    for(i = 0; i < size; i++)
    {
        if(string[i] >= 33 && string[i] <= 126)
        {
            if(string[i] == 33)
                string[i] = 126;
            else
                string[i] = string[i] - 1;
        }
    }
}

void increaseChar(char string[], int size)
{
    int i;
    for(i = 0; i < size; i++)
    {
        if(string[i] >= 33 && string[i] <= 126)
        {
            if(string[i] == 126)
                string[i] = 33;
            else
                string[i] = string[i] + 1;
        }
    }
}

void binaryEncode(char string[], int size, int integer)
{
    int i;
    char binaryrep[1000] = "";
    int binarychar = 0;
    char ch;
    while (integer > 0)
    {
        if(integer % 2 == 0)
        {
            ch = '0';
        }
        else
        {
            ch = '1';
        }
        strncat(binaryrep, &ch, 1);
        integer = integer / 2;
    }
    for(i = 0; i < size; i++)
    {
        if(string[i] >= 48 && string[i] <= 57)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 48)
                {
                    string[i] = 57;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
            else
            {
                if(string[i] == 57)
                {
                    string[i] = 48;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
        }
        if(string[i] >= 65 && string[i] <= 90)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 65)
                {
                    string[i] = 90;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
            else
            {
                if(string[i] == 90)
                {
                    string[i] = 65;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
        }
        if(string[i] >= 97 && string[i] <= 122)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 97)
                {
                    string[i] = 122;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
            else
            {
                if(string[i] == 122)
                {
                    string[i] = 97;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
        }
        if(binarychar < strlen(binaryrep) - 1)
        {
            binarychar++;
        }
        else
        {
            binarychar = 0;
        }
    }
}

void binaryDecode(char string[], int size, int integer)
{
    int i;
    char binaryrep[1000] = "";
    int binarychar = 0;
    char ch;
    while (integer > 0)
    {
        if(integer % 2 == 0)
        {
            ch = '0';
        }
        else
        {
            ch = '1';
        }
        strncat(binaryrep, &ch, 1);
        integer = integer / 2;
    }
    for(i = 0; i < size; i++)
    {
        if(string[i] >= 48 && string[i] <= 57)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 57)
                {
                    string[i] = 48;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
            else
            {
                if(string[i] == 48)
                {
                    string[i] = 57;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
        }
        if(string[i] >= 65 && string[i] <= 90)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 90)
                {
                    string[i] = 65;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
            else
            {
                if(string[i] == 65)
                {
                    string[i] = 90;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
        }
        if(string[i] >= 97 && string[i] <= 122)
        {
            if(binaryrep[binarychar] == '0')
            {
                if(string[i] == 122)
                {
                    string[i] = 97;
                }
                else
                {
                    string[i] = string[i] + 1;
                }
            }
            else
            {
                if(string[i] == 97)
                {
                    string[i] = 122;
                }
                else
                {
                    string[i] = string[i] - 1;
                }
            }
        }
        if(binarychar < strlen(binaryrep) - 1)
        {
            binarychar++;
        }
        else
        {
            binarychar = 0;
        }
    }
}


int main(int argc, char *argv[])
{
    if(argc != 4)
    {
        printf("Invalid number of arguments, must be exactly 4\n");
        return 0;
    }

    if(strcmp(argv[2], "encode") != 0 && strcmp(argv[2], "decode") != 0)
    {
        printf("Invalid option, must be 'encode' or 'decode'!\n");
        return 0;
    }


    char modifier[1000];
    strcpy(modifier, argv[3]);
    FILE *fp;
    char filename[100];
    strcpy(filename, argv[1]);
    fp = fopen(filename, "r");
    //fp = stdin;

    if(fp)
    {   
        int i;
        for(i = 0; i < strlen(modifier); i++)
        { 
            if(i % 2 == 0)
            {
                if(modifier[i] != 'L' && modifier[i] != 'R' && modifier[i] != 'C' && modifier[i] != 'B')
                {
                    if(strcmp(argv[2], "encode") == 0)
                        printf("I cannot encrypt the message with task '%c'!\n", modifier[i]);
                    else if(strcmp(argv[2], "decode") == 0)
                        printf("I cannot decrypt the message with task '%c'!\n", modifier[i]);
                    return 0;
                }
            }
            else
            {
                if(isdigit(modifier[i]) == 0)
                {
                    if(strcmp(argv[2], "encode") == 0)
                        printf("Please enter a valid number for the encryption task '%c'!\n", modifier[i-1]);
                    else if(strcmp(argv[2], "decode") == 0)
                        printf("Please enter a valid number for the decryption task '%c'\n", modifier[i-1]);
                    return 0;
                }
            }
        }
        while(fscanf(fp, "%s", string) != EOF)
        {
            //printf("|STRING:%s|", string);
            int j;
            int i;
            int repeatnum;
            //printf("%d", strlen(modifier));
            for(i = 0; i < strlen(modifier); i++)
            {
                //printf("LOOPIN%d|", i);
                if(isdigit(modifier[i] - '0') != 0)
                    continue;
                if(modifier[i] == 'L')
                {
                    repeatnum = modifier[i+1] - '0';
                    if(strcmp(argv[2], "encode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                        {   
                            //printf("%d", modifier[i+1] - '0');
                            //printf("running left shift\n");
                            shiftRight(string, strlen(string));
                            //printf("|ENCODED STRING LEFT SHIFTY:%s|", string);
                        }
                            
                    }
                    else if(strcmp(argv[2], "decode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                            shiftLeft(string, strlen(string));
                    }      
                }
                else if(modifier[i] == 'R')
                {
                    repeatnum = modifier[i+1] - '0';
                    if(strcmp(argv[2], "encode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                        {

                            shiftLeft(string, strlen(string));
                            //printf("|ENCODED STRING RIGHT SHIFTY:%s|", string);
                        }
                    }
                    else if(strcmp(argv[2], "decode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                            shiftRight(string, strlen(string));
                    }      
                }
                else if(modifier[i] == 'C')
                {
                    repeatnum = modifier[i+1] - '0';
                    if(strcmp(argv[2], "encode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                            decreaseChar(string, strlen(string));
                    }
                    else if(strcmp(argv[2], "decode") == 0)
                    {
                        for(j = 0; j < repeatnum; j++)
                            increaseChar(string, strlen(string));
                    }
                }
                else if(modifier[i] == 'B')
                {
                    repeatnum = modifier[i+1] - '0';
                    if(strcmp(argv[2], "encode") == 0)
                    {
                        binaryEncode(string, strlen(string), repeatnum);
                    }
                    else if(strcmp(argv[2], "decode") == 0)
                    {
                        binaryDecode(string, strlen(string), repeatnum);
                    }
                }
                //printf("END OF LOOP FAM LIT AF\n");
            }
            printf("%s\n", string);
        }
    }
    else
    {
        printf("Could not open file '%s'\n", filename);
        return 0;
    }
}