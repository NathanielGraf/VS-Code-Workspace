#include <stdio.h>
#include <math.h>
#include <string.h>
int N;
int main()
{
    scanf("%d", N);
    for(int i = 0; i < N; i++)
    {
        printf("X");
    }
    for (int i = 0; i < N-2; i++)
    {
        printf("X");
        for (int j = 0; j < N-2; j++)
        {
            printf(" ");
        }
        printf("X");
    }
    for(int i = 0; i < N; i++)
    {
        printf("X");
    }









}