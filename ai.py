import numpy as np
import random
import copy
import math
import board as bd
import game_logic
ROW_COUNT = 6
COLUMN_COUNT = 7
AI_PIECE = 1
PLAYER_PIECE = 2
empty_piece = 0

ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2

MAX_SPACE_TO_WIN = 3  # Farthest space where a winning connection may start

def get_valid_locations(board):
    valid_locations = []
    for i in range(1, 8):
        if bd.is_valid_column(board, i):
            valid_locations.append(i)
    return valid_locations

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return

def clone_and_place_piece(board, player, column):
    new_board = board.copy()
    place_piece(new_board, player, column)
    return new_board

def is_terminal_board(board):
    return game_logic.winning_move(board, HUMAN) or game_logic.winning_move(board, AI) or \
        len(get_valid_locations(board)) == 0

def score(board, player):
    score = 0
    for col in range(2, 5):
        for row in range(ROWS):
            if board[row][col] == player:
                if col == 3:
                    score += 3
                else:
                    score += 2
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            adjacent_pieces = [board[row][col], board[row][col+1],
                               board[row][col+2], board[row][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col],
                               board[row+2][col], board[row+3][col]]
            score += evaluate_adjacents(adjacent_pieces, player)
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col+1],
                               board[row+2][col+2], board[row+3][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
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

def minimax(board, ply, piece, alpha, beta, maxi_player, col=20):
    valid_cols = get_valid_locations(board)
    is_terminal = is_terminal_board(board)
    if ply == 0 or is_terminal:
        if is_terminal:
            if game_logic.winning_move(board, 3-piece):
                return (None, -1000000000)
            elif game_logic.winning_move(board, piece):
                return (None, 1000000000)
            else:
                return (None, 0)
        else:
            return (None, score(board, piece))

    if maxi_player:
        value = -math.inf
        if col == 20:
            col = random.choice(valid_cols)
        for c in valid_cols:
            next_board = clone_and_place_piece(board, piece, c)
            new_score = minimax(next_board, ply-1, piece, alpha, beta, False, c)[1]
            if new_score > value:
                value = new_score
                col = c
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        value = math.inf
        if col == 20:
            col = random.choice(valid_cols)
        for c in valid_cols:
            next_board = clone_and_place_piece(board, 3-piece, c)
            new_score = minimax(next_board, ply-1, piece, alpha, beta, True, c)[1]
            if new_score < value:
                value = new_score
                col = c
            beta = min(beta, value)
            if beta <= alpha:
                break

    return col, value

def pick_best_move(board, piece, depth=5):
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return None

    best_score = -math.inf
    best_col = None
    for col in valid_locations:
        next_board = clone_and_place_piece(board, piece, col)
        score = minimax(next_board, depth-1, piece, -math.inf, math.inf, False, col)[1]
        if score > best_score:
            best_score = score
            best_col = col

    return best_col