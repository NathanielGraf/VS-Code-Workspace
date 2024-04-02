#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <unordered_map>

using namespace std;

template <typename elmtype>
class CircularDynamicArray
{
public:
    elmtype *arr;
    int sz;
    int cap;
    int front;
    int back;

    // Default Constructor
    CircularDynamicArray() 
    {
        sz = 0;
        cap = 2;
        front = 0;
        back = 0;
        arr = new elmtype[cap];
    }
    
    //Constructor
    CircularDynamicArray(int s)
    {
        sz = s;
        cap = s;
        front = 0;
        back = 0;
        arr = new elmtype[cap];
    }

    // Destructor
    ~CircularDynamicArray()
    {
        delete[] arr;
    }

    // Copy Constructor
    CircularDynamicArray(const CircularDynamicArray &cda)
    {
        arr = new elmtype[cda.cap];
        sz = cda.sz;
        cap = cda.cap;
        front = cda.front;
        back = cda.back;
        for (int i = 0; i < sz; i++)
        {
            arr[(front + i) % cap] = cda.arr[(cda.front + i) % cda.cap];
        }
    }

    // Copy Assignment Operator
    CircularDynamicArray &operator=(const CircularDynamicArray &cda)
    {
        if (this != &cda)
        {
            delete[] arr;
            arr = new elmtype[cda.cap];
            sz = cda.sz;
            cap = cda.cap;
            front = cda.front;
            back = cda.back;
            for (int i = 0; i < sz; i++)
            {
                arr[(front + i) % cap] = cda.arr[(cda.front + i) % cda.cap];
            }
        }
        return *this;
    }

    // Subscript Operator
    elmtype &operator[](int i)
    {
        return arr[(front + i) % cap]; // Consider the circular nature
    }

    // Add an element at the front
    void addFront(elmtype v)
    {
        if (sz == cap)
        {
            resize(cap * 2);
        }
        front = (front - 1 + cap) % cap; // Move front back one position, wrapping around if necessary
        arr[front] = v;
        sz++; // Increment size after adding the element
    }
    
    void delFront()
    {
        if (sz == 0) // Check if the array is empty
        {
            cout << "Array is empty. No elements to remove from the front." << endl;
            return;
        }

        front = (front + 1) % cap; // Move front to the next element
        sz--; // Decrease the size

        // Check if size is 25% or less of capacity
        if (sz > 0 && sz <= cap / 4)
        {
            resize(cap / 2); // Resize to half the current capacity
        }
    }

    int length()
    {
        return sz;
    }

    int capacity()
    {
        return cap;
    }

    void clear()
    {
        delete[] arr;
        sz = 0;
        cap = 2;
        front = 0;
        back = 0;
        arr = new elmtype[cap];
    }

    // Method to print the array contents
    void printArray() const {
        for (int i = 0; i < sz; ++i) {
            cout << arr[(front + i) % cap];
            if (i < sz - 1) {
                cout << ", ";
            }
        }
    }


private:
    // Resize the array when it's full
    void resize(int newCapacity)
    {
        elmtype *temp = new elmtype[newCapacity];
        for (int i = 0; i < sz; i++)
        {
            temp[i] = arr[(front + i) % cap]; // Copy elements in circular order
        }
        delete[] arr;
        arr = temp;
        cap = newCapacity;
        front = 0; // Reset front to 0
        back = sz; // Update back based on the new size
    }
};

template <typename keytype, typename valuetype>
class two4Tree 
{
private:
    class Node 
    {
        //Each node of the tree needs: 
        //1. A vector of keys
        //2. A vector of values
        //3. A vector of children
        //4. A pointer to the parent

        //Array of 3 keys
        //4 child pointers
        //int type {2,3,4}, 2 is 2-node, 3 is 3-node, 4 is 4-node
        //Subtree size
        //CDA <valuetype> values [3]
        // duplicates [3]

        public:
        
        //Array of 3 keys
        keytype keys[3];

        //Counter for duplicates of each key
        int duplicates[3];

        //The 3 indices of the values array contains CDA's of values
        //Use a CircularDynamicArray to store the values, 3 CDA's in the array
        CircularDynamicArray<valuetype> values[3];
        

        //4 child pointers
        Node *children[4];

        //Pointer to the parent
        Node *parent;

        //int type {2,3,4}, 2 is 2-node, 3 is 3-node, 4 is 4-node
        int type = 2;

        //Subtree size
        int subtreeSize = 1;

