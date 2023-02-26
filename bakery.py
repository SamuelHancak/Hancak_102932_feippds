"""This module contains an implementation of Bakery algorythm.

Simple implementation of the Bakery algorythm using Threads from fei.ppds library.
"""

__author__ = "Samuel Hancak"
__email__ = "xhancaks@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep


def process(num_threads: int, thread_id: int):
    """
    Simulates a process.

    @param num_threads: number of threads
    @param thread_id: ID of current thread
    """
    # array of numbers assigned to threads which determines in what order will threads execute critical section
    num = [0] * num_threads
    # array used to prevent execution of critical section by thread without assigned number
    _in = [False] * num_threads

    # prevention of execution of critical section by thread before assigning it a number
    _in[thread_id] = True
    # assign number to thread which decides if it will execute critical section
    num[thread_id] = max(num) + 1
    # thread have had number assigned - prevention is unnecessary
    _in[thread_id] = False

    # wait for other processes to finish their execution of critical section
    for i in range(num_threads):
        # prevention of execution of critical section by thread without assigned number
        while _in[i]:
            pass
        # checking if the current thread is next in line to execute critical section
        # if not wait for the appropriate thread/s to execute critical section first
        while num[i] != 0 and (num[i] < num[thread_id] or (num[i] == num[thread_id] and i < thread_id)):
            pass

    # execute critical section
    print(f"Process {thread_id} runs a complicated computation!")
    sleep(1)

    # unassign thread's number
    num[thread_id] = 0


if __name__ == '__main__':
    NUM_THREADS = 4
    threads = [Thread(process, NUM_THREADS, i) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
