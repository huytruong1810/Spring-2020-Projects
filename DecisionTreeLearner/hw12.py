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


from math import log2
from csv import reader


def remove_dup (ls):
    ''' Removes duplicates from a list of values '''
    result = []
    for i in ls:
        if not i in result:
            result.append(i)
    return result


def attributes_without (A, attributes):
    ''' Returns the set of attributes without attribute A, that is, attributes - A '''
    result = []
    for attribute in attributes:
        if attribute != A:
            result.append(attribute)
    return result
    

class Dataset:
    ''' A dataset of examples for learning '''
    def __init__ (self, in_csv, attrs):
        ''' 
        Initializes the dataset given an input csv file that has the examples
        correctly ordered and an equivalent list of attribute's names with 
        target attribute being the last attribute in the list
        
        IMPORTANT: the list of attribute's names should be of the same length
        as all the examples
        '''
        self.examples = [] # list of examples, each example is a list of values
        for example in in_csv: # collect the examples
            self.examples.append(example)
            
        # remove the last attribute as it is the target attribute
        self.target_attr = attrs[-1]
        self.attrs = attributes_without(self.target_attr, attrs)


class Leaf:
    ''' Leaf of a decision tree '''
    def __init__ (self, target_value):
        ''' Initializes a leaf with the target value '''
        self.target_value = target_value

    def get_target_value (self):
        return self.target_value
    
    
class DecisionTree:
    ''' A decision tree that supports the DTL algorithm '''
    def __init__ (self, root):
        ''' Initializes a tree/subtree give a root '''
        self.root = root
        self.branches = {} # a dictionary of value - sub-decision-tree pairs

    def insertBranch (self, val, subtree):
        ''' Inserts a branch into the tree '''
        self.branches[val] = subtree

    def display (self, symbol, space_mult, target_attr):
        ''' Recursively displays each node in the tree '''
        print("Ask " + self.root + "?")
        for val, subtree in self.branches.items():
            print(symbol, self.root, "==", val, ">>", end=' ')
            if isinstance(subtree, Leaf):
                print(target_attr, "==", subtree.get_target_value())
                continue
            subtree.display(symbol * space_mult, space_mult, target_attr)


def get_types_of_values (examples):
    ''' Returns the types of values presented in the dataset '''
    types_of_values = []
    # collect each list of values of each attributes in examples
    for i in range(len(examples[0])):
        ls = [] # make an empty list
        for e in examples:
            ls.append(e[i])
        # extract different type of values in that list and save it
        types_of_values.append(remove_dup(ls))
    return types_of_values
    
    
def DTL (examples, attrs, parent_examples = None):
    ''' 
    Decision Tree Learning algorithm (pseudocode in AIMA 3rd edition)
    Returns a Decision Tree
    '''
    if len(examples) == 0:
        return plurality_value(parent_examples)
    
    if same_classification(examples):
        return Leaf(examples[0][-1])
    
    if len(attrs) == 0:
        return plurality_value(examples)
    
    A = argmax_A_in_attributes(range(len(attrs)), examples)
    tree = DecisionTree(attrs[A])
    for vk, exs in tree_split_at(A, examples):
        subtree = DTL(exs, attributes_without(A, attrs), examples)
        tree.insertBranch(vk, subtree)
    return tree


def plurality_value (exs):
    ''' Returns the target value that appears the most in the set of examples '''
    popular_val = types_of_values[-1][0]
    major_value = get_num_target_val(popular_val, exs)
    for value in types_of_values[-1]:
        if get_num_target_val(value, exs) > major_value:
            major_value = get_num_target_val(value, exs)
            popular_val = value
    return Leaf(popular_val)


def get_num_target_val (target_val, exs):
    ''' Returns the number of examples that has the given target value '''
    counter = 0
    for e in exs:
        if e[-1] == target_val:
            counter += 1
    return counter


def same_classification (exs):
    ''' Returns true if all the given examples have the same target value '''
    target_val = exs[0][-1]
    for e in exs:
        if e[-1] != target_val:
            return False
    return True


def argmax_A_in_attributes (attrs, exs):
    ''' Returns the attribute A that Gain(A) returns the highest bits '''
    important_attr = attrs[0]
    gain_value = Gain(important_attr, exs)
    for attr in attrs:
        if Gain(attr, exs) > gain_value:
            gain_value = Gain(attr, exs)
            important_attr = attr
    return important_attr


def Gain (A, exs):
    ''' 
    Tests split the tree at the given attribute A
    Returns the information gain from doing this splitting
    (formula given at page 704 in AIMA 3rd edition)
    '''
    Remainder_A = 0
    for v, ek in tree_split_at(A, exs):
        Remainder_A += (len(ek) / len(exs)) * B(ek)
    return B(exs) - Remainder_A


def B (exs):
    ''' 
    Calculates probability q of the set of examples
    Returns the entropy of a Boolean random variable that is true with
    probability q
    (formula given at page 704 in AIMA 3rd edition)
    '''
    B_q = 0
    count_ls = []
    probs = []
    
    for value in types_of_values[-1]:
        count_ls.append(get_num_target_val(value, exs))    
    s = sum(count_ls)
    if s == 0:
        return 0
    
    for n in count_ls:
        probs.append(n/s)
    for q in probs:
        if q != 0.0:
            B_q += (-q * log2(q))
    return B_q


def tree_split_at (A, exs):
    '''
    Splits the tree at attribute A
    For each "branching" value, the branch leads to a new set of examples branch_exs
    Returns a list of (branching value, branch_exs) tuples
    '''
    branches = []
    for branching_val in types_of_values[A]:
        branch_exs = []
        for e in exs:
            if branching_val == e[A]:
                branch_exs.append(e)
        branches.append((branching_val, branch_exs))
    return branches



#----------------------------------EXCUTION------------------------------------
    
""" IMPORTANT REMINDER """
# program does not check for length or input's correctness 
# error so please have the list of attributes contains correctly 
# ordered attributes equvalent to the input set of examples
# target attribute should always be last in the list of attributes


print("Welcome to the Decision Tree Learning Builder!")
choice = input("Do you want to use default inputs (Y/N)? ")

if choice == "Y":
    file_name = "input.csv"
    attrs = ["Alternate", "Bar", "Fri/Sat", "Hungry", "Patrons", "Price", 
             "Raining", "Reservation", "Type", "WaitEstimate", "WillWait"]
    display_symbol = "~~"
else:
    file_name = input("Please enter your file name of choice: ")
    print("Please enter a list of attribute's names (end the list with a #)")
    attrs = []
    attr = input("> ")
    while attr != "#":
        attrs.append(attr)
        attr = input("> ")
    display_symbol = input("Please enter your display indentation symbol of choice: ")
    
    
in_file = open(file_name, "r", encoding = "utf-8")
in_csv = reader(in_file)

dataset = Dataset(in_csv, attrs)
types_of_values = get_types_of_values(dataset.examples)
tree = DTL(dataset.examples, dataset.attrs)

print("\nTree:\n")
tree.display(display_symbol, 2, dataset.target_attr)