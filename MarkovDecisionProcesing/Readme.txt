#***************************************************
#  Author: Truong Nguyen Huy
#  UIN: 655471929
#  NetID: thuyng2
#  CS 411 - Homework 8

#  Description: this code will attemp to solve a Markov Decision Processes
#  environment given an input file that contains the specifications for the
#  environment

#  File included: hw8.py, Readme.txt, mdp_input.txt, mdp_input_book.txt
#  Run on software: Spyder (Python 3.7) - Anaconda
#***************************************************

Upon running the program, this message with show up:

Welcome to the Markov Decision Processes solver!

Do you want to use the templated input file?(Y/N):

Please enter Y to run the program on the input txt file named "mdp_input.txt"
Please enter N to manually enter your own input txt file name

An input txt file "mdp_input_book.txt" based on the AIMA book example is also included
with the correct formatting

CAUTION: input txt files have to match the format presented in "mdp_input.txt"
which is also restated as below:

____________________________________________________________________________
# general format note: 
# please avoid using the positive sign (+) to indicate a positive number
# Ex: 2 should be written as 2 and not +2
# please only use the negative sign (-) when writing a negative number,
# please do not use this symbol for any other purposes
# please enter the MDP information in the order as presented below

# size of the gridworld
size : 
# should be exactly 2 positive integers in the format: 
# number_of_row (newline) 
# number_of_col (newline)
# Example:
5
4

reward : 
# reward in non-terminal states
# should be exactly one number in the format:
# reward_value (newline)
# Example:
-0.04

discount_rate : 
# should be a positive number in between 0 and 1 and in the format:
# discount_rate (newline)
# Example:
0.85

epsilon : 
# should be a positive number in the format:
# epsilon (newline)
# Example:
0.001

transition_probabilities : 
# should be exactly four non-negative numbers in the format:
# prob_moving_in_correct_direction (newline)
# prob_slipping_right (newline) 
# prob_slipping_left (newline)
# prob_slipping_backward (newline)
# Example:
0.8
0.1
0.1
0

walls : 
# list of location of walls (these numbers are positive integers)
# each wall coordinate is in the format:
# x_coordinate (newline) 
# y_coordinate (newline)
# end each wall location using a $ on a newline
# end the sequence of walls by a % on a newline
# Example:
2
2
$
2
3
$
%

terminal_states : 
# list of terminal states (x, y, reward) 
# (the coordinates x, y are positive integers)
# each terminal's format: 
# x_coordinate (newline) 
# y_coordinate (newline) 
# terminal_reward (newline)
# end each terminal specifications using a $ on a newline
# end the sequence of terminals by a % on a newline
# Example:
5
3
-3
$
5
4
2
$
4
2
1
$
%
____________________________________________________________________________


