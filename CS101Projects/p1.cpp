#include <iostream>
#include <cstring>
#include <fstream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <unordered_set>

using namespace std;



int main(int argc, char *argv[]) 
{
    ifstream keyFile;
    ifstream codeFile;


    unordered_set<char>alphaSet({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'});

    unordered_set<char>alphaKeySet({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'});

    //Get file names from command line
    string keyFileName, codeFileName;
    keyFileName = argv[1];
    codeFileName = argv[2];
    //cout << keyFileName << " " << codeFileName << endl;

    //Open files
    keyFile.open(keyFileName);
    codeFile.open(codeFileName);

    //Check if files are open
    if (!keyFile.is_open()) {
        cout << "Error opening key file" << endl;
        return 1;
    }
    if (!codeFile.is_open()) {
        cout << "Error opening code file" << endl;
        return 1;
    }

    string alphabetLine;
    getline(keyFile, alphabetLine);

    string keyLine;
    getline(keyFile, keyLine);

    map<char, char> keyMap;
    for (int i = 0; i < alphabetLine.size(); i++) 
    {
        
        //Remove keyLine[i] from alphabetKey and alphabetLine[i] from alphabet sets
        alphaKeySet.erase(keyLine[i]);
        alphaSet.erase(alphabetLine[i]);


        keyMap[keyLine[i]] = alphabetLine[i];
    }
    
    //Get the text from the code file. 
    string codeText;
    string line;
    while (getline(codeFile, line)) 
    {
        codeText += line;
        //Add new line character to the end of the line
        codeText += '\n';
    }
    
    //Decode the text, if the character is a space, add a space to the decoded text.
    //If the character does not exist in the keyMap, print the character as is.
    //Otherwise, add the decoded character to the decoded text.
    //State tracker keeps track of whether the character was decoded or not, 1 for decoded, 0 for not decoded.
    string stateTracker;
    string decodedText;
    for (int i = 0; i < codeText.size(); i++) 
    {
        if (codeText[i] == ' ') 
        {
            decodedText += ' ';
            //stateTracker += ' ';
        }
        else if (keyMap.find(codeText[i]) == keyMap.end()) 
        {
            decodedText += codeText[i];
            //stateTracker += "0";
        }
        else 
        {
            decodedText += keyMap[codeText[i]];
            //stateTracker += "1";
        }
    }

    //stateTracker maker
    for (int i = 0; i < codeText.size(); i++) 
    {
        
        if (isalpha(codeText[i]) == false) 
        {
            stateTracker += " ";
        }
        else if (keyMap.find(codeText[i]) == keyMap.end()) 
        {
            decodedText += codeText[i];
            stateTracker += "0";
        }
        else 
        {
            decodedText += keyMap[codeText[i]];
            stateTracker += "1";
        }
    }
    //cout << stateTracker << endl;
    //Get the key word the command line:
    string keyWord = argv[3];
    string foundWord;
    string foundState;
    //Find the first instance of the key word in the decoded text, the characters must match if the state tracker at that index is 1.
    int i; 
    for (i = 0; i < decodedText.size(); i++) 
    {
        //cout << decodedText[i] << " " << stateTracker[i] << endl;
        int j;
        for (j = 0; j < keyWord.size(); j++) 
        {
            //cout << decodedText[i + j] << " " << keyWord[j] << " " << stateTracker[i + j] << endl;
            
            if (decodedText[i + j] == keyWord[j] || stateTracker[i + j] == '0') 
            {
                //cout << " J:" << j << endl;
                continue; 
            }
            else 
            {
                goto exit;
            }

            
        }
        //cout << "Found ";
        //int k;
        //for (k = 0; k < keyWord.size(); k++) 
        //{
            //cout << decodedText[i + k];
        //}
        //cout << endl;
        
        //Turn the characters of the word into a string
        
        for (int k = 0; k < keyWord.size(); k++) 
        {
            foundWord += decodedText[i + k];
        }

        for (int k = 0; k < keyWord.size(); k++) 
        {
            foundState += stateTracker[i + k];
        }
        break;


        exit: 
        continue;
    }
    //cout << foundWord << endl;
    //cout << foundState << endl;

    for (int i = 0; i < foundWord.size(); i++) 
    {
        if (foundState[i] == '0') 
        {
            alphaKeySet.erase(foundWord[i]);
            alphaSet.erase(keyWord[i]);
            keyMap[foundWord[i]] = keyWord[i];
        }
    }

    if (alphaSet.size() == 1 && alphaKeySet.size() == 1) 
    {
        keyMap[*alphaKeySet.begin()] = *alphaSet.begin();
    }


    for (int i = 0; i < codeText.size(); i++) 
    {
        if (codeText[i] == ' ') 
        {
            cout << ' ';
            //stateTracker += ' ';
        }
        else if (keyMap.find(codeText[i]) == keyMap.end()) 
        {
            cout << codeText[i];
            //stateTracker += "0";
        }
        else 
        {
            cout << keyMap[codeText[i]];
            //stateTracker += "1";
        }
    }

    

    

    return 0;
}




