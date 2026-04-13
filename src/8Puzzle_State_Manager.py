import os
import copy

'''
Global Variables
'''
default_puzzle = [2,3,0,1,5,6,4,7,8] # Default puzzle in case input.txt is wrong
puzzle_list = [] # actual puzzle
initial_puzzle = [] # Used to calculate the path cost after solving
choice = "" # Initialize choice
counter = 0 # Initialize counter for number of moves done by player


# Stores the puzzle state, it's parent, and the action it took
class Node:
    def __init__(self, state, parent=None, action=None): # default None on parent and action if not specified
        self.state = state
        self.parent = parent
        self.action = action
        
# Clears the terminal to not clutter it
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Checks if current state is solved
def GoalTest(currentNode): 
    return True if currentNode.state == [1,2,3,4,5,6,7,8,0] else False

# Gets path cost
def path_cost(goal_node):
    path_list = [] # stores the path list
    cost = -1 # accounts for initial state
    # Loops til it reaches the initial puzzle
    while goal_node is not None:
        path_list.append(goal_node)
        cost += 1
        goal_node = goal_node.parent
    
    path_list.reverse()
    for path in path_list:
        print_puzzle(path.state)
        print("======")
    
    return cost
            
# Solves through breadth-first search
def solve_bfs(initial_node):
    frontier=[initial_node] # Stores the actual nodes 
    explored=[] # Stores all explored states
    frontierCount = 0 # stores the list of frontiers
    while frontier:
        currentNode = frontier.pop(0)
        explored.append(currentNode.state) # add current node's state to explored
        if (GoalTest(currentNode)): return currentNode, frontierCount # check if solved
        else: # else find all viable moves
            for viableNode in viable_moves(currentNode):
                if viableNode.state not in explored:
                    explored.append(viableNode.state)
                    frontier.append(viableNode)
                    frontierCount += 1

# Solves through depth-first search
def solve_dfs(initial_node):
    frontier=[initial_node] # Stores the actual nodes 
    explored=[] # Stores all explored states
    frontierCount = 0 # stores the list of frontiers
    while frontier:
        currentNode = frontier.pop()
        explored.append(currentNode.state) # add current node's state to explored
        if (GoalTest(currentNode)): return currentNode, frontierCount # check if solved
        else: # else find all viable moves
            for viableNode in viable_moves(currentNode):
                if viableNode.state not in explored:
                    explored.append(viableNode.state)
                    frontier.append(viableNode)
                    frontierCount += 1

# Prints a graphical interface of the puzzle in the terminal
def print_puzzle(puzzle_list):
    print(f"{puzzle_list[0]};{puzzle_list[1]};{puzzle_list[2]}")
    print(f"{puzzle_list[3]};{puzzle_list[4]};{puzzle_list[5]}")
    print(f"{puzzle_list[6]};{puzzle_list[7]};{puzzle_list[8]}")

# Returns a list of all viable nodes in the current position
def viable_moves(original_node):
    viable_nodes = [] # list that stores the list of the viable nodes
    original_state = original_node.state
    index = original_state.index(0) # finds where the 0 is at
    
    if index not in [0,1,2]: # If 0 is not in the top part of the puzzle 
        new_state = copy.deepcopy(original_state)
        new_state[index] = new_state[index-3]
        new_state[index-3] = 0
        viable_nodes.append(Node(state=new_state, parent=original_node, action="w")) # append the puzzle to the list
        
    if index not in [6,7,8]: # If 0 is not in the bottom part of the puzzle 
        new_state = copy.deepcopy(original_state)
        new_state[index] = new_state[index+3]
        new_state[index+3] = 0
        viable_nodes.append(Node(state=new_state, parent=original_node, action="s")) # append the puzzle to the list
        
    if index not in [2,5,8]: # If 0 is not in the right side of the puzzle 
        new_state = copy.deepcopy(original_state)
        new_state[index] = new_state[index+1]
        new_state[index+1] = 0
        viable_nodes.append(Node(state=new_state, parent=original_node, action="d")) # append the puzzle to the list
        
    if index not in [0,3,6]: # If 0 is not in the left side of the puzzle 
        new_state = copy.deepcopy(original_state)
        new_state[index] = new_state[index-1]
        new_state[index-1] = 0
        viable_nodes.append(Node(state=new_state, parent=original_node, action="a")) # append the puzzle to the list
        
    return viable_nodes # list of viable puzzle nodes

'''
MAIN
'''

# Opens file
input_path = os.path.join("..", "data", "8Puzzle", "input.txt")
try:
    with open(input_path, 'r') as file:
        puzzle_list = []
        for line in file:
            clean_line = line.strip()
            
            numbers_as_strings = clean_line.split(';')
            
            for num_str in numbers_as_strings:
                puzzle_list.append(int(num_str))
        expected_numbers = set(range(9))
        puzzle_set = set(puzzle_list)
        if expected_numbers != puzzle_set:
            print("Error: input.txt is not a valid puzzle. Please use 0-8 numbers with no duplicates. Using default puzzle")
            puzzle_list = default_puzzle
except FileNotFoundError:
    print(f"Error: {input_path} file not found. Default puzzle is used.")
    puzzle_list = default_puzzle
except Exception as e:
    # Catches any other errors
    print(f"An unexpected error occurred: {e}. Default puzzle is used.")
    puzzle_list = default_puzzle

# While loop for playing the game and incorrect inputs
while True:
    if puzzle_list == [1,2,3,4,5,6,7,8,0]:
        print_puzzle(puzzle_list)
        print("YOU WIN!")
        break
    print("Type w/a/s/d then enter to move; Type 'SOLVE' to solve the puzzle")
    print_puzzle(puzzle_list)
    print(f"Counter: {counter}")
    #choice = get_key_press() (DOES NOT WORK IN LINUX, DISABLED FOR NOW)
    choice = input("Choice: ")
    clear_screen()
    # print(choice)
    counter += 1    
    index = puzzle_list.index(0) # Finds the index of 0 for if player wants to play
    match choice:
        case "a":
            if index not in [0,3,6]:
                puzzle_list[index] = puzzle_list[index-1]
                puzzle_list[index-1] = 0
            else:
                counter -= 1
        case "s":
            if index not in [6,7,8]:
                puzzle_list[index] = puzzle_list[index+3]
                puzzle_list[index+3] = 0
            else:
                counter -= 1
        case "d":
            if index not in [2,5,8]:
                puzzle_list[index] = puzzle_list[index+1]
                puzzle_list[index+1] = 0
            else:
                counter -= 1
        case "w":
            if index not in [0,1,2]:
                puzzle_list[index] = puzzle_list[index-3]
                puzzle_list[index-3] = 0
            else:
                counter -= 1
        case "SOLVE": # Case for solving
            choice = input("Type 0 for BFS or 1 for DFS: ")
            if choice == '0':
                initial_puzzle = puzzle_list
                solved, exploredCost = solve_bfs(Node(state=puzzle_list))
                print("Path Cost: ", path_cost(solved))
                print("Number of Explored States: ", exploredCost)
                break
            elif choice == '1':
                initial_puzzle = puzzle_list
                solved, exploredCost = solve_dfs(Node(state=puzzle_list))
                print("Path Cost: ", path_cost(solved))
                print("Number of Explored States: ", exploredCost)
                break
            else:
                print("Invalid input.")
        case _:
            print("Invalid input, please use wasd keys or arrow keys.")
            counter -= 1