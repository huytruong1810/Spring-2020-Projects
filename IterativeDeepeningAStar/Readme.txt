*****************************
Author: Truong Nguyen Huy
UIN: 655471929
NetID: thuyng2
CS 411 - Homework 7

Description: this code will attemp to solve the
4x4 sliding puzzle using the iterative deepening a-star search algorithm
based on both the methods of calculating number of misplaced 
tiles heuristic and Manhattan distance heuristic

File included: hw7.py, Readme.txt
Run on software: Spyder (Python 3.7) - Anaconda
*****************************


IMPORTANT NOTE: this program is written based on the Event-driven programming paradigm.
Therefore, it will only execute procedures if the user inputs something!


Some initial guidelines:
Upon starting the program, a message with show up saying:
"Do you want a default starting board?(Y/N):"

- Please enter "Y" (without the quotes) if you want to make the default initial board 
demonstrated below

Initial board:
5       1       2       4       

9       7       3       0       

11      14      12      8       

6       13      10      15


- Please enter "N" (without the quotes) if you want to enter an initial board yourself
IMPORTANT: this program will ask you to enter one integer at a time, that is, an
integer followed by ENTER and so on. The program will not check if you have inputed
16 integers correctly so it will crash if the input sequence is incorrect

- Entering anything else other than Y/N will get an error message and loop back


PROGRAM INSIGHTS:

Data structures:

- Node class which contains a board configuation, along with some other data
members that supports the iterative deepening A* Search algorithm
- Tree class which is a collection of nodes that the algorithm will be
exploring upon execution. Tree class has the functionality of expanding nodes while
paying attention to repeated children nodes so it would not expand on the same node
twice

Personal algorithm design explanation: (implementation is influenced by pseudo-code represented in https://en.wikipedia.org/wiki/Iterative_deepening_A*)

Iterative deepening A* Search requires the calculation of F Score which is the sum of both the G Score 
(the path cost score) and the H Score (the heuristic score). 
G Score is embedded into each tree node upon its creation. A node's G Score is
equivalent to its depth in the tree
H Score is also calculated and embedded into each tree node upon its creation. There
are two type of H Score: H Score calculated based on the number of misplaced tiles and
H Score calculated based on the Manhattan distance