#include <iostream>
#include <cstring>
#include <fstream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

//Merge sort code: 
void Merge(int numbers[], int i, int j, int k) {
   int mergedSize;                            // Size of merged partition
   int mergePos;                              // Position to insert merged number
   int leftPos;                               // Position of elements in left partition
   int rightPos;                              // Position of elements in right partition
   int* mergedNumbers = nullptr;

   mergePos = 0;
   mergedSize = k - i + 1;
   leftPos = i;                               // Initialize left partition position
   rightPos = j + 1;                          // Initialize right partition position
   mergedNumbers = new int[mergedSize];       // Dynamically allocates temporary array
                                              // for merged numbers
   
   // Add smallest element from left or right partition to merged numbers
   while (leftPos <= j && rightPos <= k) {
      if (numbers[leftPos] < numbers[rightPos]) {
         mergedNumbers[mergePos] = numbers[leftPos];
         ++leftPos;
      }
      else {
         mergedNumbers[mergePos] = numbers[rightPos];
         ++rightPos;
         
      }
      ++mergePos;
   }
   
   // If left partition is not empty, add remaining elements to merged numbers
   while (leftPos <= j) {
      mergedNumbers[mergePos] = numbers[leftPos];
      ++leftPos;
      ++mergePos;
   }
   
   // If right partition is not empty, add remaining elements to merged numbers
   while (rightPos <= k) {
      mergedNumbers[mergePos] = numbers[rightPos];
      ++rightPos;
      ++mergePos;
   }
   
   // Copy merge number back to numbers
   for (mergePos = 0; mergePos < mergedSize; ++mergePos) {
      numbers[i + mergePos] = mergedNumbers[mergePos];
   }
   delete[] mergedNumbers;
}

void MergeSort(int numbers[], int i, int k) {
   int j;
   
   if (i < k) {
      j = (i + k) / 2;  // Find the midpoint in the partition
      
      // Recursively sort left and right partitions
      MergeSort(numbers, i, j);
      MergeSort(numbers, j + 1, k);
      
      // Merge left and right partition in sorted order
      Merge(numbers, i, j, k);
   }
}

//Quick sort code:
int Partition(string numbers[], int i, int k) {
   int l;
   int h;
   int midpoint;
   string pivot;
   string temp;
   bool done;
   
   /* Pick middle element as pivot */
   midpoint = i + (k - i) / 2;
   pivot = numbers[midpoint];
   
   done = false;
   l = i;
   h = k;
   
   while (!done) {
      
      /* Increment l while numbers[l] < pivot */
      while (numbers[l] < pivot) {
         ++l;
      }
      
      /* Decrement h while pivot < numbers[h] */
      while (pivot < numbers[h]) {
         --h;
      }
      
      /* If there are zero or one elements remaining,
       all numbers are partitioned. Return h */
      if (l >= h) {
         done = true;
      }
      else {
         /* Swap numbers[l] and numbers[h],
          update l and h */
         temp = numbers[l];
         numbers[l] = numbers[h];
         numbers[h] = temp;
         
         ++l;
         --h;
      }
   }
   
   return h;
}

void Quicksort(string numbers[], int i, int k) {
   int j;
   
   /* Base case: If there are 1 or zero elements to sort,
    partition is already sorted */
   if (i >= k) {
      return;
   }
   
   /* Partition the data within the array. Value j returned
    from partitioning is location of last element in low partition. */
   j = Partition(numbers, i, k);
   
   /* Recursively sort low partition (i to j) and
    high partition (j + 1 to k) */
   Quicksort(numbers, i, j);
   Quicksort(numbers, j + 1, k);
}


//XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
//Actual code: 
//XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