        //Default constructor
        Node() 
        {
            // Initialize each CircularDynamicArray object in the 'values' array
            for (int i = 0; i < 3; ++i) 
            {
                values[i] = CircularDynamicArray<valuetype>();
            }
            // Set all children to nullptr initially
            for (int i = 0; i < 4; ++i) 
            {
                children[i] = nullptr;
            }
            parent = nullptr;
            // Initialize duplicates array
            for (int i = 0; i < 3; ++i) 
            {
                duplicates[i] = 0;
            }
        }

    };

    Node *root;
public:
    
    //Default constructor
    two4Tree() 
    {
        root = nullptr;
    }

    //Copy constructor
    two4Tree(const two4Tree &other) 
    {

        //Call a recursive helper function to copy all nodes in the tree
        root = copyTree(other.root);

        
    }

    two4Tree(keytype k[], valuetype v[], int s) 
    {
        root = nullptr;
        for (int i = 0; i < s; i++) 
        {
            insert(k[i], v[i]);
        }
    }

    
    //Destructor
    // Helper function to recursively delete nodes
    void clear(Node* node) {
        if (node != nullptr) {
            // Recursively delete child nodes
            for (int i = 0; i < 4; ++i) {
                clear(node->children[i]);
            }
            // After the children have been deleted, delete the node itself
            delete node;
        }
    }

    //Create hash table to store counter of each key
    

    unordered_map<keytype, int> duplicatehash;

    //Duplicate key counter map, RETURN counter of key
    int duplicates(keytype key) 
    {
        return duplicatehash[key];
    }

    
    //Insert a key-value pair into the tree
    void insert(keytype key, valuetype value) 
    {
        //Start at root, traverse down to leaf

        //If root is null, create a new node with the key-value pair
        if (root == nullptr) 
        {
            root = new Node();
            root->keys[0] = key;
            root->values[0].addFront(value);

            duplicatehash[key] = 1;

            cout << "Tree structure after inserting key: " << key << "\n";
            printNodeStructure(root);
            cout << "---------------------------------\n";
            return;
        }
        Node *curr = root;
        while (curr != nullptr) 
        {   
            if (curr->type == 2) 
            {
                insert2Node(*curr, key, value);

                cout << "Tree structure after inserting key: " << key << "\n";
                printNodeStructure(root);
                cout << "---------------------------------\n";
                return;
            } 
            else if (curr->type == 3) 
            {
                insert3Node(*curr, key, value);

                cout << "Tree structure after inserting key: " << key << "\n";
                printNodeStructure(root);
                cout << "---------------------------------\n";
                return;
            } 
            else if (curr->type == 4) 
            {
                insert4Node(*curr, key, value);

                cout << "Tree structure after inserting key: " << key << "\n";
                printNodeStructure(root);
                cout << "---------------------------------\n";
                return;
            }
        }

        
    }

    void insert2Node(Node &curr, keytype key, valuetype value)
    {


        //cout << "Inserting into 2-node " << endl;
        if (key < curr.keys[0]) 
        {
            if (curr.children[0] == nullptr) 
            {
                curr.keys[1] = curr.keys[0];
                curr.values[1] = curr.values[0];
                curr.keys[0] = key;
                curr.values[0].addFront(value);
                duplicatehash[key] = 1;
                curr.type = 3;
            } 
            else 
            {
                
                if (curr.children[0]->type == 2) 
                {
                    insert2Node(*curr.children[0], key, value);
                } 
                else if (curr.children[0]->type == 3) 
                {
                    insert3Node(*curr.children[0], key, value);
                } 
                else if (curr.children[0]->type == 4) 
                {
                    insert4Node(*curr.children[0], key, value);
                }
            }
        } 
        else if (key > curr.keys[0]) 
        {
            if (curr.children[1] == nullptr) 
            {
                curr.keys[1] = key;
                curr.values[1].addFront(value);
                duplicatehash[key] = 1;
                curr.type = 3;
            } 
            else 
            {
                if (curr.children[1]->type == 2) 
                {
                    insert2Node(*curr.children[1], key, value);
                } 
                else if (curr.children[1]->type == 3) 
                {
                    insert3Node(*curr.children[1], key, value);
                } 
                else if (curr.children[1]->type == 4) 
                {
                    insert4Node(*curr.children[1], key, value);
                }
            }
        } 
        
        else 
        {
            curr.values[0].addFront(value);
            duplicatehash[key]++;
        }
    }

