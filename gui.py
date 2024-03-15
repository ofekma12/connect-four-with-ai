# gui.py

import numpy as np
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    return screen

def draw_board(screen, board):
    board = np.flipud(board)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r, c] == 2:  # Player's piece
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r, c] == 1:  # AI's piece
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()
