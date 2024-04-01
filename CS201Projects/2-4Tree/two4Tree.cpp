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

    void delEnd()
    {
        if (sz == 0) // Check if the array is empty
        {
            cout << "Array is empty. No elements to remove from the end." << endl;
            return;
        }

        sz--;
        back = (front + sz) % cap; // Update back index

        // Check if size is 25% or less of capacity
        if (sz > 0 && sz <= cap / 4)
        {
            resize(cap / 2); // Resize to half the current capacity
        }
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

    // Method to sort the array
    void Sort() {
        if (sz <= 1) return; // Array is already sorted
        std::srand(1); // Seed the random number generator
        quicksort(0, sz - 1);
    }

    // Quicksort function
    void quicksort(int left, int right) {
        if (left < right) {
            int pivotIndex = partition(left, right); // Partition the array and get the pivot index
            quicksort(left, pivotIndex - 1); // Recursively apply quicksort to the left sub-array
            quicksort(pivotIndex + 1, right); // Recursively apply quicksort to the right sub-array
        }
    }

    // Partition function
    int partition(int left, int right) {
        int pivotIndex = left + std::rand() % (right - left + 1); // Choose a random pivot
        elmtype pivotValue = arr[(front + pivotIndex) % cap];
        std::swap(arr[(front + pivotIndex) % cap], arr[(front + right) % cap]); // Move pivot to end
        int storeIndex = left;

        for (int i = left; i < right; i++) {
            if (arr[(front + i) % cap] < pivotValue) {
                std::swap(arr[(front + i) % cap], arr[(front + storeIndex) % cap]);
                storeIndex++;
            }
        }

        std::swap(arr[(front + storeIndex) % cap], arr[(front + right) % cap]); // Move pivot to its final place
        return storeIndex;
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

    // Utility method to partition the elements in the array
    int partition(int left, int right, int pivotIndex) 
    {
        elmtype pivotValue = arr[(front + pivotIndex) % cap];
        // Move pivot to the end
        std::swap(arr[(front + pivotIndex) % cap], arr[(front + right) % cap]);

        int storeIndex = left;
        for (int i = left; i < right; i++) {
            if (arr[(front + i) % cap] < pivotValue) {
                std::swap(arr[(front + i) % cap], arr[(front + storeIndex) % cap]);
                storeIndex++;
            }
        }

        // Move pivot to its final place
        std::swap(arr[(front + right) % cap], arr[(front + storeIndex) % cap]);
        return storeIndex;
    }

};


template <typename keytype, typename valuetype>
class two4Tree {
private:
    class Node {
    public:
        vector<keytype> keys; // Can store up to 3 keys
        vector<CircularDynamicArray<valuetype>> values; // Use CircularDynamicArray to store values
        vector<Node*> children; // Pointers to child nodes
        Node* parent;

        // Node Constructor
        Node() : parent(nullptr) {
            // Assume each key has a corresponding CircularDynamicArray in values
            for (int i = 0; i < 3; ++i) {
                values.push_back(CircularDynamicArray<valuetype>());
            }
        }

        // Check if the node is a leaf
        bool isLeaf() const {
            return children.empty();
        }

        // Method to print a node's keys and values
        void printNode() const {
            for (size_t i = 0; i < keys.size(); ++i) {
                cout << keys[i] << ": ";
                values[i].printArray(); // Assuming CircularDynamicArray has a printArray() method
                if (i < keys.size() - 1) {
                    cout << " | "; // Separator between keys in the same node
                }
            }
        }

        bool containsKey(const keytype& key) {
            return std::find(keys.begin(), keys.end(), key) != keys.end();
        }

        void insertNonFull(const keytype& key, const valuetype& value) {
            if (isLeaf()) {
                auto it = lower_bound(keys.begin(), keys.end(), key);
                if (it != keys.end() && *it == key) {
                    // Key found, add value to the existing key's values
                    int index = it - keys.begin();
                    values[index].addEnd(value);
                } else {
                    // Key not found, insert new key and value
                    keys.insert(it, key);
                    values.insert(values.begin() + (it - keys.begin()), CircularDynamicArray<valuetype>());
                    values[it - keys.begin()].addEnd(value);
                }
            } else {
                // Find the child which is going to have the new key
                int i = keys.size() - 1;
                while (i >= 0 && keys[i] > key) i--;
                // Check if the found child is full
                if (children[i+1]->keys.size() == 3) {
                    splitChild(i+1, children[i+1]);
                    if (keys[i+1] < key) i++;
                }
                children[i+1]->insertNonFull(key, value);
            }
        }

        void splitChild(int i, Node* y) {
            // Split the child y of this node. i is index of y in child array children.
            // Node y must be full when this function is called

            // Create a new node which is going to store (t-1) keys of y
            Node* z = new Node();
            z->parent = y->parent;

            // Copy the last (t-1) keys and children from y to z
            z->keys.insert(z->keys.end(), y->keys.begin() + 2, y->keys.end());
            z->values.insert(z->values.end(), y->values.begin() + 2, y->values.end());
            y->keys.resize(2);
            y->values.resize(2);

            if (!y->isLeaf()) {
                z->children.insert(z->children.end(), y->children.begin() + 3, y->children.end());
                y->children.resize(3);
            }

            // Insert a new key in the parent node and update parent's children
            keys.insert(keys.begin() + i, y->keys[2]);
            values.insert(values.begin() + i, y->values[2]);
            children.insert(children.begin() + (i + 1), z);

            // Remove the median key from y
            y->keys.pop_back();
            y->values.pop_back();
        }


        //Other node methods
    };

    Node* root;

    // Helper function for in-order traversal
    void printInOrderHelper(Node* node) const {
        if (node == nullptr) return;

        // If the node is a leaf, just print its keys and values
        if (node->isLeaf()) {
            node->printNode();
            cout << endl;
            return;
        }

        // In-order traversal
        for (size_t i = 0; i < node->keys.size(); ++i) {
            // Visit left child
            if (i < node->children.size()) {
                printInOrderHelper(node->children[i]);
            }
            // Visit node's key and value
            cout << node->keys[i] << ": ";
            node->values[i].printArray(); // Assuming CircularDynamicArray has a printArray() method
            cout << endl;
        }
        // Visit rightmost child
        printInOrderHelper(node->children[node->children.size() - 1]);
    }

    void clear(Node* node) {
        if (node == nullptr) return;

        for (Node* child : node->children) {
            clear(child);
        }
        delete node;
    }






public:
    two4Tree() : root(nullptr) {}

    ~two4Tree() 
    {
        clear(root);
    }

    void insert(const keytype& key, const valuetype& value) {
        if (root == nullptr) {
            root = new Node();
            root->keys.push_back(key);
            root->values.emplace_back(CircularDynamicArray<valuetype>());
            root->values.back().addEnd(value);
        } else {
            if (root->keys.size() == 3) {
                Node* newNode = new Node();
                newNode->children.push_back(root);
                root->parent = newNode;
                newNode->splitChild(0, root);
                int i = (newNode->keys[0] < key) ? 1 : 0;
                newNode->children[i]->insertNonFull(key, value);
                root = newNode;
            } else {
                root->insertNonFull(key, value);
            }
        }
    }

    // Method to print the tree in-order
    void printInOrder() const {
        printInOrderHelper(root);
    }
};

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
}