    void insert3Node(Node &curr, keytype key, valuetype value)
    {


        if (key < curr.keys[0]) 
        {
            if (curr.children[0] == nullptr) 
            {
                curr.keys[2] = curr.keys[1];
                curr.values[2] = curr.values[1];
                curr.keys[1] = curr.keys[0];
                curr.values[1] = curr.values[0];
                curr.keys[0] = key;
                curr.values[0].addFront(value);
                
                duplicatehash[key] = 1;

                curr.type = 4;
            } 
            else 
            {
                if (curr.children[0]->type == 2) 
                {
                    insert2Node(*curr.children[0], key, value);
                } 
                else if (curr.children[0]->type == 3) 
                {
                    insert3Node(*curr.children[0], key, value);
                } 
                else if (curr.children[0]->type == 4) 
                {
                    insert4Node(*curr.children[0], key, value);
                }
            }
        } 
        else if (key > curr.keys[0] && key < curr.keys[1]) 
        {
            if (curr.children[1] == nullptr) 
            {
                curr.keys[2] = curr.keys[1];
                curr.values[2] = curr.values[1];
                curr.keys[1] = key;
                curr.values[1].addFront(value);

                duplicatehash[key] = 1;

                curr.type = 4;
            } 
            else 
            {
                if (curr.children[1]->type == 2) 
                {
                    insert2Node(*curr.children[1], key, value);
                } 
                else if (curr.children[1]->type == 3) 
                {
                    insert3Node(*curr.children[1], key, value);
                } 
                else if (curr.children[1]->type == 4) 
                {
                    insert4Node(*curr.children[1], key, value);
                }
            }
        } 
        else if (key > curr.keys[1]) 
        {
            if (curr.children[2] == nullptr) 
            {
                curr.keys[2] = key;
                curr.values[2].addFront(value);

                duplicatehash[key] = 1;

                curr.type = 4;
            }
            else 
            {
                if (curr.children[2]->type == 2) 
                {
                    insert2Node(*curr.children[2], key, value);
                } 
                else if (curr.children[2]->type == 3) 
                {
                    insert3Node(*curr.children[2], key, value);
                } 
                else if (curr.children[2]->type == 4) 
                {
                    insert4Node(*curr.children[2], key, value);
                }
            }
        }

        else
        {
            if (curr.keys[0] == key) 
            {
                curr.values[0].addFront(value);
                duplicatehash[key]++;
            } 
            else if (curr.keys[1] == key) 
            {
                curr.values[1].addFront(value);
                duplicatehash[key]++;
            } 
        }
    }

