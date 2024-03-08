# game_logic.py

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_SPACE_TO_WIN=3
def winning_move(board, player):
    # Horizontal win
    for col in range(COLUMN_COUNT - MAX_SPACE_TO_WIN):
        for row in range(ROW_COUNT):
            if board[row][col] == player and board[row][col+1] == player and \
                    board[row][col+2] == player and board[row][col+3] == player:
                return True
    # Vertical win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col] == player and \
                    board[row+2][col] == player and board[row+3][col] == player:
                return True
    # Diagonal upwards win
    for col in range(COLUMN_COUNT - MAX_SPACE_TO_WIN):
        for row in range(ROW_COUNT - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col+1] == player and \
                    board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Diagonal downwards win
    for col in range(COLUMN_COUNT - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROW_COUNT):
            if board[row][col] == player and board[row-1][col+1] == player and \
                    board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False