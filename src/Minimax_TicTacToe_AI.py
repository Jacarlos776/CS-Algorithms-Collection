import os
import random
import math

# Global variables
board = ["-", "-", "-",
        "-", "-", "-",
        "-", "-", "-"]
player = ""
ai = ""
winner = "" 

# Clears terminal screen for playing
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Prints the board
def print_board():
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("----------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("----------")
    print(board[6] + " | " + board[7] + " | " + board[8])

# Allows the player to input their move
def playerInput():
    while True:
        try:
            inp = int(input("Enter a number 1-9: "))
            if 1 <= inp <= 9 and board[inp - 1] == "-":
                board[inp - 1] = player
                clear_screen()
                return
            else:
                clear_screen()
                print_board()
                print("Incorrect input. That spot is already taken or invalid.")
        except ValueError:
            clear_screen()
            print_board()
            print("Incorrect input. Please enter a number.")

def checkWinner(current_board):
    # Winning combinations
    winning_combination = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    # Checks for a winner
    for combo in winning_combination:
        pos1, pos2, pos3 = combo
        if current_board[pos1] == current_board[pos2] == current_board[pos3] and current_board[pos1] != "-":
            if current_board[pos1] == ai:
                return 1  # AI wins
            else:
                return -1 # Player wins
    
    # Checks for tie
    if "-" not in current_board:
        return 0 # It's a tie
    
    # Continue
    return None

# Viable moves
def successors(current_board, current_player_token):
    successor_list = []
    
    for i in range(len(current_board)):
        if current_board[i] == "-":
            new_board = list(current_board)
            new_board[i] = current_player_token
            successor_list.append((i, new_board))
            
    return successor_list

def max_value(current_board, alpha, beta):
    winner = checkWinner(current_board)
    if winner is not None:
        return winner

    m = -math.inf
    for action, new_board in successors(current_board, ai):
        v = min_value(new_board, alpha, beta)
        m = max(m, v)
        if m >= beta:
            return m
        alpha = max(alpha, m)
    return m

def min_value(current_board, alpha, beta):
    winner = checkWinner(current_board)
    if winner is not None:
        return winner

    m = math.inf
    for action, new_board in successors(current_board, player):
        v = max_value(new_board, alpha, beta)
        m = min(m, v)
        if m <= alpha:
            return m
        beta = min(beta, m)
    return m


def ai_turn():
    best_move_index = -1
    best_score = -math.inf
    alpha = -math.inf
    beta = math.inf
    
    # Find highest minimax score
    for action, new_board in successors(board, ai):
        score = min_value(new_board, alpha, beta)
        if score > best_score:
            best_score = score
            best_move_index = action
    
    # Do it
    board[best_move_index] = ai

def choosePlayer():
    global player, ai
    while True:
        inp = input("Enter 'X' to be X or 'O' to be O: ").upper()
        if inp == 'X':
            player = "X"
            ai = "O"
            return
        elif inp == 'O':
            player = 'O'
            ai = "X"
            board[random.randint(0,8)] = "X"
            return
        else:
            print("Invalid input.")

# Main
choosePlayer()
current_turn = player # Human player always goes first because the AI 'randomizes' its first turn

while True:
    clear_screen()
    print_board()
    
    if current_turn == player:
        print("\nYour turn as", player)
        playerInput()
        current_turn = ai
    else:
        print("\nAI's turn as", ai)
        ai_turn()
        current_turn = player
    
    game_result = checkWinner(board)
    if game_result is not None:
        clear_screen()
        print_board()
        if game_result == 1:
            print("\nAI is the winner!")
        elif game_result == -1:
            print("\nYou are the winner!")
        else:
            print("\nIt's a tie!")
        break