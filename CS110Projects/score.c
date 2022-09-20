#include <stdio.h>
#include <math.h>

double exam1;
double exam2; 
double exam3; 
double exam4; 
double examlist[4];
double currentlowest = 100.0;
int lowindex;
double sum = 0.0;


int findMoneyValue() 
{
    
    scanf("%lf %lf %lf %lf", exam1, exam2, exam3, exam4);
    //scanf("%lf", exam2);
    //scanf("%lf", exam3);
    //scanf("%lf", exam4);


    examlist[0] = exam1;
    examlist[1] = exam2;
    examlist[2] = exam3;
    examlist[3] = exam4;

    for (int i = 0; i < 4; i++)
    {
        if (examlist[i] < currentlowest)
        {
            currentlowest = examlist[i];
            lowindex = i;
        }
    }
    examlist[lowindex] = 0.0;
    
    for (int i = 0; i < 4; i++)
    {
        sum = sum + examlist[i];
    }

    printf("The average of your three highest scores is %f\n", sum/3);


   return 0;
}
