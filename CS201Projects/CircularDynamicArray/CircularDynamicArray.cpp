#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

template <typename elmtype>
class CircularDynamicArray
{
public:
    elmtype *arr;
    int size;
    int capacity;
    int front;
    int back;

    // Default Constructor
    CircularDynamicArray() 
    {
        size = 0;
        capacity = 2;
        front = 0;
        back = 0;
        arr = new elmtype[capacity];
    }
    
    //Constructor
    CircularDynamicArray(int s)
    {
        size = 0;
        capacity = s;
        front = 0;
        back = 0;
        arr = new elmtype[capacity];
    }

    // Destructor
    ~CircularDynamicArray()
    {
        delete[] arr;
    }

    // Copy Constructor
    CircularDynamicArray(const CircularDynamicArray &cda)
    {
        arr = new elmtype[cda.capacity];
        size = cda.size;
        capacity = cda.capacity;
        front = cda.front;
        back = cda.back;
        for (int i = 0; i < size; i++)
        {
            arr[(front + i) % capacity] = cda.arr[(cda.front + i) % cda.capacity];
        }
    }

    // Copy Assignment Operator
    CircularDynamicArray &operator=(const CircularDynamicArray &cda)
    {
        if (this != &cda)
        {
            delete[] arr;
            arr = new elmtype[cda.capacity];
            size = cda.size;
            capacity = cda.capacity;
            front = cda.front;
            back = cda.back;
            for (int i = 0; i < size; i++)
            {
                arr[(front + i) % capacity] = cda.arr[(cda.front + i) % cda.capacity];
            }
        }
        return *this;
    }

    // Subscript Operator
    elmtype &operator[](int i)
    {
        return arr[(front + i) % capacity]; // Consider the circular nature
    }

    // Add an element at the end
    void addEnd(elmtype v)
    {
        if (size == capacity)
        {
            resize(capacity * 2);
        }
        back = (front + size) % capacity; // Correctly calculate back considering the circular nature
        arr[back] = v;
        size++; // Increment size after adding the element
    }

    // Add an element at the front
    void addFront(elmtype v)
    {
        if (size == capacity)
        {
            resize(capacity * 2);
        }
        front = (front - 1 + capacity) % capacity; // Move front back one position, wrapping around if necessary
        arr[front] = v;
        size++; // Increment size after adding the element
    }

    void delEnd()
    {
        if (size == 0) // Check if the array is empty
        {
            cout << "Array is empty. No elements to remove from the end." << endl;
            return;
        }

        size--;
        back = (front + size) % capacity; // Update back index

        // Check if size is 25% or less of capacity
        if (size > 0 && size <= capacity / 4)
        {
            resize(capacity / 2); // Resize to half the current capacity
        }
    }

    
    void delFront()
    {
        if (size == 0) // Check if the array is empty
        {
            cout << "Array is empty. No elements to remove from the front." << endl;
            return;
        }

        front = (front + 1) % capacity; // Move front to the next element
        size--; // Decrease the size

        // Check if size is 25% or less of capacity
        if (size > 0 && size <= capacity / 4)
        {
            resize(capacity / 2); // Resize to half the current capacity
        }
    }

    int length()
    {
        return size;
    }

    int getcapacity()
    {
        return capacity;
    }

    void clear()
    {
        delete[] arr;
        size = 0;
        capacity = 2;
        front = 0;
        back = 0;
        arr = new elmtype[capacity];
    }

    // Method to find the k-th smallest element
    elmtype QSelect(int k) 
    {
        std::srand(1); // Seed the random number generator
        return quickSelect(0, size - 1, k);
    }

    // Method to sort the array
    void sort() {
        if (size <= 1) return; // Array is already sorted
        std::srand(std::time(nullptr)); // Seed the random number generator
        quicksort(0, size - 1);
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
        elmtype pivotValue = arr[(front + pivotIndex) % capacity];
        std::swap(arr[(front + pivotIndex) % capacity], arr[(front + right) % capacity]); // Move pivot to end
        int storeIndex = left;

        for (int i = left; i < right; i++) {
            if (arr[(front + i) % capacity] < pivotValue) {
                std::swap(arr[(front + i) % capacity], arr[(front + storeIndex) % capacity]);
                storeIndex++;
            }
        }

        std::swap(arr[(front + storeIndex) % capacity], arr[(front + right) % capacity]); // Move pivot to its final place
        return storeIndex;
    }

    int linearSearch(elmtype target) 
    {
        for (int i = 0; i < size; i++) 
        {
            if (arr[(front + i) % capacity] == target) 
            {
                return i; // Return the index of the target element
            }
        }
        return -1; // Return -1 if the target is not found
    }

    // Binary search method
    int binarySearch(elmtype target) 
    {
        if (size == 0) return -1; // Check if the array is empty

        int low = 0;
        int high = size - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            elmtype midValue = arr[(front + mid) % capacity];

            if (midValue == target) {
                return mid; // Target found
            } else if (midValue < target) {
                low = mid + 1; // Continue in the right half
            } else {
                high = mid - 1; // Continue in the left half
            }
        }

        return -1; // Target not found
    }


