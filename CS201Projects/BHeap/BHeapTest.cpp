#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <unordered_map>
#include <cmath>

using namespace std;
template <typename keytype>
class BHeap
{
private:
    class Node 
    {
        //Each node in root list needs: 
        //Pointer to left and right
        //Pointer to children
        //Pointer to parent

        public:
        //Single key
        keytype key;

        //Child pointers, can have unlimited
        Node* child;

        //Degree of the node
        int degree;

        //Pointer to the parent
        Node* parent;

        Node* left;

        Node* right;

       

        //Default constructor
        Node() 
        {
            //Everything is nullptr
            child = nullptr;
            parent = nullptr;
            left = nullptr;
            right = nullptr;
            degree = 0;
        }
        

    };

    Node *minimum;

    int no_of_nodes;

    
public:

    //Heap should be empty:
    BHeap()
    {
        minimum = nullptr;

        no_of_nodes = 0;
    }

    BHeap(keytype k[], int s)
    {
        minimum = nullptr;

        for (int i = 0; i < s; i++)
        {
            insert(k);
        }
    }

    //Returns the key for the mimimum node
    keytype peekKey()
    {
        return(minimum->key);
    }

    void insert(keytype k)
    {
        //Create new node
        Node *newInsert = new Node();

        newInsert->left = newInsert;
        newInsert->right = newInsert;

        //Set key of new node
        newInsert->key = k;

        if (minimum == nullptr)
        {
            minimum = newInsert;
        }

        //If the new key is the new minimum, make minimum point to the new node
        //Put the new node to the left, update pointers
        minimum->left->right = newInsert;
        newInsert->right = minimum;
        newInsert->left = minimum->left;
        minimum->left = newInsert;

        //If the new key is the new minimum, make minimum point to the new node
        if (newInsert->key < minimum->key)
        {
            minimum = newInsert;
        }

        no_of_nodes++;


       
    }

    // Function to display the heap
    void display()
    {
        Node* ptr = minimum;
        if (ptr == nullptr)
            cout << "The Heap is Empty" << endl;
    
        else {
            cout << "The root nodes of Heap are: " << endl;
            do {
                cout << ptr->key;
                ptr = ptr->right;
                if (ptr != minimum) {
                    cout << "-->";
                }
            } while (ptr != minimum && ptr->right != nullptr);
            cout << endl
                << "The heap has " << no_of_nodes << " nodes" << endl;
        }
    }

    // Function to extract minimum node in the heap
    void extractMin()
    {
        
        
        Node* temp = minimum;
        Node* ptr;
        ptr = temp;
        Node* x = nullptr;
        if (temp->child != nullptr) {

            x = temp->child;
            do {
                ptr = x->right;
                (minimum->left)->right = x;
                x->right = minimum;
                x->left = minimum->left;
                minimum->left = x;
                if (x->key < minimum->key)
                    minimum = x;
                x->parent = nullptr;
                x = ptr;
            } while (ptr != temp->child);
        }
        (temp->left)->right = temp->right;
        (temp->right)->left = temp->left;
        minimum = temp->right;
        if (temp == temp->right && temp->child == nullptr)
            minimum = nullptr;
        else {
            minimum = temp->right;
            consolidate();
        }
        no_of_nodes--;
        
    }

    // Consolidating the heap
    void consolidate()
    {
        int temp1;
        int temp2 = static_cast<int>(log(no_of_nodes) / log(2));
        int temp3 = int(temp2);
        
        vector<Node*> arr(temp3 + 1, nullptr);

        for (int i = 0; i <= temp3; i++)
            arr[i] = nullptr;
        Node* ptr1 = minimum;
        Node* ptr2;
        Node* ptr3;
        Node* ptr4 = ptr1;
        do {
            ptr4 = ptr4->right;
            temp1 = ptr1->degree;
            while (arr[temp1] != nullptr) {
                ptr2 = arr[temp1];
                if (ptr1->key > ptr2->key) {
                    ptr3 = ptr1;
                    ptr1 = ptr2;
                    ptr2 = ptr3;
                }
                if (ptr2 == minimum)
                    minimum = ptr1;
                    //XXXXXXXXXXXXXXXXXX
                Fibonnaci_link(ptr2, ptr1);
                if (ptr1->right == ptr1)
                    minimum = ptr1;
                arr[temp1] = NULL;
                temp1++;
            }
            arr[temp1] = ptr1;
            ptr1 = ptr1->right;
        } while (ptr1 != minimum);
        minimum = nullptr;
        for (int j = 0; j <= temp3; j++) {
            if (arr[j] != nullptr) {
                arr[j]->left = arr[j];
                arr[j]->right = arr[j];
                if (minimum != nullptr) {
                    (minimum->left)->right = arr[j];
                    arr[j]->right = minimum;
                    arr[j]->left = minimum->left;
                    minimum->left = arr[j];
                    if (arr[j]->key < minimum->key)
                        minimum = arr[j];
                }
                else {
                    minimum = arr[j];
                }
                if (minimum == NULL)
                    minimum = arr[j];
                else i
	//Should output "B3: b c d e f g h i\n"
	
	H1.insert('j'); H1.insert('k'); H1.insert('l');
    
	cout << H1.extractMin() << endl;	//Should output b

	H1.printKey();
	//Should output	B3:\n c j d e f g h i\n B1:\n k l\n"
    */

	return 0;
}