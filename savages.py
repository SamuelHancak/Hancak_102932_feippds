"""
Dining Savages problem implementation using threads and semaphores from fei.ppds library.

The goal is to coordinate the savages and the cook to ensure that all savages get to eat and
that the pot is always full.
"""

__authors__ = "Matúš Jókay, Samuel Hančák"
__email__ = "matus.jokay@stuba.sk, xhancaks@stuba.sk"
__license__ = "MIT"

from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print, Event

NUM_SAVAGES = 4  # Number of savages
NUM_COOKS = 3  # Number of cooks
NUM_MEALS = 15  # Number of servings in the pot when it is full


class Barrier(object):
    """
    Barrier implementation for synchronizing savages
    """

    def __init__(self, savages_count):
        self.savages_count = savages_count
        self.waiting_savages_count = 0
        self.mutex = Mutex()  # Mutex for synchronizing access to waiting_savages_count
        self.event = Event()  # Event to signal that all savages have arrived

    def wait(self, each=None, last=None):
        """
        Synchronize all the threads at the barrier

        :param each: String to print before every thread reaches the barrier
        :param last: String to print when all the threads have reached the barrier
        """

        self.mutex.lock()
        self.waiting_savages_count += 1

        if each:
            print(each)

        if self.waiting_savages_count == self.savages_count:
            if last:
                print(last)
            self.waiting_savages_count = 0
            self.event.set()  # Signal that all savages have arrived at the barrier

        self.mutex.unlock()
        self.event.wait()  # Wait until all savages have arrived
        self.event.clear()  # Clear the event for the next barrier synchronization


class Shared:
    """
    Shared resources
    """

    def __init__(self, num_servings):
        self.servings = num_servings
        self.empty_pot = Semaphore(0)  # Semaphore to signal an empty pot to the cook
        self.full_pot = Semaphore(0)  # Semaphore to signal a full pot to the savages
        self.servings_mutex = Mutex()  # Mutex for accessing the servings variable
        self.cook_mutex = Mutex()  # Mutex for accessing the pot by the cook

        self.barrier = Barrier(NUM_SAVAGES)


def cook(shared, cook_id):
    """
    Function representing the cook thread that adds servings to the pot

    :param shared: Object representing the shared resources
    :param cook_id: ID of the cook thread
    """

    while True:
        shared.empty_pot.wait()  # Wait for an empty pot signal from the savages
        shared.cook_mutex.lock()  # Lock the pot
        if shared.servings < NUM_MEALS:  # If the pot is not full, add a serving to the pot
            print(f"Cook {cook_id} is cooking")
            sleep(1 / 100)  # simulate cooking for a short period
            shared.servings += 1
            print(f"Cook {cook_id} added a serving to pot, it now contains {shared.servings} servings")
        shared.cook_mutex.unlock()  # Unlock the pot after cooking

        if shared.servings == NUM_MEALS:
            print(f"Cook {cook_id} added last serving to pot and it's full now")
            shared.full_pot.signal()  # Signal a full pot to the savages


def savage(shared, savage_id):
    """
    Function representing the savage thread that takes servings from the pot

    :param shared: Object representing the shared resources
    :param savage_id: ID of the savage thread
    """
    
    while True:
        # Wait for all savages to arrive before attempting to eat
        shared.barrier.wait(each=f'Savage {savage_id} come',
                            last=f'Savage {savage_id} we are all, start eating')

        # Attempt to take a serving from the pot
        shared.servings_mutex.lock()
        if shared.servings == 0:
            # If the pot is empty, signal the cooks to cook more
            print(f"Savage {savage_id} signalised empty pot")
            shared.empty_pot.signal(NUM_MEALS)  # signal NUM_MEALS servings to be cooked
            shared.full_pot.wait()  # wait for the pot to be full again
        shared.servings -= 1  # take a serving from the pot
        print(f"Savage {savage_id} takes from pot - servings left {shared.servings}")
        shared.servings_mutex.unlock()  # release the mutex

        # Eat the serving
        print(f"Savage {savage_id} is eating")
        sleep(1 / 100)  # simulate eating for a short period


def main():
    # Create a new shared resource object with 0 servings
    shared = Shared(0)

    # Create a list of threads representing the savages
    savages = [Thread(savage, shared, i) for i in range(NUM_SAVAGES)]
    # Create a list of threads representing the cooks
    cooks = [Thread(cook, shared, i) for i in range(NUM_COOKS)]

    # Wait for all savage threads to finish
    for s in savages:
        s.join()
    # Wait for all cook threads to finish
    for c in cooks:
        c.join()


if __name__ == '__main__':
    main()
