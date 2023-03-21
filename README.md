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

The implementation uses threads to represent the savages and cooks, and a set of shared resources to represent the pot
of food. The fei.ppds package is used to provide synchronization primitives such as semaphores, mutexes, and events.

The shared resources include:

A semaphore `empty_pot` to signal an empty pot to the cooks.
A semaphore `full_pot` to signal a full pot to the savages.
A mutex `servings_mutex` to protect access to the servings variable, which represents the number of servings in the pot.
A mutex `cook_mutex` to protect access to the pot by the cooks.
A `Barrier` object to synchronize the savages.
The `Barrier` object is used to ensure that all savages arrive at the pot at the same time before attempting to eat. The
`Barrier` implementation is based on a mutex and an event.

The cook function represents the cook thread that adds servings to the pot. The savage function represents the savage
thread that takes servings from the pot.

The main function creates a `Shared` object with 0 servings and creates a list of threads representing the savages and
cooks. It then waits for all savage and cook threads to finish before exiting.

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