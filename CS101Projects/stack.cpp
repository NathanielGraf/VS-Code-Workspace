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

int main(int argc, char* argv[])
{
    //Read in string from command line: 
    string input = argv[1];
    vector<char> stack;
    int i = 0;

    //Iterate through string:   
    while (i < input.length())
    {
        cout << "Stack: "; 
        for (int j = 0; j < stack.size(); j++)
        {
            cout << stack[j] << " ";
        }
        cout << endl;
        cout << "Character: " << input[i] << endl;
        //If the character is an opening bracket, push it onto the stack: 
        if (input[i] == '(' || input[i] == '[' || input[i] == '{' || input[i] == '<')
        {
            cout << "Push";
            stack.push_back(input[i]);
        }
        //If the character is a closing bracket, check if it matches the top of the stack: 
        else if (input[i] == ')' || input[i] == ']' || input[i] == '}' || input[i] == '>')
        {
            //If the stack is empty, the brackets are not balanced: 
            if (stack.empty())
            {
                cout << "unmatched right symbol" << input[i] << endl;
                return 0;
            }
            //If the character is a closing bracket and it matches the top of the stack, pop the top of the stack: 
            else if (input[i] == ')' && stack.back() == '(')
            {
                cout << "Matching " << "( " << "and " << ")" << endl;
                stack.pop_back();
            }
            else if (input[i] == ']' && stack.back() == '[')
            {
                cout << "Matching " << "[ " << "and " << "]" << endl;
                stack.pop_back();
            }
            else if (input[i] == '}' && stack.back() == '{')
            {
                cout << "Matching " << "{ " << "and " << "}" << endl;
                stack.pop_back();
            }
            else if (input[i] == '>' && stack.back() == '<')
            {
                cout << "Matching " << "< " << "and " << ">" << endl;
                stack.pop_back();
            }
            //If the character is a closing bracket and it does not match the top of the stack, the brackets are not balanced: 
            else
            {
                cout << "mismatched pair " << stack.back() << " " << input[i] << endl;
                return 0;
            }
        }
        //If the character is not a bracket, do nothing: 
        else
        {
            cout << "invalid character " << input[i] << endl;
        }
        i++;
    }


}
