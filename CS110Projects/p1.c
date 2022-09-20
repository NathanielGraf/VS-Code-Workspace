#include <stdio.h>
#include <math.h>

int twentys;
int tens;
int fives;
int ones;
int quarters;
int dimes;
int nickels;
int pennies;
int dollars;
int cents;
double length;


int findMoneyValue() 
{
    printf("Enter the number of $20s: ");
    scanf("%d", &twentys);
    printf("Enter the number of $10s: ");
    scanf("%d", &tens);
    printf("Enter the number of $5s: ");
    scanf("%d", &fives);
    printf("Enter the number of $1s: ");
    scanf("%d", &ones);
    printf("Enter the number of quarters: ");
    scanf("%d", &quarters);
    printf("Enter the number of dimes: ");
    scanf("%d", &dimes);
    printf("Enter the number of nickels: ");
    scanf("%d", &nickels);
    printf("Enter the number of pennies: ");
    scanf("%d", &pennies);
    
    dollars = (twentys * 20) + (tens * 10) + (fives * 5) + (ones * 1);
    cents = (quarters * 25) + (dimes * 10) + (nickels * 5) + (pennies * 1);
    
    printf("You have %d dollars and %d cents\n", dollars, cents);

    length = (int)(round((twentys * 6.14) + (tens * 6.14) + (fives * 6.14) + (ones * 6.14) + (quarters * 0.955) + (dimes * 0.705) + (nickels * 0.835) + (pennies * 0.750)));
    //length = (int)length;
    printf("The length of your money is roughly %f inches\n", length);

   return 0;
}
