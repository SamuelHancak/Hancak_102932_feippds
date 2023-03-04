# Assignment 2

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[![FEI PPDS](https://img.shields.io/badge/fei.ppds-1.2.1-blue.svg)](https://pypi.org/project/fei.ppds/)
[![PEP8](https://img.shields.io/badge/Code%20Style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![PEP257](https://img.shields.io/badge/Doctsring%20Conventions-PEP257-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SamuelHancak/Hancak_102932D_feippds/blob/01/LICENSE)

Goal of the second assignment is to implement a solution of Sleeping Barber Problem.
Sleeping Barber Problem is a scenario where multiple customers arrive at a barbershop to get a haircut,
but there is only one barber who can serve them.
The program uses mutex and rendezvous primitives from the FEI-PPDS library to synchronize the
interactions between the customers and the barber.

<hr>
<hr>

## 🔬 The problem we are solving

**Concurrent computing** refers to the execution of multiple computations or processes at the same time, in parallel. It
is a paradigm of computing that focuses on dividing a larger problem into smaller tasks that can be executed
simultaneously, often on different processors or cores, in order to improve performance and efficiency.

**Mutual exclusion** is a concept in concurrent computing that refers to the prevention of multiple processes or threads
from simultaneously accessing a shared resource or critical section. Mutual exclusion ensures that only one process can
access the shared resource at any given time, preventing conflicts that may arise from multiple processes trying to
access or modify the same resource simultaneously.

**Race conditions** are a type of software bug that can occur when multiple threads or processes access shared data or
resources without proper synchronization. A race condition occurs when the timing or ordering of concurrent operations
causes unexpected behavior, such as incorrect results, crashes, or deadlock. These bugs can be prevented by using
synchronization mechanisms such as locks, mutexes, semaphores, or atomic
operations to ensure that only one thread or process can access a shared resource at a time.

**The Sleeping Barber Problem** is a synchronization problem that demonstrates race conditions and mutual
exclusion in concurrent systems. It describes a situation where a barber serves customers, where the barber can only cut
hair if there is a customer present, and customers must wait if the barber is busy or leave if the waiting room is full.
The problem involves managing access to a shared resource (the barber's chair) and ensuring that the resources are used
in a mutually exclusive manner to prevent race conditions and deadlocks.

<hr>
<hr>

## 🧑‍💻 Solution

<hr>
<hr>

## ⚙️ Usage

1. Install the `fei.ppds` library by running `pip install fei.ppds` in your command line interface
2. Copy the code into a new Python file, e.g. `barberShop.py`
3. Open a command line interface in the same directory as the `barberShop.py` file
4. Run the script by typing `python barberShop.py` in the command line interface and pressing Enter
5. The script will create four threads and run the `main` function

<hr>
<hr>

[👆 Back to top](#assignment-2)
