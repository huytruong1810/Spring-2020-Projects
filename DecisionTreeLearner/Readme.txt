#***************************************************
#  Author: Truong Nguyen Huy
#  UIN: 655471929
#  NetID: thuyng2
#  CS 411 - Homework 12

# Description: this code will attempt to build a decision tree
# using the decision tree learning algorithm presented in figure 18.5 
# in chapter 18 of AIMA textbook

#  File included: hw12.py, Readme.txt, input.csv
#  Run on software: Spyder (Python 3.7) - Anaconda
#***************************************************


IMPORTANT NOTE: this program is written based on the Event-driven programming paradigm.
Therefore, it will only execute procedures if the user inputs something!


Some initial guidelines:
Upon starting the program, a message with show up saying:
"Do you want to use default inputs (Y/N)?"


- Please enter "Y" (without the quotes) if you want the algorithm to take default inputs,
which are the following:

file_name = "input.csv"

attrs = ["Alternate", "Bar", "Fri/Sat", "Hungry", "Patrons", "Price", 
         "Raining", "Reservation", "Type", "WaitEstimate", "WillWait"]

display_symbol = "~~"


- Please enter "N" (without the quotes) if you want to enter these inputs yourself
messages will show up asking the user to input these variables manually

IMPORTANT NOTE: the file that you want to input has to have format follow these rules:
+ it is a CSV file (comma-separated values file) as templated in "input.csv" (no unecessary newline)
+ the number of examples in the file can be as many as you want but the length of these
examples (the number of attr_values) has to be the same with the number of inputted attribute's names
+ the order of these attr_values also has to be equivalent to the order their attribute's names
+ the target attribute should always be last in both the input file and the attribute's names

Example on small inputs: (fruit dataset)

if this is your input csv file
________________________
$,yellow,small,banana   |
$,yellow,medium,lemon   |
$$,red,medium,apple     |
$$$,red,small,cherry    |
$$,yellow,medium,apple  |
$,green,small,banana    |
________________________|

your attributes should be enter in the following order
> price > color > seed_size > name > # (end the inputing sequence with a #)

and if you choose your display indentation symbol as ~~
please expect your output tree to look like the following:

Tree:

Ask price?
~~ price == $ >> Ask seed_size?
~~~~ seed_size == small >> name == banana
~~~~ seed_size == medium >> name == lemon
~~ price == $$ >> name == apple
~~ price == $$$ >> name == cherry