using namespace std;

template <typename T>
class queue
{
public:


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
        if (size == capacity)
        {
            T *temp = new T[capacity * 2];
            for (int i = 0; i < size; i++)
            {
                temp[i] = arr[i];
            }
            delete[] arr;
            arr = temp;
            capacity *= 2;
        }
        arr[size] = x;
        size++;
    }
    
    T dequeue()
    {
        if (size == 0)
        {
            return -1;
        }
        T temp = arr[0];
        for (int i = 0; i < size - 1; i++)
        {
            arr[i] = arr[i + 1];
        }
        size--;
        return temp;
    }

private:
    T *arr;
    int size;
    int capacity;
};