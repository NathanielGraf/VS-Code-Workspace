#include <iostream>

using namespace std;

class MyDynamicArray {
    private:
        int size, capacity, error;
        int *a;
    public:
        MyDynamicArray() 
        {
           capacity = 2;
           size = 0;
           error = 0;
           a = new int[capacity];
        }
        MyDynamicArray(int s) 
        {
            capacity = s;
            size = s;
            error = 0;
            a = new int[capacity];
        }
        int& operator[](int i)
        {
            if (i < 0 || i >= size) 
            {
                cout << "Out of bounds reference : " << i << endl;
                return error;
            }
            else 
            {
                error = 0;
                return a[i];
            }
        }
        void add(int v) 
        {
            if (size == capacity) 
            {
                int *b = new int[capacity * 2];
                for (int i = 0; i < size; i++) 
                {
                    b[i] = a[i];
                }
                delete[] a;
                a = b;
                capacity *= 2;
                cout << "Doubling to : " << capacity << endl;
            }
            a[size] = v;
            size++;
        }

        void del() {
            if (size > 0) {
                size--;
            }
            if (size <= capacity / 4) {
                int *b = new int[capacity / 2];
                for (int i = 0; i < size; i++) {
                    b[i] = a[i];
                }
                delete[] a;
                a = b;
                capacity /= 2;
                cout << "Reducing to : " << capacity << endl;
            }
        }

        int length() {
            return size;
        }
        void clear() {
            delete[] a;

            capacity = 2;
            size = 0;
            error = 0;
            a = new int[capacity];
        }

        MyDynamicArray& operator=(const MyDynamicArray& src) {

            //Create copy assignment operator
            cout << "In the copy assignment operator" << endl;

            if (this != &src) {
                delete[] a;

                capacity = src.capacity;
                size = src.size;
                error = src.error;
                a = new int[capacity];

                for (int i = 0; i < size; i++) {
                    a[i] = src.a[i];
                }
            }
            

            return *this;
        }
        
        MyDynamicArray(const MyDynamicArray & src) {
            cout << "In the copy constructor" << endl;

            capacity = src.capacity;
            size = src.size;
            error = src.error;
            a = new int[capacity];

            for (int i = 0; i < size; i++) {
                a[i] = src.a[i];
            }



        }

        ~MyDynamicArray() {
            cout << "In the destructor" << endl;

            delete[] a;

        }
};
