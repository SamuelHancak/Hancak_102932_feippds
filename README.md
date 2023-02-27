# Assignment 1

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[![FEI PPDS](https://img.shields.io/badge/fei.ppds-1.2.1-blue.svg)](https://pypi.org/project/fei.ppds/)
[![PEP8](https://img.shields.io/badge/Code%20Style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![PEP257](https://img.shields.io/badge/Doctsring%20Conventions-PEP257-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SamuelHancak/Hancak_102932D_feippds/blob/01/LICENSE)

Goal of the first assignment is to implement Bakery algorithm and show an example of it using more threads.
The Bakery Algorithm is a mutual exclusion algorithm used
to solve the critical section problem in concurrent computing.
<hr>
<hr>

## 🔬 The problem we are solving

**Concurrent computing** refers to the execution of multiple computations or processes at the same time, in parallel. It
is a paradigm of computing that focuses on dividing a larger problem into smaller tasks that can be executed
simultaneously, often on different processors or cores (in this example on different threads - Multithreading), in order
to improve performance and efficiency.

**Multithreading** involves running multiple threads within a single process, allowing different parts of the program
to run concurrently.

**Mutual exclusion** is a concept in concurrent computing that refers to the prevention of multiple processes or threads
from simultaneously accessing a shared resource or critical section. Mutual exclusion ensures that only one process can
access the shared resource at any given time, preventing conflicts that may arise from multiple processes trying to
access or modify the same resource simultaneously.

There are several techniques for achieving mutual exclusion in concurrent computing and in this assignment we will
achieve it with use of the bakery algorithm.

**The Bakery algorithm** is based on assigning a unique ticket number to each process that wishes to enter the critical
section. The processes then use their ticket numbers to determine the order in which they can enter the critical
section. Algorithm uses a shared data structure to keep track of the tickets and choosing flags. It guarantees that no
two processes can enter the critical section simultaneously, and that every process eventually enters the critical
section if it requests it. Because of that is this algorithm appropriate for achieving mutual exclusion in concurrent
computing.
<hr>
<hr>

## 🧑‍💻 Solution

The implementation of the algorithm can be found in
file [bakery.py](https://github.com/SamuelHancak/Hancak_102932D_feippds/blob/01/bakery.py).

All values necessary for the start of program are already set and the program can be run without any required inputs.
The number of threads is by default set to 4 but can be changed by changing the value of `NUM_THREADS` variable in main.

The implementation of the algorithm itself is in the `proces()` function which requires two params:

* `num_threads` - number of threads
* `thread_id` - ID of current thread

Function also works with two global arrays `num` and `_id`. It uses them to keep track of which proces should be
executed and which should wait.

Execution of critical section is 'faked' by printing a message, with the thread id, and `sleep()` function.

Expected output of the function is message in a such form

```
Process 0 runs a complicated computation!
Process 1 runs a complicated computation!
Process 2 runs a complicated computation!
Process 3 runs a complicated computation!
.
.
.
Process `NUM_THREADS` runs a complicated computation!
```

Each message should be printed in a new line which should (but doesn't have to!) assure us, that only one thread
accessed critical section at the time.

In the case that not only one thread at time had access to critical section, the output of the function won't be in such
a form and can look for example like this

```
Process 0 runs a complicated computation!Process 1 runs a complicated computation!

Process 2 runs a complicated computation!
Process 3 runs a complicated computation!
```

Here we can see that the `process_0` and `process_1` accessed critical section simultaneously.
<hr>

I achieved such output during the first attempt of the implementation when the arrays `num` and `_in` weren't global
variables but were defined in the `process()` function only
<hr>
<hr>

## ⚙️ Usage

1. Install the `fei.ppds` library by running `pip install fei.ppds` in your command line interface
2. Copy the code into a new Python file, e.g. `bakery.py`
3. Open a command line interface in the same directory as the `bakery.py` file
4. Run the script by typing `python bakery.py` in the command line interface and pressing Enter
5. The script will create four threads and run the `process` function

<hr>
<hr>

[👆 Back to top](#assignment-1)

