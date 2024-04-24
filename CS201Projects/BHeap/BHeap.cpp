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
            //Insert the new node to the left of the minimum node
            newInsert->right = minimum;
            newInsert->left = minimum->left;
            minimum->left = newInsert;
            newInsert->left->right = newInsert;

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
        Node* start = nullptr;
        ptr = temp;
        Node* x = nullptr;
        if (temp->child != nullptr) {
            start = temp->child;
            x = temp->child;
            do {
                ptr = x->right;
                (minimum->left)->right = x;
                x->right = minimum;
                x->left = minimum->left;
                minimum->left = x;
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
            //Must make the smallest child of temp the new minimum
            if (start != nullptr)
            {
                minimum = start;
            }
            //cout << "Consolidating the heap" << endl;
            //printKey();
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
                    Node* temp = x;
                    x = y;
                    y = temp;
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
            // Add y to the end of the child list (circular doubly linked list)
            y->right = x->child;
            y->left = x->child->left;
            x->child->left->right = y;
            x->child->left = y;
            
            
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

    /*
    Merges the heap H2 into the current heap.
Consumes H2, H2 should be empty after. H2’s
root list should be inserted to the left of the
minimum in H1, with the minimum in H2 being
the first root inserted
    */
    void merge(BHeap<keytype> &H2)
    {
        if (H2.minimum == nullptr)
        {
            return;
        }

        if (minimum == nullptr)
        {
            minimum = H2.minimum;
            no_of_nodes = H2.no_of_nodes;
            H2.minimum = nullptr;
            H2.no_of_nodes = 0;
            return;
        }
        Node* temp = minimum->left;
        
        minimum->left->right = H2.minimum;
        minimum->left = H2.minimum->left;
        H2.minimum->left->right = minimum;
        H2.minimum->left = temp;
        
        if (H2.minimum->key < minimum->key)
        {
            minimum = H2.minimum;
        }

        no_of_nodes += H2.no_of_nodes;

        H2.minimum = nullptr;

        H2.no_of_nodes = 0;


        
        
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

    //cout << "LOOK" << endl;
    //H1.printKey();
    
	cout << H1.extractMin() << endl;	//Should output b

	H1.printKey();
	//Should output	B3:\n c j d e f g h i\n B1:\n k l\n"
	
	H2.insert('A'); H2.insert('B'); H2.insert('C'); H2.insert('D');
	cout<< H2.extractMin() << endl;	//Should output A

	H2.printKey();
	//Should output "B1:\n B C\n B0:\n D\n"
	
	H1.merge(H2); H1.printKey();
	//Should output "B1: B C\n B0:\n D\n B3:\n c j d e f g h i\n B1:\n k l\n"
	
	cout << H1.extractMin() << endl;	//Should output B

	H1.printKey();
	//Should output "B2:\n C D k l\n B3:\n c j d e f g h i\n"
	
	return 0;

}