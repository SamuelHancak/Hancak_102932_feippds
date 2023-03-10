# Assignment 3

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[![FEI PPDS](https://img.shields.io/badge/fei.ppds-1.2.1-blue.svg)](https://pypi.org/project/fei.ppds/)
[![PEP8](https://img.shields.io/badge/Code%20Style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![PEP257](https://img.shields.io/badge/Doctsring%20Conventions-PEP257-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SamuelHancak/Hancak_102932D_feippds/blob/01/LICENSE)

Goal of the third assignment is to implement one of the solutions of the Dining Philosophers Problem.
The Dining Philosophers Problem is a classic synchronization problem in computer science that illustrates the challenge
of avoiding deadlock and starvation in a concurrent system. In the assignment is implementation of the solution with the
one philosopher as right handed and the rest of them are left handed. We also compared this solution with the solution
with the waiter.
<hr>
<hr>

## 🔬 The problem we are solving

In this example five philosophers sit around a circular table. Each philosopher can do one of the two activities
_thinking_ or _eating_. Each philosopher spends most of their time thinking, but occasionally gets hungry and wants to
eat. However, their food is so slippery that a philosopher needs two forks to eat it. Because the forks are shared
resources, they may be used by only one philosopher at a time. Therefore, a philosopher can only pick up a fork if both
the fork they want to use and the fork on the other side are available. After eating, the philosopher puts both forks
down and resumes thinking.

The problem is to design an algorithm that allows the philosophers to dine without deadlock or starvation. Deadlock
occurs when all philosophers pick up their left fork and wait indefinitely for their right fork, which is held by their
neighbour. Starvation occurs when a philosopher is never able to pick up both forks and eat, because other philosophers
keep taking the forks they need.

There are several solutions to this problem, each with its own advantages and disadvantages. Some
common solutions include:

* Left-handers and right-handers - One of the philosophers takes the forks in the opposite order
* We will let only _N-1_ (N is number of philosophers) philosophers compete for forks at a time (we will establish an
  institute of the waiter)
* We let a philosopher eat only if none of his neighbors are eating (e.g. using a token)

<hr>
<hr>

## 🧑‍💻 Solution

The most important part of the code is the `philosopher()` function. There are executed all the actions which
philosophers are doing. The common solution without the prevention of the deadlock can be found in the code below. There
all of the philosophers pick up forks on the left side first. The deadlock can occur if all the philosophers decide to
eat at the same time. All of them pick up the fork by their left. Due to this, none of them can eat and will wait for
one of the philosophers to put down their fork which will never happen - this produce a circular waiting.

```python
def philosopher(i, shared):
    while (1):
        think(i)

        shared.forks[i].lock()  # pick up left fork
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()  # pick up right fork

        eat(i)

        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()  # put down right fork
        shared.forks[i].unlock()  # put down left fork
```

My solution can be found in the `philosophers.py` file. Program contains a _Left-handers and right-handers_ solution.
The whole solution lies in the fact, that one of the philosophers is right-handed, that means he picks up fork on the
right side at first, in comparison to the other philosophers who are left-handed and they pick up the left fork first.
This leads to the deadlock prevention. I updated the previous code by adding an if which checks, by the philosopher's
id whether he is right-handed of left-handed.

```python
def philosopher(i, shared):
    while (1):
        think(i)

        if i == 0:  # right-handed philosopher
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()  # pick up right fork first
            shared.forks[i].lock()
        else:  # left-handed philosophers
            shared.forks[i].lock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()

        eat(i)

        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
        shared.forks[i].unlock()
```

In the `lecture_solution.py` file can be found solution from our lecture. There is implemented the so-called _waiter
institute_ solution. By implementing a waiter Semaphore we ensure that no more than `NUM_PHILOSOPHERS - 1` philosophers
can acquire the forks at the same time, preventing deadlock. Additionally, the philosophers acquire the forks one at a
time, allowing other philosophers to potentially acquire the other fork in the meantime, preventing starvation.
The `philosopher()` function of this solution looks like this.

```python
def philosopher(i, shared):
    while (1):
        think(i)

        shared.waiter.wait()  # philosopher comes to table - max number of philosophers at the table is `NUM_PHILOSOPHERS - 1`

        shared.forks[i].lock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()

        eat(i)

        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()

        shared.waiter.signal()  # philosopher leaves table

```

Comparison of pros and cons of both solutions:

| Left-handers and right-handers                                                                     | Waiter institute                                                                                                                         |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| ✅ Simple implementation and easy to understand.                                                    | ✅ Prevents deadlock and starvation by using a Semaphore to limit the number of philosophers that can acquire the forks at the same time. |
| ✅ Does not require any additional synchronization constructs                                       | ✅ Robust and works well with any number of philosophers.                                                                                 |
| ✅ Can be useful in situations where starvation is not a concern, and deadlock is unlikely to occur | ✅ Ensures fairness by limiting the number of philosophers that can acquire the forks at the same time.                                   |
| ❌ Not robust and might not work well with a large number of philosophers.                          | ❌ More complex implementation and might be harder to understand.                                                                         |
| ❌ Does not ensure fairness, as some philosophers might be able to eat more often than others.      | ❌ Requires additional synchronization constructs, which might increase the overhead.                                                     |
|                                                                                                    | ❌ Might not be useful in situations where fairness is not a concern, and a simple implementation is sufficient.                          |

In general, the solution from our lecture is more robust and reliable than the one I've implemented. It can handle a
larger number of philosophers and ensure fairness. However, it comes at the cost of increased complexity and potential
overhead. The choice between the two solutions ultimately depends on the specific requirements of the problem at hand.
<hr>
<hr>

## ⚙️ Usage

1. Install the `fei.ppds` library by running `pip install fei.ppds` in your command line interface
2. Copy the code into a new Python file, e.g. `philosophers.py`
3. Open a command line interface in the same directory as the `philosophers.py` file
4. Run the script by typing `python philosophers.py` in the command line interface and pressing Enter
5. The script will create four threads and run the `main` function

<hr>
<hr>

## 📖 Sources

* [PPDS moodle](https://elearn.elf.stuba.sk/moodle/course/view.php?id=699)
* [Zerobone](https://zerobone.net/blog/cs/dining-philosophers-problem/)
* [PagesMTU](https://pages.mtu.edu/~shene/NSF-3/e-Book/MUTEX/TM-example-left-right.html)
* [YouTube](https://www.youtube.com/watch?v=FYUi-u7UWgw)

<hr>
<hr>

[👆 Back to top](#assignment-3)