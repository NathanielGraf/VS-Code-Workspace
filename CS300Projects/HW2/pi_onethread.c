#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

int points_in_circle = 0;

// Thread function to generate points and count the ones inside the circle
void* count_points(void* arg) {
    int num_points = *((int*)arg);
    int local_count = 0;

    for (int i = 0; i < num_points; i++) {
        double x = (double)rand() / RAND_MAX;  // Random x coordinate [0,1]
        double y = (double)rand() / RAND_MAX;  // Random y coordinate [0,1]
        if (x * x + y * y <= 1.0) {
            local_count++;
        }
    }

    points_in_circle += local_count;  // Update global variable
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {

    int total_points = atoi(argv[1]);
    pthread_t thread;

    // Create the thread and pass the total number of points to it
    pthread_create(&thread, NULL, count_points, &total_points);
    pthread_join(thread, NULL);

    // Estimate value of pi
    double pi_estimate = 4.0 * points_in_circle / total_points;
    printf("Estimated value of Pi: %f\n", pi_estimate);

    return 0;
}
