#include <iostream>
using namespace std;


bool getScores(double &score1, double &score2, double &score3, double &score4);
{
    cout << "Enter 4 test scores: ";
    cin >> score1 >> score2 >> score3 >> score4;
    if (score1 < 0 || score2 < 0 || score3 < 0 || score4 < 0)
    {
        cout << "Invalid input. Please enter a positive number.";
        return false;
    }
    else
    {
        return true;
    }
}
double calcAverage(double score1, double score2, double score3, double score4);
{
    double average = (score1 + score2 + score3 + score4) / 4;
    return average;
}

double calcAverageDropLowest(int score1, int score2, int score3, int score4);
{
    int lowest = score1;
    if (score2 < lowest)
    {
        lowest = score2;
    }
    if (score3 < lowest)
    {
        lowest = score3;
    }
    if (score4 < lowest)
    {
        lowest = score4;
    }
    double average = (score1 + score2 + score3 + score4 - lowest) / 3;
    return average;
}


void main()
{
    //Declare variables
    double score1, score2, score3, score4, average;
    bool valid;

    //Call function 1
    valid = getScores(score1, score2, score3, score4);

    //If data is valid, call function 2
    if (valid)
    {
        average = calcAverage(score1, score2, score3, score4);
        cout << "The average of the 4 scores is: " << average << endl;
        cout << "The average of the 3 highest scores is: " << calcAverageDropLowest(score1, score2, score3, score4) << endl;
    }
    else
        cout << "Invalid data. Please try again." << endl;
}