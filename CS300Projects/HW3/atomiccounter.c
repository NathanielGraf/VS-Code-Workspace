#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
#include <semaphore.h>

volatile long long counter_mutex = 0; // Counter for Mutex Worker
volatile long long counter_semaphore = 0; // Counter for Binary Semaphore Worker
volatile long long counter_cas = 0; // Counter for Compare-and-Swap Worker
volatile long long counter_tas = 0; // Counter for Test-and-Set Worker
volatile long long counter_dum = 0; // Counter without sync

volatile int tas_lock = 0; // 0: unlocked, 1: locked

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
sem_t semaphore;

// Worker functions (DumWorker, CASWorker, etc.)

void* mutexWorker(void* arg) {
    long maxcount = *(long*)arg;
    for (long i = 0; i < maxcount; i++) {
        pthread_mutex_lock(&mutex);
        counter_mutex++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void* semaphoreWorker(void* arg) {
    long maxcount = *(long*)arg;
    for (long i = 0; i < maxcount; i++) {
        sem_wait(&semaphore);
        counter_semaphore++;
        sem_post(&semaphore);
    }
    return NULL;
}

void atomic_increment(long long* value) {
    long long old_val, new_val;
    do {
        old_val = *value;
        new_val = old_val + 1;
    } while (__sync_val_compare_and_swap(value, old_val, new_val) != old_val);
}

void* CASWorker(void* arg) {
    long maxcount = *(long*)arg;
    for (long i = 0; i < maxcount; i++) {
        atomic_increment(&counter_cas);
    }
    return NULL;
}

void tas_lock_acquire(volatile int* lock) {
    while (__sync_lock_test_and_set(lock, 1)) {}
}

void tas_lock_release(volatile int* lock) {
    __sync_lock_release(lock);
}

void* testAndSetWorker(void* arg) {
    long maxcount = *(long*)arg;
    for (long i = 0; i < maxcount; i++) {
        tas_lock_acquire(&tas_lock);
        counter_tas++;
        tas_lock_release(&tas_lock);
    }
    return NULL;
}

void *DumWorker(void *arg) {
    long maxcount = *(long*)arg;
    for (int i = 0; i < maxcount; i++) {
        counter_dum++;
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <NumThread> <MaxCount> \n", argv[0]);
        exit(1);
    }
    int num_threads = atoi(argv[1]);
    long maxcount = atol(argv[2]);

    struct timeval start, end;
    long long elapsed;
    pthread_t threads[num_threads];

    // Dum increment
    gettimeofday(&start, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, DumWorker, &maxcount);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&end, NULL);
    elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    printf("Dum Time [%lld us], final counter value: %lld\n", elapsed, counter_dum);

    // CAS increment
    gettimeofday(&start, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, CASWorker, &maxcount);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&end, NULL);
    elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    printf("CAS Time [%lld us], final counter value: %lld\n", elapsed, counter_cas);

    // TAS increment
    gettimeofday(&start, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, testAndSetWorker, &maxcount);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&end, NULL);
    elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    printf("TAS Time [%lld us], final counter value: %lld\n", elapsed, counter_tas);

    // Mutex increment
    gettimeofday(&start, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, mutexWorker, &maxcount);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&end, NULL);
    elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    printf("MUT Time [%lld us], final counter value: %lld\n", elapsed, counter_mutex);

    // Semaphore increment
    sem_init(&semaphore, 0, 1);
    gettimeofday(&start, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, semaphoreWorker, &maxcount);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&end, NULL);
    elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    printf("SEM Time [%lld us], final counter value: %lld\n", elapsed, counter_semaphore);

    // Destroy mutex and semaphore
    pthread_mutex_destroy(&mutex);
    sem_destroy(&semaphore);
    return 0;
}