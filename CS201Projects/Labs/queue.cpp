using namespace std;
#include <iostream>
#include <string>

template <typename T>
class queue
{
public:
    T *arr;
    int size;
    int capacity;
    int front = 0;
    int back = 0;

    queue() 
    {
        //Create array of capacity 10, size of 0
        arr = new T[10];
        int size = 0;
        int capacity = 10;
    }
    queue(int s)
    {
        //Create array of capacity s, size of 0
        arr = new T[s];
        int size = 0;
        int capacity = s;
    }
    void enqueue(T x)
    {
        
        arr[back] = x;
        //cout << "Enqueue: " << arr[back] << endl;
        size++;
        back++;
    }
    
    T dequeue()
    {
        T temp = arr[front];
        //cout << "Dequeue: " << arr[front] << endl;
        front++;
        size--;
        return temp;
        
    }
    T operator[](int i)
    {
        return arr[i];
    }
    ~queue()
    {
        delete[] arr;
    }

    queue(const queue &q)
    {
        arr = new T[q.capacity];
        size = q.size;
        capacity = q.capacity;
        front = q.front;
        back = q.back;
        for (int i = 0; i < size; i++)
        {
            arr[i] = q.arr[i];
        }
    }

    queue &operator=(const queue &q)
    {
        if (this != &q)
        {
            delete[] arr;
            arr = new T[q.capacity];
            size = q.size;
            capacity = q.capacity;
            front = q.front;
            back = q.back;
            for (int i = 0; i < size; i++)
            {
                arr[i] = q.arr[i];
            }
        }
        return *this;
    }

};

main()
{
    cout <<"Queue of things:" << endl;
    queue<char> q;
    q.enqueue('a');
    q.enqueue('b');
    q.enqueue('c');
    //cout << q[0] << endl; // prints 'a'
    cout << q.dequeue() << endl;
    cout << q.dequeue() << endl;
    cout << q.dequeue() << endl;

    queue<int> q2;

    
    q2.enqueue(1);
    q2.enqueue(2);
    q2.enqueue(3);
    cout << q2.dequeue() << endl;
    cout << q2.dequeue() << endl;
    cout << q2.dequeue() << endl;   
}