private:
    // Resize the array when it's full
    void resize(int newCapacity)
    {
        elmtype *temp = new elmtype[newCapacity];
        for (int i = 0; i < size; i++)
        {
            temp[i] = arr[(front + i) % capacity]; // Copy elements in circular order
        }
        delete[] arr;
        arr = temp;
        capacity = newCapacity;
        front = 0; // Reset front to 0
        back = size; // Update back based on the new size
    }

    // Utility method to perform the Quickselect algorithm
    elmtype quickSelect(int left, int right, int k) {
        if (left == right) { // If the list contains only one element,
            return arr[(front + left) % capacity]; // return that element
        }

        // Select a random pivotIndex between left and right
        int pivotIndex = left + std::rand() % (right - left + 1);
        pivotIndex = partition(left, right, pivotIndex);

        // The pivot is in its final sorted position
        if (k == pivotIndex) {
            return arr[(front + k) % capacity];
        } else if (k < pivotIndex) {
            return quickSelect(left, pivotIndex - 1, k);
        } else {
            return quickSelect(pivotIndex + 1, right, k);
        }
    }

    // Utility method to partition the elements in the array
    int partition(int left, int right, int pivotIndex) 
    {
        elmtype pivotValue = arr[(front + pivotIndex) % capacity];
        // Move pivot to the end
        std::swap(arr[(front + pivotIndex) % capacity], arr[(front + right) % capacity]);

        int storeIndex = left;
        for (int i = left; i < right; i++) {
            if (arr[(front + i) % capacity] < pivotValue) {
                std::swap(arr[(front + i) % capacity], arr[(front + storeIndex) % capacity]);
                storeIndex++;
            }
        }

        // Move pivot to its final place
        std::swap(arr[(front + right) % capacity], arr[(front + storeIndex) % capacity]);
        return storeIndex;
    }

    

};

int main() 
{
    CircularDynamicArray<int> cda;

    // Adding elements to trigger an increase in capacity
    cout << "Adding elements to the end to increase capacity:" << endl;
    for (int i = 1; i <= 8; ++i) {
        cda.addEnd(i);
        cout << "Added " << i << "; Size: " << cda.size << ", Capacity: " << cda.capacity << endl;
    }

    // Removing elements from the end to trigger a decrease in capacity
    cout << "\nRemoving elements from the end to decrease capacity:" << endl;
    for (int i = 0; i < 6; ++i) {
        cda.delEnd();
        cout << "Removed from end; Size: " << cda.size << ", Capacity: " << cda.capacity << endl;
    }

    // Adding elements to the front
    cout << "\nAdding elements to the front:" << endl;
    for (int i = 10; i <= 12; ++i) {
        cda.addFront(i);
        cout << "Added " << i << " to the front; Size: " << cda.size << ", Capacity: " << cda.capacity << endl;
    }

    // Removing elements from the front to further test resizing
    cout << "\nRemoving elements from the front to further test resizing:" << endl;
    while (cda.size > 0) {
        cda.delFront();
        cout << "Removed from front; Size: " << cda.size << ", Capacity: " << cda.capacity << endl;
    }

    int k = 3;

    // Adding elements to the end
    cout << "\nAdding elements to the end:" << endl;
    for (int i = 1; i <= 8; ++i) {
        cda.addEnd(i);
        cout << "Added " << i << " to the end; Size: " << cda.size << ", Capacity: " << cda.capacity << endl;
    }

    // Finding the k-th smallest element

    cout << "\nFinding the " << k << "-th smallest element:" << endl;

    cout << "The " << k << "-th smallest element is: " << cda.QSelect(k - 1) << endl;

    // Add unsorted elements to the array
    cda.addEnd(7);
    cda.addEnd(3);
    cda.addEnd(5);
    cda.addEnd(2);
    cda.addEnd(9);
    cda.addEnd(1);
    cda.addEnd(4);

    // Print the unsorted array
    cout << "Unsorted array:" << endl;
    for (int i = 0; i < cda.size; ++i) {
        cout << cda[i] << " ";
    }
    cout << endl;

    // Sort the array
    cda.sort();

    // Print the sorted array to verify the sort method works
    cout << "Sorted array:" << endl;
    for (int i = 0; i < cda.size; ++i) {
        cout << cda[i] << " ";
    }
    cout << endl;

    // Populate the array
    cda.addEnd(3);
    cda.addEnd(6);
    cda.addEnd(8);
    cda.addEnd(12);
    cda.addEnd(15);
    cda.addEnd(18);

    cda.sort(); // Sort the array

    // Display the array
    cout << "Array elements:" << endl;
    for (int i = 0; i < cda.size; ++i) {
        cout << cda[i] << " ";
    }
    cout << "\n";

    // Linear search test
    int target = 12;
    int index = cda.linearSearch(target);
    if (index != -1) {
        cout << "Linear Search: Found " << target << " at index " << index << ".\n";
    } else {
        cout << "Linear Search: " << target << " not found.\n";
    }

    // Binary search test (array should be sorted)
    target = 18;
    index = cda.binarySearch(target);
    if (index != -1) {
        cout << "Binary Search: Found " << target << " at index " << index << ".\n";
    } else {
        cout << "Binary Search: " << target << " not found.\n";
    }

    // Attempt to search for a value that is not in the array
    target = 20;
    index = cda.binarySearch(target); // Assuming the array is sorted
    if (index != -1) {
        cout << "Binary Search: Found " << target << " at index " << index << ".\n";
    } else {
        cout << "Binary Search: " << target << " not found.\n";
    }
    

    return 0;
}