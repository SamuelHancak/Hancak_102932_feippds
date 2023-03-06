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

In order to implement the solution, we use the following synchronization tools:

* **Mutex**: used to provide mutual exclusion for the shared variables
* **Semaphore**: used to signal between the barber and the customers
* **Thread**: used to represent the barber and the customers

To implement this problem, we define a `Shared` class that contains all the shared variables between the barber and
customers. The class contains the following variables:

* `mutex`: a mutex lock to provide mutual exclusion for the shared variables
* `waiting_room`: the number of customers waiting in the waiting room
* `customer`: a semaphore to signal the barber when a customer arrives
* `barber`: a semaphore to signal the customer when the barber is ready to serve him
* `customer_done`: a semaphore to signal the barber when the customer is done
* `barber_done`: a semaphore to signal the customer when the barber is done

We defined also helper functions that simulate different actions, such as `get_haircut`, `cut_hair`, `balk`,
`growing_hair`, and `waiting_in_room`. These functions simulate the time needed for a customer to get a haircut, the
barber to cut hair, and for the hair to grow back.

We use the following global variables to define initial conditions of the barber shop:

* `NUM_OF_CUSTOMERS`: an integer representing the total number of customers that will visit the barber shop. (set to `5`
  by default)
* `SIZE_OF_WAITING_ROOM`: an integer representing the maximum number of customers that can wait in the waiting room at
  any given time. (set to `3` by default)
* `RANDOMNESS`: an integer that determines the amount of randomness in the program, which affects the time it takes for
  a customer to get a haircut or for the barber to cut hair. (set to `5` by default)

The main functions of the code are `customer()` and `barber()`.

The `customer()` function simulates a customer's behavior.
If there is space in the waiting room, the customer enters the waiting room, signals the barber that they are waiting,
waits for the barber to cut their hair, and leaves the waiting room. If there is no space in the waiting room, the
customer balks and leaves the barber shop. After getting a haircut, the customer waits for their hair to grow back.

The `barber()` function simulates the barber's behavior. If there are no customers in the waiting room, the barber
sleeps. When a customer arrives, the barber cuts their hair and waits for them to leave.

The `main()` function initializes the shared variables, creates the threads for the customers and the barber, and
starts them. It joins all the threads and waits for them to complete.

The expected output can vary due to the randomness introduced by the `randint()` function. Each time the code is
executed, the output will likely be different. However, the general output should be in form of printed message in a
such form (with initial setup of variables set as described above):

```
CUSTOMER 0: Is waiting in room - places left 2
CUSTOMER 1: Is waiting in room - places left 1
BARBER: Cuts hair
CUSTOMER 0: Gets haircut
CUSTOMER 2: Is waiting in room - places left 0
CUSTOMER 3: Walks away 'cause waiting room is full
CUSTOMER 4: Walks away 'cause waiting room is full
BARBER: Cuts hair
CUSTOMER 0: Is growing his hair
CUSTOMER 1: Gets haircut
CUSTOMER 0: Is waiting in room - places left 0
```

The use of semaphores, on the lines `116`, `117`, `122`, `123`, `144`, `145`, `150` and `151`, and mutexes, on the
lines `104` and `126` (and it's corresponding unlocks) ensures that only one thread can access a shared variable or
resource at a time, preventing race conditions and ensuring thread safety. The correctness of the solution can be
verified by observing that each customer gets serviced exactly once (before his hair has grown again) and the barber
serves only one customer at a time. Additionally, there are no race conditions or deadlocks in the code, ensuring that
it operates correctly and efficiently.
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

## 📖 Sources

* [Wikipedia](https://en.wikipedia.org/wiki/Sleeping_barber_problem)
* [GeeksForGeeks](https://www.geeksforgeeks.org/sleeping-barber-problem-in-process-synchronization/)
* [Baeldung](https://www.baeldung.com/cs/sleeping-barber-problem)
* [YouTube](https://www.youtube.com/@paralelneprogramovanieadis9457)

<hr>
<hr>

[👆 Back to top](#assignment-2)
