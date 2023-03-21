from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print

num_savages = 3
num_cooks = 1
num_meals = 10


class Barrier(object):
    def __init__(self, savages_count):
        self.savages_count = savages_count
        self.waiting_savages_count = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None):
        self.mutex.lock()
        self.waiting_savages_count += 1

        if each:
            print(each)

        if self.waiting_savages_count == self.savages_count:
            if last:
                print(last)
            self.waiting_savages_count = 0
            self.barrier.signal(self.savages_count)

        self.mutex.unlock()
        self.barrier.wait()


class Shared:
    def __init__(self, num_servings):
        self.servings = num_servings
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.servings_mutex = Mutex()
        self.print_mutex = Mutex()

        self.barrier1 = Barrier(num_savages)
        self.barrier2 = Barrier(num_savages)


def cook(shared, cook_id, meals):
    while True:
        shared.empty_pot.wait()
        print(f"Cook {cook_id} is cooking")
        sleep(1 / 100)
        shared.servings = meals
        print(f"Pot is full and contains {meals} servings")
        shared.full_pot.signal()


def savage(shared, savage_id, _meals):
    while True:
        shared.barrier1.wait()
        shared.barrier2.wait(each=f'Savage {savage_id} come',
                             last=f'Savage {savage_id} we are all, start eating')

        shared.servings_mutex.lock()
        if shared.servings == 0:
            print(f"Savage {savage_id} signalised empty pot")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.servings -= 1
        print(f"Savage {savage_id} takes from pot - servings left {shared.servings}")
        shared.servings_mutex.unlock()

        print(f"Savage {savage_id} is eating")
        sleep(1 / 100)


def main():
    shared = Shared(0)

    savages = [Thread(savage, shared, i, num_meals) for i in range(num_savages)]
    cooks = [Thread(cook, shared, i, num_meals) for i in range(num_cooks)]

    for s in savages:
        s.join()
    for c in cooks:
        c.join()


if __name__ == '__main__':
    main()
