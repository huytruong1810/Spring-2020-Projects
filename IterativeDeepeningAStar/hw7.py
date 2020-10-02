#***************************************************
#  Author: Truong Nguyen Huy
#  UIN: 655471929
#  NetID: thuyng2
#  CS 411 - Homework 7

#  Description: this code will attemp to solve the
#  4x4 sliding puzzle using the iterative deepening a-star search algorithm

#  File included: hw7.py, Readme.txt
#  Run on software: Spyder (Python 3.7) - Anaconda
#***************************************************


from time import process_time # for calculating the runtime of IDA*
from sys import getsizeof # for calculating the memory usage of the search tree

# global variable: size of the board
boardSize = 4

# utility functions and data structures _______________________________________
''' returns a 2D-board based on user's input '''
def makeBoard (num_list):
    board = []
    
    for i in range(boardSize):
        board.append([])
    
    index = 0
    for i in range(boardSize):
        for j in range(boardSize):
            board[i].append (num_list[index])
            index += 1
            
    return board

''' Node class definition '''
class Node:
    
    # node constructor
    def __init__(self, board):
        self.board = [] # make the board for the node
        for i in range(boardSize):
            self.board.append([])
        
        for i in range(4):
            for j in range(boardSize):
                self.board[i].append (board[i][j])
        
        self.parent = None # parent of the node
        self.branch = None # transition branch that leads to the node
        self.gScore = None # the path cost score of the node
        self.NMTHScore = None # the number of misplaced tiles heuristic score of the node
        self.MDHScore = None # the manhattan distance heuristic score of the node
        
    # return a replica of the node
    def replicate (self):
        return Node(self.board)
        
    # return position of the blank tile on the board
    def findBlank (self):
        for i in range(boardSize):
            for j in range(boardSize):
                if self.board[i][j] == 0:
                    return [i, j]
       
    # swap two tile on the board
    def swapTile (self, x1, y1, x2, y2):
        temp = self.board[x1][y1]
        self.board[x1][y1] = self.board[x2][y2]
        self.board[x2][y2] = temp
        
    # give the node a parent
    def setParent (self, p):
        self.parent = p
        
    # give the node a transition branch that leads to it
    def setBranch (self, move):
        self.branch = move
        
    # set the path cost of the node
    def setGScore (self, g):
        self.gScore = g
    
    # return the board stored in the node
    def getBoard (self):
        return self.board
    
    # get the parent of the node
    def getParent (self):
        return self.parent
    
    # return the transition branch that leads to the node
    def getBranch (self):
        return self.branch
    
    # return the path cost of the node
    def getGScore (self):
        return self.gScore
    
    # return the heuristic score of the node based on the number of misplaced tiles
    def getHScore_NMT (self):
        return self.NMTHScore
    
    # return the heuristic of the node based on manhattan distance
    def getHScore_MD (self):
        return self.MDHScore
    
    def getCorrectPosition (self, tile, goalBoard):
        for i in range(boardSize):
            for j in range(boardSize):
                if goalBoard[i][j] == tile:
                    return [i, j]
        
    # give the child a heuristic score based on the manhattan distance calculation
    def setMDHeuristic (self, goalBoard):
        self.MDHScore = 0
        for i in range(boardSize):
            for j in range(boardSize):
                # don't consider the blank tile
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j] != goalBoard[i][j]:
                    correctPos = self.getCorrectPosition (self.board[i][j], goalBoard)
                    self.MDHScore += abs(i - correctPos[0]) + abs(j - correctPos[1])
        
    # give the child a heuristic score based on the number of misplaced tiles
    def setNMTHeuristic (self, goalBoard):
        self.NMTHScore = 0
        for i in range(boardSize):
            for j in range(boardSize):
                # don't consider the blank tile
                if self.board[i][j] == 0:
                    continue
                # increment the NMTH score for each misplaced tile
                if self.board[i][j] != goalBoard[i][j]:
                    self.NMTHScore += 1
    
    # give the child an F score (admissible heuristic score) using the number of misplaced tiles
    def getFScore_NMTH (self):
        return self.gScore + self.NMTHScore
    
    # give the child an F score (admissible heuristic score) using the manhattan distance
    def getFScore_MDH (self):
        return self.gScore + self.MDHScore
    
    # return true if the board stored in the node is similar to another board,
    # return false otherwise
    def similarTest (self, otherBoard):
        for i in range(boardSize):
            for j in range(boardSize):
                if self.board[i][j] != otherBoard[i][j]:
                    return False
        return True
    
    # display the board in the node           
    def display (self):
        for i in range(boardSize):
            for j in range(boardSize):
                print(self.board[i][j], end = "\t")
            print("\n")
     
