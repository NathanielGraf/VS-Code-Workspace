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

        no_of_nodes = 0;

        for (int i = 0; i < s; i++)
        {
            insert(k[i]);
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

        else
        {
            //Insert the new node to the right of the minimum node
            newInsert->right = minimum->right;
            newInsert->left = minimum;
            (minimum->right)->left = newInsert;
            minimum->right = newInsert;

            //If the new key is the new minimum, make minimum point to the new node
            if (newInsert->key < minimum->key)
            {
                minimum = newInsert;
            }
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
    keytype extractMin()
    {
        
        keytype returnKey = minimum->key;
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

        return returnKey;
        
    }

    void consolidate() 
    {
        int maxDegree = (int)log2(no_of_nodes) + 1;
        vector<Node*> A(maxDegree, nullptr);

        Node* w = minimum;
        if (w == nullptr) return;

        vector<Node*> rootList; // Store all nodes in the root list
        Node* current = w;
        do {
            rootList.push_back(current);
            current = current->right;
        } while (current != w);

        for (Node* w : rootList) {
            Node* x = w;
            int d = x->degree;
            while (A[d] != nullptr) {
                Node* y = A[d];
                if (y == x) {
                    break; // Prevent a node from being linked to itself
                }
                if (x->key > y->key) {
                    swap(x, y);
                }
                Fibonnaci_link(y, x);
                A[d] = nullptr;
                d++;
            }
            A[d] = x;
        }

        minimum = nullptr;
        for (int i = 0; i < maxDegree; i++) {
            if (A[i] != nullptr) {
                A[i]->left = A[i];
                A[i]->right = A[i];
                if (minimum == nullptr) {
                    minimum = A[i];
                } else {
                    // Insert A[i] into the root list
                    minimum->left->right = A[i];
                    A[i]->right = minimum;
                    A[i]->left = minimum->left;
                    minimum->left = A[i];
                    // Update the minimum, if necessary
                    if (A[i]->key < minimum->key) {
                        minimum = A[i];
                    }
                }
            }
        }
    }

    // Linking the heap nodes in parent child relationship
    void Fibonnaci_link(Node* y, Node* x) 
    {
        // Remove y from the root list
        y->left->right = y->right;
        y->right->left = y->left;
        
        // Make y a child of x
        y->parent = x;
        y->left = y;   // Point y's left and right to itself to remove it from the root list
        y->right = y;

        // Insert y into x's child list
        if (x->child == nullptr) {
            x->child = y;
        } else {
            // Add y to the beginning of the child list (circular doubly linked list)
            Node* lastChild = x->child->left; // Last child in x's current child list
            lastChild->right = y;
            x->child->left = y;
            y->right = x->child;
            y->left = lastChild;
        }

        // Increment the degree of x
        x->degree++;
        
        // Optionally clear y's mark if you're using marked nodes for decrease-key operations
    }



    void printPreOrder(Node* node)
    {
        if (node == nullptr)
            return;

        cout << node->key << " "; // Print the current node's key
        Node* child = node->child;

        if (child != nullptr) {
            Node* current = child;
            do {
                printPreOrder(current); // Recursively print each child
                current = current->right; // Move to the next child
            } while (current != child); // Ensure that we stop when we complete the loop
        }
    }

    void printKey()
    {
        if (minimum == nullptr)
        {
            cout << "The Heap is Empty" << endl;
            return;
        }

        Node* temp = minimum;
        do {
            cout << "B" << temp->degree << ":" << endl;
            printPreOrder(temp); // Print the tree rooted at 'temp' in preorder
            cout << endl;
            temp = temp->right; // Move to the next node in the root list
        } while (temp != minimum); // Ensure that we stop when we complete the loop
    }



  
};

    
    

/**/
int main()
{

    char K[6] = {'a','b','c','d','e','f'};
	
	BHeap<char> H1, H2;
	for(int i=0; i<6; i++) H1.insert(K[i]);
	
	cout << H1.extractMin() << endl; //Should output a
	
	H1.printKey();
	//Should output "B2:\n b c d e\n B0:\n f \n"
	
	H1.insert('g'); H1.insert('h'); H1.insert('a'); H1.insert('i');
	
	H1.printKey();
	//Should output "B0:\n a\n B2:\n b c d e\n B0:\n f\n B0:\n g\n B0:\n h\n B0:\n i\n"
	
	cout << H1.extractMin() << endl; 	//Should output a

	H1.printKey();	
	//Should output "B3: b c d e f g h i\n"
	
	H1.insert('j'); H1.insert('k'); H1.insert('l');
    
	cout << H1.extractMin() << endl;	//Should output b


	return 0;
}