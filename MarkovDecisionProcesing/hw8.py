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


def right_of (action):
    """Return the equivalent action of slipping to the right"""
    if action == 'U':
        return 'R'
    elif action == 'R':
        return 'D'
    elif action == 'D':
        return 'L'
    elif action == 'L':
        return 'U'
    
def left_of (action):
    """Return the equivalent action of slipping to the left"""
    if action == 'U':
        return 'L'
    elif action == 'R':
        return 'U'
    elif action == 'D':
        return 'R'
    elif action == 'L':
        return 'D'


class Markov_Decision_Processes:
    def __init__(self, size, walls, terms, reward, transition_probabilities, discount_rate, epsilon):
        self.size = size # size of the grid (number_of_row, number_of_column)
        
        self.walls = walls # list of walls
        
        self.terms = [] # list of terminal states
        for tupl in terms:
            self.terms.append((tupl[0], tupl[1]))
            
        self.states = [] # list of states
        
        self.utility = {} # dictionary of state - reward pairs
        
        self.grid = [] # the grid (for debugging purposes)
        for i in range(size[1]):
            self.grid.append([])
            for j in range(size[0]):
                self.grid[i].append(None)
        
        for i in range(size[1]):
            for j in range(size[0]):
                if not self.is_wall(i + 1, j + 1):
                    self.states.append((j + 1, i + 1))
                    value = self.is_term(i + 1, j + 1, terms)
                    if value:
                        self.grid[i][j] = value
                        self.utility[(j + 1, i + 1)] = value
                    else:
                        self.grid[i][j] = reward
                        self.utility[(j + 1, i + 1)] = reward
                        
        self.discount_rate = discount_rate # gamma
        
        self.epsilon = epsilon
        
        self.actions = ['U', 'L', 'D', 'R'] # list of applicable actions
        
        # transition model
        # dictionary of state - (action, result) pairs
        # (action, result) is a dictionary of action - (prob, states) pairs
        # (prob, states) is tuples of states giving their euivalent probabilities
        self.TM = {}
        for s in self.states:
            self.TM[s] = {}
            for a in self.actions:
                self.TM[s][a] = [(transition_probabilities[0], self.get_result_state(s, a)), 
                                 (transition_probabilities[1], self.get_result_state(s, right_of(a))), 
                                 (transition_probabilities[2], self.get_result_state(s, left_of(a)))]
                
        self.solved_MDP = None
        
    def is_term (self, x, y, terms):
        """Return reward value if given coordinate is terminal, false otherwise"""
        # check each 3-tuple in terms
        for tupl in terms:
            # if the coordinate matches any of the terminal coordinates
            if tupl[1] == x and tupl[0] == y:
                return tupl[2] # the coordinate is at terminal state
        return False # reaches here means it is not
    
    def is_wall (self, x, y):
        """Return true if given coordinate is at a wall, false otherwise"""
        # check each 2-tuple in walls
        for tupl in self.walls:
            # if the coordinate matches any of the wall coordinates
            if tupl[1] == x and tupl[0] == y:
                return True # the coordinate is at a wall
        return False # reaches here means it is not
    
    def R (self, s):
        """Return the reward for state s"""
        return self.utility[s]

    def P (self, s, a):
        """Return a list of tuples (prob, state) given a state and an action"""
        if a == None:
            return [(0.0, s)]
        else:
            return self.TM[s][a]

    def get_actions (self, s):
        """Return a list of actions in state s"""
        if s in self.terms:
            return [None]
        else:
            return self.actions
                
    def display (self):
        """Print the information of our MDP environment (debugging purposes)"""
        print("size", self.size, "\n")
        print("walls", self.walls, "\n")
        print("terms", self.terms, "\n")
        print("states", self.states, "\n")
        print("utility", self.utility, "\n")
        print("P")
        for k, v in self.TM.items():
            print(k, ":")
            for k2, v2 in v.items():
                print(k2, "->", v2)
            print()
            
        self.grid.reverse()
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                print(self.grid[i][j], end = "\t")
            print()
        self.grid.reverse()

    def get_result_state (self, s, a):
        """Return the state resulting from taking action a in state s"""
        x = s[0]
        y = s[1]
        
        if a == 'U':
            if y + 1 < self.size[1] + 1 and not self.is_wall(y + 1, x):
                return (x, y + 1)
            else:
                return s
            
        elif a == 'R':
            if x + 1 < self.size[0] + 1 and not self.is_wall(y, x + 1):
                return (x + 1, y)
            else:
                return s
            
        elif a == 'D':
            if y - 1 > 0 and not self.is_wall(y - 1, x):
                return (x, y - 1)
            else:
                return s
            
        else:
            if x - 1 > 0 and not self.is_wall(y, x - 1):
                return (x - 1, y)
            else:
                return s
            
    def get_optimal_transition_value (self, value_grid, s):
        """Return the highest value of state s given a value-grid"""
        value_sums = []
        for a in self.get_actions(s): # for each allowed action in state s
            action_sum = 0
            for tupl in self.P(s, a):
                # sum up all possible values resulting from taking that action
                prob = tupl[0]
                s1 = tupl[1]
                action_sum += (prob * value_grid[s1])
            value_sums.append(action_sum) # add that sumation to our value list
        return max(value_sums) # return the highest value
        
    def value_iteration (self):
        """Return a dictionary that keeps track of each value iteration"""
        progress = {} # iteration progress dictionary
        
        U1 = {}
        for s in self.states:
            U1[s] = 0
        progress[0] = U1
            
        gamma = self.discount_rate
        conv_val = self.epsilon * (1 - gamma) / gamma
        iteration = 1
            
        while True:
            U = progress[iteration - 1] # get the previous value-grid state
            U1 = {} # construct the next value-grid state
            delta = 0
            for s in self.states: # for each state in current value-grid
                # apply Bellman equation
                optimal_val = self.get_optimal_transition_value(U, s)
                U1[s] = self.R(s) + gamma * optimal_val
                delta = max(delta, abs(U1[s] - U[s]))
            progress[iteration] = U1 # update the progress
            # check convergency
            if delta <= conv_val:
                # if value-grid has reached convergence, we are done
                # return the value iteration progress
                self.solved_MDP = U1 # save the final solution for policy extraction
                return progress
            
            iteration += 1
            
    def get_utility_of (self, s, a):
        """Return the utility of taking action a in state s"""
        u = 0
        for tupl in self.P(s, a):
            prob = tupl[0]
            s1 = tupl[1]
            u += prob * self.solved_MDP[s1]
        return u

    def evaluate_best_policy (self): # should only be called after the operation of value iteration
        """Return the best policy based on the solution of this MDP environment"""
        policy_book = {}
        for s in self.states: # for each state s
            action_values = {}
            for a in self.get_actions(s): # for each applicable action a in state s
                # save the actions equivalent to each utility value
                action_values[self.get_utility_of(s, a)] = a
            best_value = max(action_values.keys()) # extract best value
            policy_book[s] = action_values[best_value] # save the equivalent best action
        return policy_book


