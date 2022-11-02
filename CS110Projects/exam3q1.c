#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/*
 The command line will contain a number (N) and a file name (INPUT).
 
 Your program will read N strings from from INPUT and store them in an array.
 
 Some of the strings will be numeric (integer) in range 0 ..< N (0 <= number < N).
 The number may be larger, smaller, or the same as its own index,
 but will be a valid index in range 0 up to N-1.
 Print the strings at the index position of all numeric strings found.
 
 There are no "trick" words.
 If a word begins with a digit you may assume it is a number.
 
 
 Example: a.out 5 inputfile.txt
 inputfile.txt: 0 3 apple baker 2
 Output: 0 baker apple
*/

int main(int argc, char **argv){
    int stringNum;
    stringNum = atoi(argv[1]);
    //printf("%d", stringNum);

    char *stringArray[stringNum];

    FILE *fp;
    fp = fopen(argv[2], "r");
    
    //Read in all strings from file into array

    int i;
    for(i = 0; i < stringNum; i++){
        stringArray[i] = malloc(100);
        fscanf(fp, "%s", stringArray[i]);
    }


    for(int j = 0; j < stringNum; j++)
    {
        {
        printf("%s lol", stringArray[j]);
        }
    }

    for(int i = 0; i < stringNum; i++){
        if(isdigit(stringArray[i][0])){
            printf("%s ", stringArray[atoi(stringArray[i])]);
        }
    }
    return 0;
}
