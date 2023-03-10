"""
This module implements a solution of the Dinning Philosophers Problem.

Solution is implemented using the deadlock-free approach,
where each philosopher picks up the left fork first,
except for one philosopher who picks up the right fork first.
"""

__authors__ = "Tomáš Vavro, Samuel Hančák"
__email__ = "xvavro@stuba.sk, xhancaks@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """
    Represent shared data for all threads.
    """

    def __init__(self):
        """
        Initialize an instance of Shared.

        Class constructor initialises a Mutex for each fork.
        The number of forks is determined by the number of philosophers.
        """
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """
    Simulate thinking.

    @param i: philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)  # simulating time of execution


def eat(i: int):
    """
    Simulate eating.

    @param i: philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)  # simulating time of execution


def philosopher(i, shared):
    """
    Run philosopher's code.

    @param i: philosopher's id
    @param shared: shared data
    """
    left_fork = i
    right_fork = (i + 1) % NUM_PHILOSOPHERS

    for _ in range(NUM_RUNS):
        think(i)

        # picking up forks
        if i == 0:  # right-handed philosopher
            shared.forks[right_fork].lock()  # pick up right fork first
            shared.forks[left_fork].lock()
        else:  # left-handed philosophers
            shared.forks[left_fork].lock()
            shared.forks[right_fork].lock()

        eat(i)

        # put down forks
        shared.forks[right_fork].unlock()
        shared.forks[left_fork].unlock()


def main():
    shared = Shared()  # object of shared variables
    philosophers = [Thread(philosopher, i, shared) for i in range(
        NUM_PHILOSOPHERS)]  # array of philosophers - for each philosopher is appended Thread to the array
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
