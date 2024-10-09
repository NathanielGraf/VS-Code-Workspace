#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <command>\n", argv[0]);
        exit(1);
    }

    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        exit(1);
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {  // Child process
        // Close the read end of the pipe
        close(pipefd[0]);

        // Get the start time
        struct timeval start_time;
        gettimeofday(&start_time, NULL);

        // Write the start time to the pipe
        write(pipefd[1], &start_time, sizeof(start_time));

        // Close the write end of the pipe
        close(pipefd[1]);

        // Execute the command using execvp
        execvp(argv[1], &argv[1]);
        // If exec fails
        perror("execvp failed");
        exit(1);
    } else {  // Parent process
        // Close the write end of the pipe
        close(pipefd[1]);

        // Wait for the child process to complete
        wait(NULL);

        // Get the end time
        struct timeval end_time;
        gettimeofday(&end_time, NULL);

        // Read the start time from the pipe
        struct timeval start_time;
        read(pipefd[0], &start_time, sizeof(start_time));

        // Close the read end of the pipe
        close(pipefd[0]);

        // Calculate elapsed time
        double elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
                              (end_time.tv_usec - start_time.tv_usec) / 1000000.0;

        printf("Elapsed time: %.5f seconds\n", elapsed_time);
    }

    return 0;
}
