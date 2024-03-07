# game_logic.py

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if np.all(board[r, c:c+4] == piece):
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if np.all(board[r:r+4, c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if np.all(np.diag(board[r:r+4, c:c+4]) == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if np.all(np.diag(np.fliplr(board[r-3:r+1, c:c+4])) == piece):
                return True

    return False