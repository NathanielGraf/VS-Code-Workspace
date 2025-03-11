#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <command>\n", argv[0]);
        exit(1);
    }

    // Create shared memory
    int shm_id = shmget(IPC_PRIVATE, sizeof(struct timeval), IPC_CREAT | 0666);
    if (shm_id == -1) {
        perror("shmget failed");
        exit(1);
    }

    // Attach shared memory
    struct timeval *start_time = (struct timeval *) shmat(shm_id, NULL, 0);
    if (start_time == (struct timeval *) -1) {
        perror("shmat failed");
        exit(1);
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {  // Child process
        // Get the start time
        gettimeofday(start_time, NULL);

        // Execute the command using execvp
        execvp(argv[1], &argv[1]);
        // If exec fails
        perror("execvp failed");
        exit(1);
    } else {  // Parent process
        // Wait for the child process to complete
        wait(NULL);

        // Get the end time
        struct timeval end_time;
        gettimeofday(&end_time, NULL);

        // Calculate elapsed time
        double elapsed_time = (end_time.tv_sec - start_time->tv_sec) +
                              (end_time.tv_usec - start_time->tv_usec) / 1000000.0;

        printf("Elapsed time: %.5f seconds\n", elapsed_time);

        // Detach and remove shared memory
        shmdt(start_time);
        shmctl(shm_id, IPC_RMID, NULL);
    }

    return 0;
}
