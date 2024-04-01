#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

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
        values[0] = CircularDynamicArray<valuetype>();
        values[1] = CircularDynamicArray<valuetype>();
        values[2] = CircularDynamicArray<valuetype>();

        //4 child pointers
        Node *children[4];

        //Pointer to the parent
        Node *parent;

        //int type {2,3,4}, 2 is 2-node, 3 is 3-node, 4 is 4-node
        int type = 2;

        //Subtree size
        int subtreeSize = 1;
    }
public:
    //Default constructor
    two4Tree() 
    {
        root = nullptr;
    }

    two4Tree(keytype keys[], valuetype values[], int size) 
    {
        root = nullptr;
        for (int i = 0; i < size; i++) {
            insert(keys[i], values[i]);
        }
    }

    //Destructor
    ~two4Tree() 
    {
        clear(root);
    }

    //Copy constructor
    two4Tree(const two4Tree &other) 
    {
        root = copy(other.root, nullptr);
    }

    //Copy assignment operator
    two4Tree &operator=(const two4Tree &other) 
    {
        if (this != &other) 
        {
            clear(root);
            root = copy(other.root, nullptr);
        }
        return *this;
    }

    void insert(keytype key, valuetype value) 
    {
        
    }
       
   
};

/*
int main() {
    two4Tree<int, std::string> tree;

    // Insert some nodes with values
    tree.insert(15, "Apple");
    tree.insert(10, "Banana");
    tree.insert(20, "Cherry");
    tree.insert(25, "Date");
    tree.insert(8, "Elderberry");
    tree.insert(12, "Fig");
    tree.insert(15, "Grape");

    // Print the tree in-order
    std::cout << "Tree in-order after insertions:" << std::endl;
    tree.printInOrder();
    std::cout << std::endl;

    // Test insertions that require node splits
    tree.insert(30, "Honeydew");
    tree.insert(35, "Kiwi");
    tree.insert(40, "Lemon");
    
    // Print the tree in-order after more insertions
    std::cout << "Tree in-order after more insertions:" << std::endl;
    tree.printInOrder();
    std::cout << std::endl;

    return 0;
};
*/


/*
// Insert method implementation
void insert(keytype k, valuetype v) {
    if (!root) {
        root = new Node();
        root->keys[0] = k;
        root->values[0].addFront(v);
        root->type = 2; // Node becomes 2-node since it has one key
        return;
    }

    // Start from the root and move down the tree to find the correct position
    Node *current = root;
    Node *parent;
    while (current) {
        // Check for duplicate keys
        for (int i = 0; i < current->type - 1; ++i) {
            if (current->keys[i] == k) {
                current->duplicates[i]++;
                current->values[i].addFront(v); // Add the new value to the circular dynamic array
                return; // Finish insertion as the key is a duplicate
            }
        }

        parent = current;
        // Decide the child node to move to
        int i;
        for (i = 0; i < current->type - 1; ++i) {
            if (k < current->keys[i]) {
                break;
            }
        }
        current = current->children[i];
    }

    // Perform the insertion into a leaf node
    // Since we reached a leaf, parent cannot be null
    insertNonFull(parent, k, v);
}

// Utility function to insert a new key and value in a non-full node
void insertNonFull(Node *x, keytype k, valuetype v) {
    // Initialize i to the rightmost index
    int i = x->type - 2;

    // If x is a leaf node
    if (x->children[0] == nullptr) {
        // Find the location of the new key to be inserted and move all
        // greater keys one space ahead
        while (i >= 0 && x->keys[i] > k) {
            x->keys[i + 1] = x->keys[i];
            x->values[i + 1] = x->values[i]; // Also move the values
            i--;
        }

        // Insert the new key at the found location
        x->keys[i + 1] = k;
        x->values[i + 1].clear();
        x->values[i + 1].addFront(v);
        x->type++;

        // Split the parent node if necessary
        if (x->type == 5) {
            splitChild(x->parent, findChildIndex(x->parent, x));
        }
    } else { // If x is not a leaf, find the child which is going to have the new key
        while (i >= 0 && x->keys[i] > k) {
            i--;
        }
        i++; // Move to the child that is going to have the new key
        if (x->children[i]->type == 4) { // Split the child if it is full

        Pick up from here 
        

*/