//Main function
int main(int argc, char *argv[]) {

    //Sorting algo variable
    char input1;
    input1 = argv[1][0];
    
    //Filenames
    char inputFileName1[100];
    char inputFileName2[100];

    //Define inputFileName1 from command line argument
    strcpy(inputFileName1, argv[2]);
    strcpy(inputFileName2, argv[3]);

    if (input1 == 'i')
    {
        vector<int> intVector1;
        //Read in integers from file1
        ifstream inputFile1;
        inputFile1.open(inputFileName1);
        if (!inputFile1.is_open()) {
            cout << "Error opening input file" << endl;
            return 1;
        }
        int int1;
        while (inputFile1 >> int1)
        {
            intVector1.push_back(int1);
        }
        inputFile1.close();

        //Read in integers from file2
        vector<int> intVector2;
        ifstream inputFile2;
        inputFile2.open(inputFileName2);
        if (!inputFile2.is_open()) {
            cout << "Error opening input file" << endl;
            return 1;
        }
        int int2;
        while (inputFile2 >> int2)
        {
            intVector2.push_back(int2);
        }
        inputFile2.close();

        //Sort the intersection vector using quick sort
        //Convert vector to array
        int* strings1 = new int[intVector1.size()];
        int* strings2 = new int[intVector2.size()];
        for (int i = 0; i < intVector1.size(); i++)
        {
            strings1[i] = intVector1[i];
        }
        for (int i = 0; i < intVector2.size(); i++)
        {
            strings2[i] = intVector2[i];
        }

        //Call quicksort
        MergeSort(strings1, 0, intVector1.size() - 1);
        MergeSort(strings2, 0, intVector2.size() - 1);

        //Find intersection and print
        //For each string in strings1, check if it is in strings2
        for (int i = 0; i < intVector1.size()-1; i++)
        {
            //Checks to make sure we don't repeat the same string
            if (strings1[i] != strings1[i + 1])
            {
                //Prints intersection
                for (int j = 0; j < intVector2.size(); j++)
                {
                    if (strings1[i] == strings2[j])
                    {
                        cout << strings1[i] << endl;
                        break;
                    }
                }
            }
        }
        //Do last string
        for (int j = 0; j < intVector2.size(); j++)
        {
            if (strings1[intVector1.size() - 1] == strings2[j])
            {
                cout << strings1[intVector1.size() - 1] << endl;
                break;
            }
        }
    }

    if (input1 == 's')
    {
        vector<string> intVector1;
        //Read in integers from file1
        ifstream inputFile1;
        inputFile1.open(inputFileName1);
        if (!inputFile1.is_open()) {
            cout << "Error opening input file" << endl;
            return 1;
        }
        string string1;
        while (inputFile1 >> string1)
        {
            intVector1.push_back(string1);
        }
        inputFile1.close();

        //Read in integers from file2
        vector<string> intVector2;
        ifstream inputFile2;
        inputFile2.open(inputFileName2);
        //Check if file opened
        if (!inputFile2.is_open()) {
            cout << "Error opening input file" << endl;
            return 1;
        }
        string string2;
        while (inputFile2 >> string2)
        {
            intVector2.push_back(string2);
        }
        inputFile2.close();

        //Sort the intersection vector using quick sort
        //Convert vector to array
        string* strings1 = new string[intVector1.size()];
        string* strings2 = new string[intVector2.size()];
        for (int i = 0; i < intVector1.size(); i++)
        {
            strings1[i] = intVector1[i];
        }
        for (int i = 0; i < intVector2.size(); i++)
        {
            strings2[i] = intVector2[i];
        }

        //Call quicksort
        Quicksort(strings1, 0, intVector1.size() - 1);
        Quicksort(strings2, 0, intVector2.size() - 1);

        //Find intersection and print
        //For each string in strings1, check if it is in strings2
        for (int i = 0; i < intVector1.size()-1; i++)
        {
            //Checks to make sure we don't repeat the same string
            if (strings1[i] != strings1[i + 1])
            {
                //Prints intersection
                for (int j = 0; j < intVector2.size(); j++)
                {
                    if (strings1[i] == strings2[j])
                    {
                        cout << strings1[i] << endl;
                        break;
                    }
                }
            }
        }
        for (int j = 0; j < intVector2.size(); j++)
        {
            if (strings1[intVector1.size() - 1] == strings2[j])
            {
                cout << strings1[intVector1.size() - 1] << endl;
                break;
            }
        }


    }

    return 0;
}