''' Search Tree class definition '''
class SearchTree:
    
    # tree constructor
    def __init__(self, root):
        self.nodes = []
        self.nodes.append (root)
        
    # return the memory usage of the search tree
    def getMemoryUsage (self):
        memoryUsed = 0
        for n in self.nodes:
            memoryUsed += getsizeof (n)
        return memoryUsed
        
    # insert a branch at a cur node
    def insert (self, cur, move, child, gScore, dest):
        
        child.setParent (cur)
        child.setBranch (move)
        child.setGScore (gScore)
        child.setNMTHeuristic (dest)
        child.setMDHeuristic (dest)
        
        self.nodes.append (child)
        
    # return true if a board state is already in the tree, false otherwise
    def alreadyExist (self, cur):
        curBoard = cur.getBoard()
        for n in self.nodes:
            if n.similarTest (curBoard):
                return True
        return False
        
    # expand the branches from a cur node
    def expandBranchesFrom (self, cur, dest):
        children = []
        curGScore = cur.getGScore()
        # find the blank position in the current board
        x = cur.findBlank()[0]
        y = cur.findBlank()[1]
        
        # expand possible branches and make sure that the branch
        # is not already in the tree
        if (y - 1) >= 0:
            child = cur.replicate()
            child.swapTile (x, y - 1, x, y)
            if not self.alreadyExist (child):
                self.insert (cur, 'L', child, curGScore + 1, dest)
                children.append (child)
                
        if (y + 1) < boardSize:
            child = cur.replicate()
            child.swapTile (x, y + 1, x, y)
            if not self.alreadyExist (child):
                self.insert (cur, 'R', child, curGScore + 1, dest)
                children.append (child)
                
        if (x - 1) >= 0:
            child = cur.replicate()
            child.swapTile (x - 1, y, x, y)
            if not self.alreadyExist (child):
                self.insert (cur, 'U', child, curGScore + 1, dest)
                children.append (child)
                
        if (x + 1) < boardSize:
            child = cur.replicate()
            child.swapTile (x + 1, y, x, y)
            if not self.alreadyExist (child):
                self.insert (cur, 'D', child, curGScore + 1, dest)
                children.append (child)
                
        return children
        
    # return a path from the root node to the cur node
    def traceBack (self, cur):
        path = []
        
        # while root node is not met yet
        while cur != self.nodes[0]:
            # collect the moves, aka the transition branches
            path.append (cur.getBranch())
            for n in self.nodes:
                # track back by setting cur to its parent node
                if cur.getParent() == n:
                    cur = n
                    break
                
        # reverse the path by using a stack
        stack = []
        while len(path) != 0:
            stack.append (path.pop())
            
        return stack
    
    # _________________________________________________________________________
    # using number of misplaced tile heuristic, this recursive IDA* algorithm  
    # returns a solution path (if one exist), else returns a candidate 
    # threshold for next iteration
    def _IDAStar_NMTH (self, fringe, dest, threshold,systemInfo):
        
        # get the last node in fringe
        cur = fringe[-1]
        # update number of node expanded
        systemInfo[0] += 1
        
        # if current node f score exceeds current threshold, returns that score
        if cur.getFScore_NMTH() > threshold:
            return cur.getFScore_NMTH()
        # if goal is reached, return true
        if cur.similarTest (dest):
            return True
        
        # let minimum threshold be infinity
        minimum = float("inf")
        # expand on the current node
        children = self.expandBranchesFrom (cur, dest)
        
        for child in children:
            
            fringe.append(child)
            # call itself recursively
            result = self._IDAStar_NMTH (fringe, dest, threshold, systemInfo)
            # if solution is found, return true
            if result == True:
                return True
            # if result is smaller than the minimum threshold, reassign the 
            # minimum threshold 
            if result < minimum:
                minimum = result
            # remove that node from fringe
            fringe.pop()
          
        # return the minimum threshold as candidate for next iteration
        return minimum
    
    # using number of misplaced tile heuristic, this IDA* algorithm  
    # returns a solution path (if one exist), else returns false
    def IDAStar_NMTH (self, start, dest, systemInfo):
        
        # the initial cutoff depth is f score of the start node
        threshold = start.getFScore_NMTH()
        # make fringe with start node
        fringe = [start]
        
        while True:
            
            # call recursive IDA* algorithm
            result = self._IDAStar_NMTH (fringe, dest, threshold, systemInfo)
            # if result is found, returns solution path
            if result == True:
                return self.traceBack(fringe[-1])
            # if result is infinity, no realistic threshold can be found so
            # no solution exist
            if result == float("inf"):
                return False
            # refresh tree
            self.nodes = []
            self.nodes.append (start)
            # update cutoff depth
            threshold = result
            
    # _________________________________________________________________________
    # using Manhattan distance heuristic, this recursive IDA* algorithm  
    # returns a solution path (if one exist), else returns a candidate 
    # threshold for next iteration
    def _IDAStar_MDH (self, fringe, dest, threshold,systemInfo):
        
        # get the last node in fringe
        cur = fringe[-1]
        # update number of node expanded
        systemInfo[0] += 1
        
        # if current node f score exceeds current threshold, returns that score
        if cur.getFScore_MDH() > threshold:
            return cur.getFScore_MDH()
        # if goal is reached, return true
        if cur.similarTest (dest):
            return True
        
        # let minimum threshold be infinity
        minimum = float("inf")
        # expand on the current node
        children = self.expandBranchesFrom (cur, dest)
        
        for child in children:
              
            fringe.append(child)
            # call itself recursively
            result = self._IDAStar_MDH (fringe, dest, threshold, systemInfo)
            # if solution is found, return true
            if result == True:
                return True
            # if result is smaller than the minimum threshold, reassign the 
            # minimum threshold 
            if result < minimum:
                minimum = result 
            # remove that node from fringe
            fringe.pop()
             
        # return the minimum threshold as candidate for next iteration
        return minimum
    
    # using Manhattan distance heuristic, this IDA* algorithm  
    # returns a solution path (if one exist), else returns false
    def IDAStar_MDH (self, start, dest, systemInfo):
        
        # the initial cutoff depth is f score of the start node
        threshold = start.getFScore_MDH()
        # make fringe with start node
        fringe = [start]
        
        while True:
            
            # call recursive IDA* algorithm
            result = self._IDAStar_MDH (fringe, dest, threshold, systemInfo)
            # if result is found, returns solution path
            if result == True:
                return self.traceBack(fringe[-1])
            # if result is infinity, no realistic threshold can be found so
            # no solution exist
            if result == float("inf"):
                return False
            # refresh tree
            self.nodes = []
            self.nodes.append (start)
            # update cutoff depth
            threshold = result

