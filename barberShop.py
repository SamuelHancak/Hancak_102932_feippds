"""
Program represents a solution of the Sleeping Barber Problem.

Sleeping Barber Problem is a scenario where multiple customers arrive at a barbershop to get a haircut,
but there is only one barber who can serve them.
The program uses mutex and rendezvous primitives from the FEI-PPDS library to synchronize the
interactions between the customers and the barber.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Marián Šebeňa, Samuel Hančák"
__email__ = "mariansebena@stuba.sk, xhancaks@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

NUM_OF_CUSTOMERS = 5
SIZE_OF_WAITING_ROOM = 3
RANDOMNESS = 5  # time of functions execution is randomised by this variable


class Shared(object):

    def __init__(self):
        """
        Class constructor initializes 4 semaphores
        for barber and customer states, creates Mutex object,
        and waiting room counter
        """
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """
    Simulates time and prints info when customer gets haircut

    @param i: Index of current customer
    """
    print(f"CUSTOMER {i}: Gets haircut")
    sleep(randint(1, RANDOMNESS) / 10)  # simulating time of execution


def cut_hair():
    """
    Simulates time and prints info when barber cuts customer's hair
    """
    print('BARBER: Cuts hair')
    sleep(randint(1, RANDOMNESS) / 10)  # simulating time of execution


def balk(i):
    """
    Represents situation when waiting room is full and prints info

    @param i: Index of current customer
    """
    print(f"CUSTOMER {i}: Walks away 'cause waiting room is full")
    sleep(randint(1, RANDOMNESS) / 10)  # simulating time of execution


def growing_hair(i):
    """
    Represents situation when customer waits after getting haircut.
    So hair is growing and customer is sleeping for some time.

    @param i: Index of current customer
    """
    print(f"CUSTOMER {i}: Is growing his hair")
    sleep(randint(1, RANDOMNESS) / 10)  # simulating time of execution


def waiting_in_room(i, shared):
    """
    Simulates time and prints info when customer is waiting in the waiting room

    @param i: Index of current customer
    @param shared: Shared object of needed variables
    """
    print(f"CUSTOMER {i}: Is waiting in room - places left {SIZE_OF_WAITING_ROOM - shared.waiting_room}")
    sleep(randint(1, RANDOMNESS) / 10)  # simulating time of execution


def customer(i, shared):
    """
    Function represents customers behaviour. Customer come to waiting if room is full sleep.
    Wake up barber and waits for invitation from barber. Then gets new haircut.
    After it both wait to complete their work. At the end waits to hair grow again.

    @param i: Index of current customer
    @param shared: Shared object of needed variables
    """
    while True:
        # access to waiting room
        shared.mutex.lock()  # ensure that only one thread can access and modify `waiting_room` at a time
        # checking if there is a place for another customer in the waiting room
        if shared.waiting_room < SIZE_OF_WAITING_ROOM:
            shared.waiting_room += 1
            waiting_in_room(i, shared)
            shared.mutex.unlock()  # lock is released after the critical section of the code is executed
        else:
            shared.mutex.unlock()  # lock is released after the critical section of the code is executed
            balk(i)  # if the waiting room is full customer walks away
            continue

        # rendezvous 1
        shared.customer.signal()
        shared.barber.wait()

        get_haircut(i)

        # rendezvous 2
        shared.customer_done.signal()
        shared.barber_done.wait()

        # leave waiting room
        shared.mutex.lock()  # ensure that only one thread can access and modify `waiting_room` at a time
        shared.waiting_room -= 1
        shared.mutex.unlock()  # lock is released after the critical section of the code is executed

        # customer waits for hair to grow again
        growing_hair(i)


def barber(shared):
    """
    Function barber represents barber. Barber is sleeping.
    When customer come to get new hair wakes up barber.
    Barber cuts customer hair and both wait to complete their work.

    @param shared: Shared object of needed variables
    """
    while True:
        # rendezvous 1
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        # rendezvous 2
        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    shared = Shared()  # object of shared variables
    customers = []  # array of customers - for each customer is appended Thread to the array

    for i in range(NUM_OF_CUSTOMERS):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
