import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
empty_piece = 0  # Represent empty spaces with 0
ROWS = 6
COLUMNS = 7
def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)

def drop_piece(board, row, col, piece):
    board[row, col] = piece
    
def is_valid_column(board, column):
    return board[0][column - 1] == empty_piece

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r, col] == empty_piece:
            return r
    return None

def print_board(board):
    print(np.flip(board, 0))  # Flip the board to print with the bottom row first





