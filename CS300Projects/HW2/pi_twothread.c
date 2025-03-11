#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

// Thread function to generate points and count the ones inside the circle
void* count_points(void* arg) {
    int num_points = *((int*)arg);
    int* local_count = (int*)malloc(sizeof(int)); // Allocate memory to store the result
    *local_count = 0;

    for (int i = 0; i < num_points; i++) {
        double x = (double)rand() / RAND_MAX;  // Random x coordinate [0,1]
        double y = (double)rand() / RAND_MAX;  // Random y coordinate [0,1]
        if (x * x + y * y <= 1.0) {
            (*local_count)++;
        }
    }

    pthread_exit((void*)local_count); // Return the result as a pointer
}

int main(int argc, char* argv[]) {

    int total_points = atoi(argv[1]);
    pthread_t thread1, thread2;
    int points_per_thread = total_points / 2;

    // Create the threads and pass the points to each
    pthread_create(&thread1, NULL, count_points, &points_per_thread);
    pthread_create(&thread2, NULL, count_points, &points_per_thread);

    int *result1, *result2;

    // Wait for both threads to finish and get results
    pthread_join(thread1, (void**)&result1);
    pthread_join(thread2, (void**)&result2);

    // Combine results
    int total_points_in_circle = *result1 + *result2;

    // Estimate value of pi
    double pi_estimate = 4.0 * total_points_in_circle / total_points;
    printf("Estimated value of Pi: %f\n", pi_estimate);

    return 0;
}