# UTILITY FUNCTIONS ___________________________________________________________
def print_Grid (value_grid, size):
    grid = []
    for i in range(size[1]):
        grid.append([])
        for j in range(size[0]):
            grid[i].append(None)
    for i in range(size[1]):
        for j in range(size[0]):
            if (j + 1, i + 1) in value_grid.keys():
                grid[i][j] = round(value_grid[(j + 1, i + 1)], 3)
            else:
                grid[i][j] = "---"
    grid.reverse()
    for i in range(size[1]):
        for j in range(size[0]):
            print(grid[i][j], end = "\t")
        print()
        
        
def print_Policy (value_grid, size):
    grid = []
    for i in range(size[1]):
        grid.append([])
        for j in range(size[0]):
            grid[i].append(None)
    for i in range(size[1]):
        for j in range(size[0]):
            if (j + 1, i + 1) in value_grid.keys():
                policy = value_grid[(j + 1, i + 1)]
                if policy == 'U':
                    grid[i][j] = 'N'
                elif policy == 'R':
                    grid[i][j] = 'E'
                elif policy == 'D':
                    grid[i][j] = 'S'
                elif policy == 'L':
                    grid[i][j] = 'W'
                else:
                    grid[i][j] = 'T'
            else:
                grid[i][j] = "---"
    grid.reverse()
    for i in range(size[1]):
        for j in range(size[0]):
            print(grid[i][j], end = "\t")
        print()
        
        
def acceptable_symbol (string):
    if (len(string) > 1 and string[0] == "-") or string == "$" or string == "%":
        return True
    return False

    
def Read_file_Run_mdp_Display_result (fname):
    f = open(fname, "r")
    
    mdp_info = []
    while True:
        line = f.readline()
        if not line:
            break
        line = line.replace("\n", "")
        if line.isnumeric() or line.replace(".", "").isdigit() or acceptable_symbol(line):
            mdp_info.append(line)
            
    size = (int(mdp_info.pop(0)), int(mdp_info.pop(0)))
    
    reward = float(mdp_info.pop(0))
    
    discount_rate = float(mdp_info.pop(0))
    
    epsilon = float(mdp_info.pop(0))
    
    transition_probabilities = (float(mdp_info.pop(0)), float(mdp_info.pop(0)), float(mdp_info.pop(0)), float(mdp_info.pop(0)))
    
    walls = []
    num = mdp_info.pop(0)
    while num != "%": # while there are more wall locations
        x = int(num)
        y = int(mdp_info.pop(0))
        walls.append((x, y))
        mdp_info.pop(0) # pop off the ending $
        num = mdp_info.pop(0)
        
    terms = []
    num = mdp_info.pop(0)
    while num != "%": # while there are more terminal states
        x = int(num)
        y = int(mdp_info.pop(0))
        r = float(mdp_info.pop(0))
        terms.append((x, y, r))
        mdp_info.pop(0) # pop off the ending $
        num = mdp_info.pop(0)
    
    mdp_environment = Markov_Decision_Processes(size, walls, terms, reward, transition_probabilities, discount_rate, epsilon)
    
    progress = mdp_environment.value_iteration()
    final_value = progress.popitem()[1]
    policy = mdp_environment.evaluate_best_policy()
    
    for iteration, value_grid in progress.items():
        print("\nIteration:", iteration)
        print_Grid (value_grid, size)
    
    print("\nFinal Value After Convergence")
    print_Grid (final_value, size)
    print("\nFinal Policy")
    print_Policy (policy, size)
    
    
# ->->->->->->->->->->->->->->-> CONSOLE UI <-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-
print("\n\nWelcome to the Markov Decision Processes solver!")

fname = ""
userInput = input ("Do you want to use the templated input file?(Y/N): ")
if (userInput == "Y"):
    fname = "mdp_input.txt"
elif (userInput == "N"):
    fname = input("Please enter the file name you wish to run MDP on:")

# ->->->->->->->->->->->->->->->-> EXECUTION <-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-
Read_file_Run_mdp_Display_result(fname)


    