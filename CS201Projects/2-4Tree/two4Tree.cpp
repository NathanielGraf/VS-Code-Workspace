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

    // Add an element at the end
    void addEnd(elmtype v)
    {
        if (sz == cap)
        {
            resize(cap * 2);
        }
        back = (front + sz) % cap; // Correctly calculate back considering the circular nature
        arr[back] = v;
        sz++; // Increment size after adding the element
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
            root->values[0].addEnd(value);

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

        if (key == "M") 
        {
            cout << "M" << endl;
        }


        //cout << "Inserting into 2-node " << endl;
        if (key < curr.keys[0]) 
        {
            if (curr.children[0] == nullptr) 
            {
                curr.keys[1] = curr.keys[0];
                curr.values[1] = curr.values[0];
                curr.keys[0] = key;
                curr.values[0].addEnd(value);
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
                curr.values[1].addEnd(value);
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
            curr.values[0].addEnd(value);
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
                curr.values[0].addEnd(value);
                
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
                curr.values[1].addEnd(value);

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
                curr.values[2].addEnd(value);

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
                curr.values[0].addEnd(value);
                duplicatehash[key]++;
            } 
            else if (curr.keys[1] == key) 
            {
                curr.values[1].addEnd(value);
                duplicatehash[key]++;
            } 
        }
    }

    void insert4Node(Node &curr, keytype key, valuetype value)
    {
        //Check to see if the key is the same as the middle key: if it is, add the value to the middle value
        if (key == curr.keys[1]) 
        {
            curr.values[1].addEnd(value);
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
            newRoot->values[0].addEnd(middleValue);
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
                curr.parent->values[0].addEnd(middleValue);
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
                curr.parent->values[1].addEnd(middleValue);
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
                curr.parent->values[0].addEnd(middleValue);
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
                curr.parent->values[1].addEnd(middleValue);
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
                curr.parent->values[2].addEnd(middleValue);
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

    void postorder() 
    {
        postorder(root);  // Call the private helper function starting at the root
        cout << endl;  // End the line after printing all keys
    }

    // Recursive helper function for postorder traversal
    void postorder(Node* node) 
    {
        if (node == nullptr) 
            return;  // Base case: empty subtree

        // First, visit each child from left to right
        for (int i = 0; i < node->type; i++) 
        {
            postorder(node->children[i]);
        }

        // Then, process the current node's keys
        for (int i = 0; i < node->type - 1; i++) 
        {
            cout << node->keys[i] << " ";
        }
        cout << "\n";  // Print a newline after the keys of the node
    }

    //Return a pointer to the first value in the CDA of values for the key
    valuetype* search(keytype k)
    {
        Node* node = searchNode(root, k);
        if (node == nullptr) 
        {
            return NULL;
        }
        else if (node->keys[0] == k) 
        {
            return &node->values[0][0];
        } 
        else if (node->keys[1] == k) 
        {
            return &node->values[1][0];
        } 
        else if (node->keys[2] == k) 
        {
            return &node->values[2][0];
        }
        else
        {
            return NULL;
        }

    }

    //Search for a key in the tree and return a pointer to the node containing the key
    Node* searchNode(Node* node, keytype k) 
    {
        if (node == nullptr) 
        {
            return nullptr;
        }
        for (int i = 0; i < node->type - 1; i++) 
        {
            if (k == node->keys[i]) 
            {
                return node;
            } 
            else if (k < node->keys[i]) 
            {
                return searchNode(node->children[i], k);
            }
        }
        return searchNode(node->children[node->type - 1], k);
    }

    /*





    //Stuff for remove:::
    
    void removeValueFromNode(Node &node, keytype k) {
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node.type - 1; ++i) {
            if (node.keys[i] == k) {
                index = i;
                break;
            }
        }
        // If the key is not found, return
        if (index == -1) return;
        // Remove the value from the CircularDynamicArray
        node.values[index].delFront();
        // If the CDA is empty, remove the key from the node
        //Is length working properly on the CDA?
        if (node.values[index].length() == 0) {
            for (int i = index; i <= node.type - 2; ++i) {
                node.keys[i] = node.keys[i + 1];
                node.values[i] = node.values[i + 1];
            }
            node.keys[node.type - 2] = keytype();
            node.values[node.type - 2] = CircularDynamicArray<valuetype>();
            node.type--;
        }
    }

    bool isLeaf(Node* node) {
        return node->children[0] == nullptr;
    }

    //Remove a key from the tree and return 1, if the key is not in the tree, return 0.
    //If more than one copy of the key is in the tree, remove one copy from the duplicate map,
    //Delete the front value in the CDA of values for the key

    //Use predecessor to replace the key if it is an internal node
    
    remove(keytype k) {

        // Initial search for the node containing the key k
        Node* node = searchNode(root, k); // You need to implement searchNode function.
        if (!node) return 0; // Key not found in the tree.

        // Check if the key has duplicates.
        if (duplicatehash[k] > 1) {
            // Simply remove one instance of the key.
            removeValueFromNode(*node, k); // You need to implement removeValueFromNode function.
            duplicatehash[k]--;

            cout << "Tree structure after deleting key: " << k << "\n";
            printNodeStructure(root);
            cout << "---------------------------------\n";

            return 1;
        }

        // Key is unique. Check if it's a leaf or internal node.
        if (isLeaf(node)) {
            // Remove the key from the leaf node
            removeValueFromNode(*node, k);

            //If we have gotten to here the node should not be a 2 node, because we should have merged on the way down.

            // Balance the tree if necessary (handle underflow)
            //balanceTreeAfterRemoval(node); // You need to implement balanceTreeAfterRemoval function.
        } else {
            // If it's an internal node, find the predecessor (or successor).
            Node* predecessorNode = getPredecessorNode(node, k); // You need to implement getPredecessorNode function.
            keytype predecessorKey = findLargestKey(predecessorNode);
            // Swap the key with its predecessor.
            swapKeys(node, k, predecessorNode, predecessorKey); // You need to implement swapKeys function.
            // Remove the predecessor key now at the leaf level.
            removeValueFromNode(*predecessorNode, predecessorKey);
            // Balance the tree if necessary (handle underflow)
            balanceTreeAfterRemoval(predecessorNode);
        }

        cout << "Tree structure after deleting key: " << k << "\n";
        printNodeStructure(root);
        cout << "---------------------------------\n";

        return 1; // Success
    }

    Node* getPredecessorNode(Node* node, keytype key) {
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node->type - 1; ++i) {
            if (node->keys[i] == key) {
                index = i;
                break;
            }
        }
        // Go to the rightmost child of the left subtree
        Node* predecessorNode = node->children[index];
        while (predecessorNode->children[predecessorNode->type - 1] != nullptr) {
            predecessorNode = predecessorNode->children[predecessorNode->type - 1];
        }
        return predecessorNode;
    }

    void swapKeys(Node* node, keytype key, Node* predecessorNode, keytype predecessorKey) {
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node->type - 1; ++i) {
            if (node->keys[i] == key) {
                index = i;
                break;
            }
        }
        // Replace the key with its predecessor
        node->keys[index] = predecessorKey;
        // Copy the predecessor's value to the node
        node->values[index] = predecessorNode->values[predecessorNode->type - 2];

        //No need to update the predecessor node, as it will be removed later
        
    }

    

    // Function to balance the tree after the removal of a key, handling underflows.
    void balanceTreeAfterRemoval(Node* node) {
        // Check if the node is a 2-node and underflows
        while (node != root && node->type == 1) {
            int childIndex = getChildIndex(node->parent, node); // Get index of child in parent node
            Node* sibling;
            bool isLeftSibling = (childIndex > 0); // Check if there is a left sibling

            // Check for a non-empty left sibling first, cannot be a 2 node (underflow)
            if (isLeftSibling && node->parent->children[childIndex - 1]->type > 2) {
                sibling = node->parent->children[childIndex - 1];
                rotateRight(node->parent, childIndex - 1);
            } 
            // Check for a non-empty right sibling next, cannot be 2 node for underflow
            else if (childIndex < node->parent->type - 1 && node->parent->children[childIndex + 1]->type > 2) {
                sibling = node->parent->children[childIndex + 1];
                rotateLeft(node->parent, childIndex);
            }
            // If siblings are also 2-nodes, merge with one of them
            else {
                if (isLeftSibling) { // Merge with left sibling
                    sibling = node->parent->children[childIndex - 1];
                    mergeNodes(sibling, node, childIndex - 1);
                } else { // Merge with right sibling
                    sibling = node->parent->children[childIndex + 1];
                    mergeNodes(node, sibling, childIndex);
                }
            }

            // After merging, check if parent is underflowing
            node = node->parent;
        }

        // If root is a 2-node with no children, make its child the new root
        if (root->type == 2 && root->children[0]) {
            Node* newRoot = root->children[0];
            newRoot->parent = nullptr;
            delete root;
            root = newRoot;
        }
    }

    // Helper function to get the index of the child node in its parent's children array
    int getChildIndex(Node* parent, Node* child) {
        for (int i = 0; i <= parent->type; ++i) {
            if (parent->children[i] == child) {
                return i;
            }
        }
        return -1; // Should not happen if tree is well-formed
    }

    // Rotation to the right
    void rotateRight(Node* parent, int leftChildIndex) {
        Node* leftSibling = parent->children[leftChildIndex];
        Node* rightChild = parent->children[leftChildIndex + 1];

        // Move a key from the left sibling to the right child
        rightChild->keys[1] = rightChild->keys[0]; // Shift existing key
        rightChild->values[1] = rightChild->values[0];
        rightChild->keys[0] = parent->keys[leftChildIndex]; // Move parent key down
        rightChild->values[0] = leftSibling->values[leftSibling->type - 2]; // Move sibling value down

        // Move a key from the left sibling to the parent
        parent->keys[leftChildIndex] = leftSibling->keys[leftSibling->type - 2];

        // Adjust children pointers if necessary
        if (leftSibling->children[leftSibling->type]) {
            rightChild->children[2] = rightChild->children[1]; // Shift existing child
            rightChild->children[1] = rightChild->children[0];
            rightChild->children[0] = leftSibling->children[leftSibling->type]; // Move sibling's child
            leftSibling->children[leftSibling->type] = nullptr;
            rightChild->children[0]->parent = rightChild;
        }

        // Update the size of the nodes
        leftSibling->type--;
        rightChild->type++;

        // Clean up the moved key and value from the left sibling
        leftSibling->keys[leftSibling->type - 1] = keytype(); // Default-initialized keytype
        leftSibling->values[leftSibling->type - 1].clear(); // Clear the CDA
    }


    void rotateLeft(Node* parent, int rightChildIndex) {
        Node* rightSibling = parent->children[rightChildIndex];
        Node* leftChild = parent->children[rightChildIndex - 1];

        // Move a key from the right sibling to the left child
        leftChild->keys[leftChild->type - 1] = parent->keys[rightChildIndex - 1]; // Move parent key down
        leftChild->values[leftChild->type - 1] = rightSibling->values[0]; // Move sibling value down

        // Move a key from the right sibling to the parent
        parent->keys[rightChildIndex - 1] = rightSibling->keys[0];

        // Adjust children pointers if necessary
        if (rightSibling->children[0]) {
            leftChild->children[leftChild->type] = rightSibling->children[0]; // Move sibling's child
            rightSibling->children[0] = rightSibling->children[1]; // Shift sibling's children
            rightSibling->children[1] = rightSibling->children[2];
            rightSibling->children[2] = rightSibling->children[3];
            rightSibling->children[3] = nullptr;
            leftChild->children[leftChild->type]->parent = leftChild;
        }

        // Shift the keys and values in the right sibling to remove the moved key and value
        for (int i = 0; i < rightSibling->type - 2; i++) {
            rightSibling->keys[i] = rightSibling->keys[i + 1];
            rightSibling->values[i] = rightSibling->values[i + 1];
        }

        // Update the size of the nodes
        leftChild->type++;
        rightSibling->type--;

        // Clean up the moved key and value from the right sibling
        rightSibling->keys[rightSibling->type - 1] = keytype(); // Default-initialized keytype
        rightSibling->values[rightSibling->type - 1].clear(); // Clear the CDA
    }


    void mergeNodes(Node* leftNode, Node* rightNode, int mergeIndex) {
        // 'mergeIndex' is the index of the left node in the parent's children array
        Node* parent = leftNode->parent;
        int parentKeyIndex = mergeIndex;

        // Move the parent's key down to the left node
        leftNode->keys[leftNode->type - 1] = parent->keys[parentKeyIndex];
        leftNode->values[leftNode->type - 1] = rightNode->values[0];  // Assuming rightNode has only one value

        // Move keys and values from the right node to the left node
        for (int i = 0; i < rightNode->type - 1; ++i) {
            leftNode->keys[leftNode->type + i] = rightNode->keys[i];
            leftNode->values[leftNode->type + i] = rightNode->values[i];
        }

        // If rightNode has children, move them to leftNode
        if (rightNode->children[0]) {
            for (int i = 0; i <= rightNode->type; ++i) {
                leftNode->children[leftNode->type + i] = rightNode->children[i];
                if (rightNode->children[i]) {
                    rightNode->children[i]->parent = leftNode;
                }
            }
        }

        // Update the type of the left node
        leftNode->type += rightNode->type;

        // Shift keys and children in the parent node to fill the gap
        for (int i = parentKeyIndex; i < parent->type - 2; ++i) {
            parent->keys[i] = parent->keys[i + 1];
            parent->children[i + 1] = parent->children[i + 2];
        }

        // Clean up the parent node
        parent->keys[parent->type - 2] = keytype(); // Default-initialized keytype
        parent->children[parent->type - 1] = nullptr;

        // Update the type of the parent node
        parent->type--;

        // Delete the right node as it has been merged into the left node
        delete rightNode;

        // If the parent is the root and now has no keys, the left node becomes the new root
        if (parent == root && parent->type == 1) {
            root = leftNode;
            root->parent = nullptr;
            delete parent;
        }
    }


    */

   
   /**/
        

    int containsKeyInNode(Node* node, keytype k) {
        if (node == nullptr) return false;  // If node is null, key is not present.
        for (int i = 0; i < node->type - 1; ++i) {
                if (node->keys[i] == k) {
                    return i;
                }
            }
            return -1;
    }

    void removeValueFromNode(Node &node, keytype k) {

        if (node.type == 2)
        {
            cout << "Attempted Removal of Key from Type 2 Node" << endl;
            return;
        }
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node.type - 1; ++i) {
            if (node.keys[i] == k) {
                index = i;
                break;
            }
        }
        // If the key is not found, return
        if (index == -1) return;
        // Remove the value from the CircularDynamicArray
        node.values[index].delFront();
        // If the CDA is empty, remove the key from the node
        //Is length working properly on the CDA?
        if (node.values[index].length() == 0) {
            for (int i = index; i <= node.type - 2; ++i) {
                node.keys[i] = node.keys[i + 1];
                node.values[i] = node.values[i + 1];
            }
            node.keys[node.type - 2] = keytype();
            node.values[node.type - 2] = CircularDynamicArray<valuetype>();
            node.type--;
        }
    }

    Node* getPredecessorNode(Node* node, keytype key) {
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node->type - 1; ++i) {
            if (node->keys[i] == key) {
                index = i;
                break;
            }
        }
        // Go to the rightmost child of the left subtree
        Node* predecessorNode = node->children[index];
        while (predecessorNode->children[predecessorNode->type - 1] != nullptr) {
            predecessorNode = predecessorNode->children[predecessorNode->type - 1];
        }
        return predecessorNode;
    }

    Node* getSuccessorNode(Node* node, keytype key) {
        // Find the index of the key in the node
        int index = -1;
        for (int i = 0; i < node->type - 1; ++i) {
            if (node->keys[i] == key) {
                index = i;
                break;
            }
        }
        // Go to the leftmost child of the right subtree
        Node* successorNode = node->children[index + 1];
        while (successorNode->children[0] != nullptr) {
            successorNode = successorNode->children[0];
        }
        return successorNode;
    }

   

    int remove(keytype k) {

        //Handle special case of deleting only key, as we can't rectify solo root of type 2. 
        if (root->type == 2 && root->children[0] == nullptr && root->keys[0] == k)
        {
            root = nullptr;
            return 1;
        }
        
        //Create current node pointer
        Node* curr = root;
        
        //Check if k is in the node: 
        int index = containsKeyInNode(curr, k);

        //If k is in the node, the node is a leaf, and the type is 3 or 4, remove key and value
        if (index != -1 && curr->children[0] == nullptr && (curr->type == 3 || curr->type == 4))
        {
            removeValueFromNode(*curr, k);
            return 1;
        }

        //If k is in the node and the node is an internal node, and the type of the left child is 3 or 4, get the predecessor and swap the key with the predecessor
        else if (index != -1 && curr->children[0] != nullptr && (curr->children[index]->type == 3 || curr->children[index]->type == 4))
        {
            Node* predecessorNode = getPredecessorNode(curr, k);
            
            //Find the largest key in the predecessor node
            keytype predecessorKey = predecessorNode->keys[predecessorNode->type - 2];

            //Save the pred value to be replaced
            CircularDynamicArray<valuetype> predValues = predecessorNode->values[predecessorNode->type - 2];

            //Replace the predecessor key with the key
            predecessorNode->keys[predecessorNode->type - 2] = k;

            //Replace the predecessor value with the value
            predecessorNode->values[predecessorNode->type - 2] = curr->values[index];

            //Replace the key with the predecessor
            curr->keys[index] = predecessorKey;

            //Replace the value with the pred value
            curr->values[index] = predValues;

            //Replace the key with the predecessor
            curr->keys[index] = predecessorKey;

            //Call remove on the key
            remove(k);
        }

        //If k is in the node and the node is an internal node, and the type of the right child is 3 or 4, get the successor and swap the key with the successor
        else if (index != -1 && curr->children[0] != nullptr && (curr->children[index + 1]->type == 3 || curr->children[index + 1]->type == 4))
        {
            Node* successorNode = getSuccessorNode(curr, k);
            
            //Find the smallest key in the successor node
            keytype successorKey = successorNode->keys[0];

            //Save the succ value to be replaced
            CircularDynamicArray<valuetype> succValues = successorNode->values[0];

            //Replace the successor key with the key
            successorNode->keys[0] = k;

            //Replace the successor value with the value
            successorNode->values[0] = curr->values[index];

            //Replace the key with the successor
            curr->keys[index] = successorKey;

            //Replace the value with the succ value
            curr->values[index] = succValues;

            //Replace the key with the successor
            curr->keys[index] = successorKey;

            //Call remove on the key
            remove(k);
        }



            

        /*
        // Initial search for the node containing the key k, must make all nodes non-2 nodes on the way down
        Node* node = searchNodeMerge(root, k);


        if (!node) return 0; // Key not found in the tree.

        // Check if the key has duplicates.
        if (duplicatehash[k] > 1) {
            // Simply remove one instance of the key.
            removeValueFromNode(*node, k); // You need to implement removeValueFromNode function.
            duplicatehash[k]--;

            cout << "Tree structure after deleting key: " << k << "\n";
            printNodeStructure(root);
            cout << "---------------------------------\n";

            return 1;
        }

        // Key is unique. Check if it's a leaf or internal node.
        if (isLeaf(node)) {
            // Remove the key from the leaf node
            removeValueFromNode(*node, k);

            //If we have gotten to here the node should not be a 2 node, because we should have merged on the way down.

            // Balance the tree if necessary (handle underflow)
            //balanceTreeAfterRemoval(node); // You need to implement balanceTreeAfterRemoval function.
        } else {
            // If it's an internal node, find the predecessor (or successor).
            Node* predecessorNode = getPredecessorNode(node, k); // You need to implement getPredecessorNode function.
            keytype predecessorKey = findLargestKey(predecessorNode);
            // Swap the key with its predecessor.
            swapKeys(node, k, predecessorNode, predecessorKey); // You need to implement swapKeys function.
            // Remove the predecessor key now at the leaf level.
            removeValueFromNode(*predecessorNode, predecessorKey);
            // Balance the tree if necessary (handle underflow)
            balanceTreeAfterRemoval(predecessorNode);
        }

        cout << "Tree structure after deleting key: " << k << "\n";
        printNodeStructure(root);
        cout << "---------------------------------\n";

        return 1; // Success
    
    */
    }
    
};

