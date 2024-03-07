import numpy as np
import random
import copy
import multiprocessing
import math
ROW_COUNT = 6
COLUMN_COUNT = 7
AI_PIECE = 1
PLAYER_PIECE = 2
empty_piece=0
import numpy as np
import multiprocessing
import copy

# Assume ROW_COUNT, COLUMN_COUNT, AI_PIECE, PLAYER_PIECE, etc., are defined elsewhere

def parallel_minimax(args):
    # Unpack arguments
    col, board, piece, depth, alpha, beta, maximizingPlayer = args
    # Assume minimax is defined elsewhere
    return minimax(board, depth, piece, alpha, beta, maximizingPlayer, col)

# Initialize multiprocessing pool once
pool = None

def initialize_pool():
    global pool
    if pool is None:  # Only initialize the pool if it hasn't been already
        cpu_count = multiprocessing.cpu_count()  # Get the number of CPU cores
        pool = multiprocessing.Pool(processes=cpu_count)  # Create a pool with CPU core count

def pick_best_move(board, piece, depth=5):
    initialize_pool()  # Ensure the pool is initialized
    
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return None

    # Prepare arguments for each task
    tasks = [(col, copy.deepcopy(board), piece, depth, float('-inf'), float('inf'), True) for col in valid_locations]

    # Map tasks to the pool
    results = pool.map(parallel_minimax, tasks)

    # Find the best move
    best_score = float('-inf')
    best_col = None
    for col, score in results:
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

# Remember to gracefully close the pool if your application ends or no longer needs it
def close_pool():
    global pool
    if pool is not None:
        pool.close()
        pool.join()
        pool = None
# -*- coding: utf-8 -*-
import os, time
import numpy as np
import random
import math

ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2

MAX_SPACE_TO_WIN = 3 # Farthest space where a winning connection may start

def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)

# Checks if column is full or not
def is_valid_column(board, column):
    return board[0][column - 1] == EMPTY

# Returns list of columns that are still not full
def get_valid_locations(board):
    valid_locations = []
    for i in range(1,8):
       if is_valid_column(board, i):
           valid_locations.append(i)
    return valid_locations

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return

# Returns a successor board
def clone_and_place_piece(board, player, column):
    new_board = board.copy()
    place_piece(new_board, player, column)
    return new_board

# Checks if the player won the given board
def detect_win(board, player):
    # Horizontal win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            if board[row][col] == player and board[row][col+1] == player and \
                    board[row][col+2] == player and board[row][col+3] == player:
                return True
    # Vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col] == player and \
                    board[row+2][col] == player and board[row+3][col] == player:
                return True
    # Diagonal upwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col+1] == player and \
                    board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Diagonal downwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            if board[row][col] == player and board[row-1][col+1] == player and \
                    board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False
    
# Returns true if current board is a terminal board which happens when 
# either player wins or no more spaces on the board are free
def is_terminal_board(board):
    return detect_win(board, HUMAN) or detect_win(board, AI) or \
        len(get_valid_locations(board)) == 0
        
def score(board, player):
    score = 0
    # Give more weight to center columns
    for col in range(2, 5):
        for row in range(ROWS):
            if board[row][col] == player:
                if col == 3:
                    score += 3
                else:
                    score+= 2
    # Horizontal pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            adjacent_pieces = [board[row][col], board[row][col+1], 
                                board[row][col+2], board[row][col+3]] 
            score += evaluate_adjacents(adjacent_pieces, player)
    # Vertical pieces
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col], 
                                board[row+2][col], board[row+3][col]] 
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal upwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col+1], 
                                board[row+2][col+2], board[row+3][col+3]] 
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal downwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            adjacent_pieces = [board[row][col], board[row-1][col+1], 
                    board[row-2][col+2], board[row-3][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    return score

def evaluate_adjacents(adjacent_pieces, player):
    opponent = AI
    if player == AI:
        opponent = HUMAN
    score = 0
    player_pieces = 0
    empty_spaces = 0
    opponent_pieces = 0
    for p in adjacent_pieces:
        if p == player:
            player_pieces += 1
        elif p == EMPTY:
            empty_spaces += 1
        elif p == opponent:
            opponent_pieces += 1
    if player_pieces == 4:
        score += 99999
    elif player_pieces == 3 and empty_spaces == 1:
        score += 100
    elif player_pieces == 2 and empty_spaces == 2:
        score += 10
    return score

def minimax(board, ply,piece, alpha, beta, maxi_player,col=20):

    valid_cols = get_valid_locations(board)
    is_terminal = is_terminal_board(board)
    if ply == 0 or is_terminal:
        if is_terminal:
            if detect_win(board, 3-piece):
                return (None,-1000000000)
            elif detect_win(board, piece):
                return (None,1000000000)
            else: # There is no winner
                return (None,0)
        else: # Ply == 0
            return (None,score(board, piece))
    # If max player
    if maxi_player:
        value = -math.inf
        # If every choice has an equal score, choose randomly
        if(col==20):
            col = random.choice(valid_cols)
            # Expand current node/board
            for c in valid_cols:
                next_board = clone_and_place_piece(board, piece, c)
                new_score = minimax(next_board, ply - 1,piece, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    col = c
                # Alpha pruning
                if value > alpha:
                    alpha = new_score
                # If beta is less than or equal to alpha, there will be no need to
                # check other branches because there will not be a better move
                if beta <= alpha:
                    break
        else:
            next_board = clone_and_place_piece(board, piece, col)
            new_score = minimax(next_board, ply - 1,piece, alpha, beta, False)[1]
            value=new_score
            
        return col, value
        
    #if min player
    else:
        value = math.inf
        if(col==20):
            col = random.choice(valid_cols)
            for c in valid_cols:
                next_board = clone_and_place_piece(board, 3-piece, c)
                new_score = minimax(next_board, ply - 1,piece, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    col = c
                if value < beta:
                    beta  = value
                if beta <= alpha:
                    break
        else:
            next_board = clone_and_place_piece(board, 3-piece, col)
            new_score = minimax(next_board, ply - 1,piece, alpha, beta, False)[1]
            
        return col, value
        

