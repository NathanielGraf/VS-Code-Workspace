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

    // Consolidating the heap
    void consolidate()
    {

        //Determine the maximum possible degree of a node in the heap
        int maxDegree = (int)log2(no_of_nodes) + 1;
        
        vector<Node*> A(maxDegree, nullptr);
        //Set the maximum possible degree of a node in the heap to nullptr
        for (int i = 0; i <= maxDegree; i++)
            A[i] = nullptr;
        
        //Go through each node in the root list
        Node* w;
        w = minimum;
        
        while (w->right != minimum) 
        {
            Node *x = w;
            int d = x->degree;
           
            
            while (A[d] != nullptr && A[d] != x) 
            {
                Node* y = A[d];
                if (y == x)
                {
                    break;
                }
                else if (x->key > y->key) 
                {
                    Node* temp = x;
                    x = y;
                    y = temp;
                }
                
                Fibonnaci_link(y, x);

                A[d] = nullptr;
                d++;
            }
            A[d] = x;
            w = w->right;
        }

        //Do the same for the last node in the root list

        Node* x = w;
        int d = x->degree;
        while (A[d] != nullptr) 
        {

            Node* y = A[d];
            if (x->key > y->key) 
            {
                Node* temp = x;
                x = y;
                y = temp;
            }
            Fibonnaci_link(y, x);
            A[d] = nullptr;
            d++;
        }

        minimum = nullptr;

        for (int i = 0; i <= no_of_nodes; i++)
        {
            if (A[i] != nullptr)
            {
                if (minimum == nullptr)
                {
                    minimum = A[i];
                }
                else
                {
                    
                    (minimum->left)->right = A[i];
                    A[i]->right = minimum;
                    A[i]->left = minimum->left;
                    minimum->left = A[i];
                    

                    if (A[i]->key < minimum->key)
                    {
                        minimum = A[i];
                    }
                }
            }
        }

    }

    // Linking the heap nodes in parent child relationship
    void Fibonnaci_link(Node* ptr2, Node* ptr1)
    {


        //Remove node from root list of heap
        (ptr2->left)->right = ptr2->right;
        (ptr2->right)->left = ptr2->left;

        //If the node is the only node in the root list, set minimum to nullptr
        if (ptr1->right == ptr1)
        {
            minimum = ptr1;
        }
            

        
        ptr2->left = ptr2;
        ptr2->right = ptr2;


        ptr2->parent = ptr1;

        //If the parent has no children, set the child to the new node
        if (ptr1->child == nullptr)
        {
            ptr1->child = ptr2;
        }

        //If the parent has children, add the new node to the right of the child
        else if (ptr1->child != nullptr) 
        {
            ptr2->right = ptr1->child;
            ptr2->left = (ptr1->child)->left;
            ((ptr1->child)->left)->right = ptr2;
            (ptr1->child)->left = ptr2;
        }
       
        ptr1->degree++;
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
    printTree(Node* root)
    {
        if (root != nullptr) 
        {
            cout << root->key << endl;
            for (int i = 0; i < 100; i++)
            {
                if (root->children[i] != nullptr)
                {
                    printTree(root->children[i]);
                }
            }
        }
    }





    
    
        Writes the keys stored in the heap. Prints the
    tree with the minimum first, then proceeds
    through the root list printing each tree. When
    printing a binomial tree, print the size of tree first
    and then use a modified preorder traversal of the
    tree. See the example below
    */

    

   
    

    

    //Returns minimum node for printing purposes
    Node* getMinimum()
    {
        return(minimum);
    }

    /*
    

    //Prints the keys in preorder in the tree

    void printTree(Node* root)
    {
        if (root != nullptr) 
        {
            cout << root->key << endl;
            for (int i = 0; i < 100; i++)
            {
                if (root->children[i] != nullptr)
                {
                    printTree(root->children[i]);
                }
            }
        }
    }

    //First prints the tree of the minimum node, then the rest of the trees in the root list by going to the right and then around
    void printKey()
    {
        Node* temp = minimum;
        printTree(minimum);
        temp = minimum->right;
        while (temp != minimum && temp != nullptr)
        {
            printTree(temp);
            temp = temp->right;
        }

        temp = minimum;
        while (temp->left != minimum && temp->left != nullptr)
        {
            temp = temp->left;
        }

        while (temp != minimum && temp != nullptr)
        {   
            printTree(temp);
            if (temp != nullptr)
            {
                temp = temp->right;
            }
        }
    

    }

    keytype extractMin()
    {
        // Store the minimum key.
        keytype minKey = minimum->key;

        // Remove the minimum node from the root list.
        Node* oldMin = minimum;
        if (oldMin->right == nullptr && oldMin->left == nullptr) 
        {
            minimum = nullptr;
        } 
        else 
        {
            oldMin->right->left = oldMin->left;
            oldMin->left->right = oldMin->right;
            
            //Must find the min after we consolidate the trees
        }

        // Add the children of the minimum node to the root list.

        int i = 0;
        Node* prev = oldMin;
        while (oldMin->children[i] != nullptr) 
        {
            Node* child = oldMin->children[i];
            child->right = nullptr;
            prev->right = child;
            child->left = prev;
            prev = child;
            i++;
            if (i == 100) 
            {
                break;
            }
        }

        // Consolidate the heap.
        //if (minimum != nullptr) 
        //{
            //consolidate();
        //}

        // Return the minimum key.
        return minKey;
    }
    */
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

    cout << "Final printKey: \n";
    H1.printKey();
    
	cout << H1.extractMin() << endl;	//Should output b


	
    /*
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

	H1.printKey();
	//Should output	B3:\n c j d e f g h i\n B1:\n k l\n"
    */

	return 0;
}