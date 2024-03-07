import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
empty_piece = 0  # Represent empty spaces with 0

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row, col] = piece
    

def is_valid_location(board, col):
    return board[ROW_COUNT-1, col] == empty_piece

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r, col] == empty_piece:
            return r
    return None

def print_board(board):
    print(np.flip(board, 0))  # Flip the board to print with the bottom row first