# START OF EXECUTION <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-

print("\n\nWelcome to the 4x4 sliding puzzle solver!!")
inputList = []
while True:
    userInput = input ("Do you want a default starting board?(Y/N): ")
    if (userInput == "Y"):
        inputList = [5,1,2,4,9,7,3,0,11,14,12,8,6,13,10,15]
        break
    elif (userInput == "N"):
        print("Please input a list of 16 intergers ONE NUMBER AT A TIME! (0 for the blank tile)")
        for i in range (16):
            inputList.append ((int)(input("> ")))
        break
    else:
        print("***Error: not a valid option***")
    
    
# Initial board state declaration ********************************
initialBoard = makeBoard (inputList)
# ****************************************************************

# Goal board state declaration *********************************
goalBoard = makeBoard ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0])
# **************************************************************

# IDA* Search using number of misplaced tiles ___________________________________
start = Node(initialBoard)
start.setGScore (0)
start.setNMTHeuristic (goalBoard)
dest = Node(goalBoard)


''' start-up interface '''

print("Initial board:")
start.display()
print("**************")
print("Goal board:")
dest.display()
print("**************")

''' main procedures '''

tree = SearchTree (start)
systemInfo = [0]

# begin time counting 
beginTime = process_time()
# call Iterative-Deepening-A*-Search on the tree using number of misplaced tiles heuristic
result = tree.IDAStar_NMTH (start, goalBoard, systemInfo)
# end time counting
endTime = process_time() 

''' result interface '''

print("IDA* Search using number of misplaced tiles:")
if result == False:
    print("No solution is found!")
else:
    print("Moves:", end = " ")
    for move in result:
        print(move, end = "")
    print("\nNumber of Nodes expanded:", systemInfo[0])
    print("Time Taken:", endTime - beginTime)
    print("Memory Used:", tree.getMemoryUsage()/1024.0, "kb")

# IDA* Search using manhattan distance __________________________________________
start2 = Node(initialBoard)
start2.setGScore (0)
start2.setMDHeuristic (goalBoard)
dest2 = Node(goalBoard)

''' main procedures '''

tree2 = SearchTree (start2)
systemInfo2 = [0]

# begin time counting 
beginTime2 = process_time()
# call Iterative-Deepening-A*-Search on the tree using Manhattan distance heuristic
result2 = tree2.IDAStar_MDH (start2, goalBoard, systemInfo2)
# end time counting
endTime2 = process_time() 

''' result interface '''

print("\n\nIDA* Search using Manhattan distance:")
if result2 == False:
    print("No solution is found!")
else:
    print("Moves:", end = " ")
    for move in result2:
        print(move, end = "")
    print("\nNumber of Nodes expanded:", systemInfo2[0])
    print("Time Taken:", endTime2 - beginTime2)
    print("Memory Used:", tree2.getMemoryUsage()/1024.0, "kb")