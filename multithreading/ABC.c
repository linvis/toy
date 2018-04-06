/*
 * A program, start 3 thread, each thread have an ID: A, B, C,
 * every thread print its ID 10 times, the result should be:
 * ABCABC...
 */

#include <stdio.h>
#include <pthread.h>
#include <string.h>


#define THREAD_NUM 3
#define THREAD_TIMES 10

int n = 0;
pthread_mutex_t lock;
pthread_cond_t qready;

void* thread_func(void *arg)
{
    int param = (int)arg;
    int i = 0;
    char c = 'A' + param;

    for ( ; i < THREAD_TIMES; i++) {
        pthread_mutex_lock(&lock);
        while( param != n) {
            pthread_cond_wait(&qready, &lock);
        }
        printf("%c ", c);
        n = (n + 1) % THREAD_NUM;
        pthread_mutex_unlock(&lock);
        pthread_cond_broadcast(&qready);
    }
    return (void *)0;
}

int main(void) 
{
    int i = 0, err;
    pthread_t tid[THREAD_NUM];
    void *tret;
    for ( ; i < THREAD_NUM; i++) {
        err = pthread_create(&tid[i], NULL, thread_func, (void *)i);
        if (err != 0) {
            printf("create thread %d, err %s\n", i, strerror(err));
        }
    }

    for (i = 0; i< THREAD_NUM; i++) {
        err = pthread_join(tid[i], &tret);
        if (err != 0) {
            printf("cant't join with thread %d, err %s\n", i, strerror(err));
        }
    }
    printf("\n");

    return 0;
}
