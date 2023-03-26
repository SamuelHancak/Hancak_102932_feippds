# Assignment 4

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[![FEI PPDS](https://img.shields.io/badge/fei.ppds-1.2.1-blue.svg)](https://pypi.org/project/fei.ppds/)
[![PEP8](https://img.shields.io/badge/Code%20Style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![PEP257](https://img.shields.io/badge/Doctsring%20Conventions-PEP257-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SamuelHancak/Hancak_102932D_feippds/blob/01/LICENSE)

This is a Python implementation of the Dining Savages problem using the fei.ppds package. The Dining Savages problem is
a classic synchronization problem where a group of savages repeatedly take servings from a communal pot of food, which
is cooked by a group of cooks. The problem is to ensure that the savages and cooks synchronize properly so that the pot
is never empty or overfilled.

<hr>
<hr>

## 🔬 The problem we are solving

The Dining Savages problem is a synchronization problem that involves a group of savages sharing a common pot
of food. The savages are dinning all together and share the pot of food, which initially contains some number of
servings (in our implementation `0`).
When a savage is hungry, they take a serving from the pot, eat it, and then return to their seat. If the pot becomes
empty, the savage signalises the cook and waits until the pot is refilled.

If a savage arrives at an empty pot, they must wait for the cook to refill it, and the cook should only refill the pot
when it is empty. Furthermore, the cook should only refill the pot with a fixed number of servings at a time (in our
implementation `1` serving), and the savages must wait until the pot is full again before eating. Finally, multiple
savages should not try to take food from the pot at the same time, and the cook should not try to add food to the pot
while a savage is taking food from it.

<hr>
<hr>

## 🧑‍💻 Solution

The solution to the Dining Savages problem involves coordinating the actions of multiple threads in a shared-memory
setting to ensure that the savages eat from a pot of food without any collisions or deadlocks.

In this solution, we use semaphores and mutexes to coordinate the actions of the threads. The Semaphore class is used to
signal the availability of the pot to the savages, and to signal the cooks to cook more servings. The Mutex class is
used to ensure mutual exclusion when accessing the servings variable and the pot. The Barrier class is used to
synchronize the arrival of all the savages before eating from the pot.

The main function creates the threads and starts them. It then waits for all the threads to complete before exiting. The
savage function represents the behavior of the savages, while the cook function represents the behavior of the cooks.

The `Shared` class represents the shared resources that the threads need to access. The `empty_pot` semaphore signals
the
availability of an empty pot to the cooks. The `full_pot` semaphore signals the availability of a full pot to the
savages.
The `servings_mutex` mutex ensures mutual exclusion when accessing the servings variable, which keeps track of the
number
of servings in the pot. The `cook_mutex` mutex ensures mutual exclusion when accessing the pot by the cook. The barrier
object is used to synchronize the arrival of all the savages before they can eat from the pot.

Below is a snippet of the savage function, which represents the behavior of the savages:

```python
def savage(shared, savage_id):
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
```

The `savage` thread first waits at the barrier until all the savages have arrived. Once they have all arrived, the
savage attempts to take a serving from the pot by acquiring the `servings_mutex`. If the pot is empty, the savage
signals the cooks to cook more servings by calling `shared.empty_pot.signal(NUM_MEALS)`, which signals the cooks to
cook `NUM_MEALS`servings. The savage then waits for the pot to be full again by calling `shared.full_pot.wait()`. Once
the pot is full again, the savage takes a serving from the pot by decrementing the servings variable, and releases
the `servings_mutex`. Finally, the savage eats the serving.

There are several synchronization patterns used in this function:

* The shared `barrier` object is used to synchronize all the savages before they start eating.
* The `shared.servings_mutex` object is used to protect the `shared.servings` variable from concurrent access by
  multiple threads. The mutex is locked before accessing the `shared` variable, and unlocked after the access is
  complete.
* The `shared.empty_pot` and `shared.full_pot` objects are used as condition variables to signal the
  cooks when the pot is empty and to wait for the pot to be full again.

The cook function is responsible for cooking servings of food and refilling the pot. Here is the skeleton of the cook
function:

```python
def cook(shared, num_cooks):
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
```

The `cook` thread first waits at the `empty_pot` condition variable until it is signaled by a savage thread that the pot
is empty. Once the pot is empty, the cook thread acquires the `servings_mutex` and cooks `NUM_MEALS` servings of food.
The cook thread then refills the pot by incrementing the `servings` variable, signals the `full_pot` condition variable
to notify the savage threads that the pot is full again, and releases the `servings_mutex`.

There are several synchronization patterns used in this function:

* The shared `empty_pot` and `full_pot` objects are used as condition variables to signal the cook thread when to cook
  more servings and to notify the savage threads when the pot is full again.
* The `shared.servings_mutex` object is used to protect the `shared.servings` variable from concurrent access by
  multiple threads. The mutex is locked before accessing the `shared` variable, and unlocked after the access is
  complete.

The shared resources used in this implementation are:

* `servings`: A variable representing the number of servings in the pot.
* `empty_pot`: A semaphore that signals the cooks when the pot is empty.
* `full_pot`: A semaphore that signals the savages when the pot is full.
* `servings_mutex`: A mutex that is used to ensure mutual exclusion when accessing the servings variable.
* `cook_mutex`: A mutex that is used to ensure mutual exclusion when the cooks are adding servings to the pot.
* `barrier`: A Barrier object that is used to synchronize the savages before they attempt to take a serving from the
  pot.

The default values for the variables are:

* `NUM_SAVAGES`: 4 (number of savages - represents the number of savage threads )
* `NUM_COOKS`: 3 (number of cooks - represents the number of cook threads)
* `NUM_MEALS`: 15 (size of the pot - max number of meals which can fit into pot)

The exact expected output may vary each time the code is run due to the non-deterministic nature of thread scheduling
but should always have a pattern displayed below:

```
Savage 0 come
Savage 1 come
Savage 2 come
Savage 3 come
Savage 3 we are all, start eating
Savage 3 signalised empty pot
Cook 0 is cooking
Cook 0 added a serving to pot, it now contains 1 servings
... (Cooks cook until the pot is full)
Cook 1 is cooking
Cook 1 added a serving to pot, it now contains 14 servings
Cook 2 is cooking
Cook 2 added a serving to pot, it now contains 15 servings
Cook 2 added last serving to pot and it's full now
Savage 3 takes from pot - servings left 14
Savage 3 is eating
Savage 1 takes from pot - servings left 13
Savage 1 is eating
Savage 2 takes from pot - servings left 12
Savage 2 is eating
Savage 0 takes from pot - servings left 11
Savage 0 is eating
Savage 3 come
Savage 2 come
Savage 1 come
Savage 0 come
Savage 0 we are all, start eating
Savage 0 takes from pot - servings left 10
Savage 0 is eating
... (Such outputs repeat in an infinite loop)
```

<hr>
<hr>

## ⚙️ Usage

1. Install the `fei.ppds` library by running `pip install fei.ppds` in your command line interface
2. Copy the code into a new Python file, e.g. `savages.py`
3. Open a command line interface in the same directory as the `savages.py` file
4. Run the script by typing `python savages.py` in the command line interface and pressing Enter
5. The script will create four threads and run the `main` function

<hr>
<hr>

## 📖 Sources

* [PPDS moodle](https://elearn.elf.stuba.sk/moodle/course/view.php?id=699)
* [YouTube](https://www.youtube.com/watch?v=iotYZJzxKf4)
* [Eiffel](https://www.eiffel.org/doc/solutions/Dining_savages)
* [The Little Book Of Semaphores](https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf)

<hr>
<hr>

[👆 Back to top](#assignment-4)