    void insert4Node(Node &curr, keytype key, valuetype value)
    {
        //Check to see if the key is the same as the middle key: if it is, add the value to the middle value
        if (key == curr.keys[1]) 
        {
            curr.values[1].addFront(value);
            duplicatehash[key]++;
            return;
        }
        //Everything else should be covered by the 2-node and 3-node cases

        cout << "Splitting 4-node " << endl;
        //Split the 4-node into two 2-nodes and promote the middle key to the parent
        Node *newNode = new Node();
        Node *newNode2 = new Node();

        //Define the types of the new nodes
        newNode->type = 2;
        newNode2->type = 2;

        

        //Store the middle key of the 4-node 
        keytype middleKey = curr.keys[1];

        //Store the middle value of the 4-node
        valuetype middleValue = curr.values[1][0];

        //Erase the middle key and value from the 4-node
        curr.keys[1] = curr.keys[2];
        curr.values[1] = curr.values[2];

        //newNode gets the 2 smallest children of the 4-node
        newNode->children[0] = curr.children[0];
        newNode->children[1] = curr.children[1];

        //newNode2 gets the 2 largest children of the 4-node
        newNode2->children[0] = curr.children[2];
        newNode2->children[1] = curr.children[3];

        //Split the now 3-node into two 2-nodes
        newNode->keys[0] = curr.keys[0];
        newNode->values[0] = curr.values[0];
        newNode2->keys[0] = curr.keys[1];
        newNode2->values[0] = curr.values[1];

        
        

        //Find the place to insert the middle key and value in the parent
        if (curr.parent == nullptr) 
        {
            Node *newRoot = new Node();
            newRoot->keys[0] = middleKey;
            newRoot->values[0].addFront(middleValue);
            newRoot->children[0] = newNode;
            newRoot->children[1] = newNode2;
            newNode->parent = newRoot;
            newNode2->parent = newRoot;
            root = newRoot;
        }

        else if (curr.parent->type == 2) 
        {
            if (middleKey < curr.parent->keys[0]) 
            {
                curr.parent->keys[1] = curr.parent->keys[0];
                curr.parent->values[1] = curr.parent->values[0];
                curr.parent->keys[0] = middleKey;
                curr.parent->values[0].addFront(middleValue);
                curr.parent->children[2] = curr.parent->children[1];
                curr.parent->children[0] = newNode;
                curr.parent->children[1] = newNode2;
                 //Define the parent of the new nodes
                newNode->parent = curr.parent;
                newNode2->parent = curr.parent;
                
                curr.parent->type = 3;
            } 
            else 
            {
                curr.parent->keys[1] = middleKey;
                curr.parent->values[1].addFront(middleValue);
                curr.parent->children[1] = newNode;
                curr.parent->children[2] = newNode2;
                 //Define the parent of the new nodes
                newNode->parent = curr.parent;
                newNode2->parent = curr.parent;
                        
                curr.parent->type = 3;
            }
        } 
        else if (curr.parent->type == 3) 
        {
            if (middleKey < curr.parent->keys[0]) 
            {
                curr.parent->keys[2] = curr.parent->keys[1];
                curr.parent->values[2] = curr.parent->values[1];
                curr.parent->keys[1] = curr.parent->keys[0];
                curr.parent->values[1] = curr.parent->values[0];
                curr.parent->keys[0] = middleKey;
                curr.parent->values[0].addFront(middleValue);
                curr.parent->children[3] = curr.parent->children[2];
                curr.parent->children[2] = curr.parent->children[1];
                curr.parent->children[0] = newNode;
                curr.parent->children[1] = newNode2;
                 //Define the parent of the new nodes
                newNode->parent = curr.parent;
                newNode2->parent = curr.parent;
                curr.parent->type = 4;
            } 
            else if (middleKey > curr.parent->keys[0] && middleKey < curr.parent->keys[1]) 
            {
                curr.parent->keys[2] = curr.parent->keys[1];
                curr.parent->values[2] = curr.parent->values[1];
                curr.parent->keys[1] = middleKey;
                curr.parent->values[1].addFront(middleValue);
                curr.parent->children[3] = curr.parent->children[2];
                curr.parent->children[1] = newNode;
                curr.parent->children[2] = newNode2;
                //Define the parent of the new nodes
                newNode->parent = curr.parent;
                newNode2->parent = curr.parent;
                curr.parent->type = 4;
            } 
            else 
            {
                curr.parent->keys[2] = middleKey;
                curr.parent->values[2].addFront(middleValue);
                curr.parent->children[2] = newNode;
                curr.parent->children[3] = newNode2;
                //Define the parent of the new nodes
                newNode->parent = curr.parent;
                newNode2->parent = curr.parent;
                curr.parent->type = 4;
            }
        }

       

        //Set the parent pointers of the new nodes
        if (curr.children[0]) curr.children[0]->parent = newNode;
        if (curr.children[1]) curr.children[1]->parent = newNode;
        if (curr.children[2]) curr.children[2]->parent = newNode2;
        if (curr.children[3]) curr.children[3]->parent = newNode2;



        //Insert the key and value into the appropriate 2-node
        //If the key is less than the middle key, insert into the left 2-node
        if (key < middleKey) 
        {
            insert2Node(*newNode, key, value);
        }
        //If the key is greater than the middle key, insert into the right 2-node
        else 
        {
            insert2Node(*newNode2, key, value);
        }
        

        
        

        


        

    }

    // Helper function to print a node and its children (for debugging)
    void printNodeStructure(Node* node, int depth = 0) {
        if (node == nullptr) return;
        string indent(depth * 4, ' '); // Create an indent based on the depth of the node
        cout << indent << "Node keys: ";
        for (int i = 0; i < node->type - 1; ++i) {
            cout << node->keys[i] << " ";
        }
        cout << "\n";
        for (int i = 0; i < node->type; ++i) {
            printNodeStructure(node->children[i], depth + 1); // Recursively print children
        }
    }

    //Print the tree inorder
    void inorder() 
    {
        printf("Inorder: ");
        inorder(root);
        cout << endl;
    }
   
    void inorder(Node* node) 
    {
        if (node == nullptr) 
            return;  // Base case: empty subtree

        // In a 2-4 tree, nodes can have between 2 and 4 children and 1 to 3 keys
        // The number of keys in a node is always one less than the number of children

        // First, visit the leftmost child
        inorder(node->children[0]);

        // Then, process the keys and in-between children
        for (int i = 0; i < node->type - 1; i++) 
        {
            // Print the ith key
            cout << node->keys[i] << " ";
            // Visit the ith+1 child which lies between the ith and (i+1)th keys
            inorder(node->children[i+1]);
        }
    }

    // Public function to call preorder traversal
    void preorder() 
    {
        preorder(root);  // Call the private helper function starting at the root
        cout << endl;  // End the line after printing all keys
    }

    
    // Recursive helper function for preorder traversal
    void preorder(Node* node) 
    {
        if (node == nullptr) 
            return;  // Base case: empty subtree

        // Process the current node's keys
        for (int i = 0; i < node->type - 1; i++) 
        {
            cout << node->keys[i] << " ";
        }
        cout << "\n";  // Print a newline after the keys of the node

        // Then, visit each child from left to right
        for (int i = 0; i < node->type; i++) 
        {
            preorder(node->children[i]);
        }
    }
};

