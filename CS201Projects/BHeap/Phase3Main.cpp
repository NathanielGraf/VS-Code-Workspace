#include <iostream>
using namespace std;
#include "BHeap.cpp"

void printErrors(string errors, int numOfErrors){
        if(numOfErrors < 5){
                cout << errors << " passed (Key:imeidj)" << endl;
        }else if(numOfErrors < 100){
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
        }else if (numOfErrors < 1000){
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
        }else if (numOfErrors < 10000){
                cout << errors << " caused " << numOfErrors << " of errors ADD+1(Key:kdjoum)" << endl;
        }else{
                cout << errors << " caused " << numOfErrors << " of errors " << endl;
        }
}

int main(){
        string A[20] = {"AD","AB","AA","A","B","C","D","E","F","H","I","J","K","L","M","O","Q","R","S","T"};
       
        BHeap<string> Z(A,20), Y;

		cout << "ACTUALLY RUNNING" << endl;
 
        Z.printKey();
   //B4:A AA AB AD B C D E F H I J K L M O

  //B2:
   //Q R S T


        cout << Z.extractMin() << endl;       //A

        Z.printKey();
        //B0:
 //AA

//B1:
//AB AD

//B4:
//B C D E Q R S T F H I J K L M O
       
        Y.insert("p");
        Y.insert("h");
        Y.insert("a");
        Y.insert("s");
        Y.insert("e");
        Y.insert("3");
        Y.printKey();
   //B0:
//3

//B0:
//a

//B0:
//h

//B0:
//p

//B0:
//s

//B0:
//e

       
        Y.merge(Z);
   
        Y.printKey();
    //B0:
//3

//B0:
//a

//B0:
//h

//B0:
//p

//B0:
//s

//B0:
//e

//B0:
//AA

//B1:
//AB AD

//B4:
//B C D E Q R S T F H I J K L M O

        cout << Y.peekKey() << endl;            //3
        cout << Y.extractMin() << endl;       //3
        Y.printKey();
        //B3:
//AA e AB AD a h p s

//B4:
//B C D E Q R S T F H I J K L M O
       
        BHeap<int> X;
        for(int i = 0; i < 100000; i++){
                X.insert(i);
        }
        int peakKey=0;
        int extractMin=0;
        for(int i = 0; i < 100000; i++){
                if(X.peekKey() != i) peakKey++;
                if(X.extractMin() != i) extractMin++;
        }
        //peakkey passed (Key:imeidj)
        printErrors("peakKey",peakKey);
        //extractMin passed (Key:imeidj)
        printErrors("extractMin",extractMin);          
       
        BHeap<int> C,D;
        for(int i = 0; i < 100000; i++){
                C.insert(i);
                D.insert(100000+i);
        }
        C.merge(D);
        peakKey=0;
        extractMin=0;
        for(int i = 0; i < 199999; i++){
                if(C.peekKey() != i) peakKey++;
                if(C.extractMin() != i) extractMin++;
        }
        //peakkey passed (Key:imeidj)
        printErrors("peakKey",peakKey);
        //extractMin passed (Key:imeidj)
        printErrors("extractMin",extractMin);
        return 0;
}