import numpy as np
import pygame
import sys
import gui
import board
import game_logic
import ai
import math
import random
import time
import completo_MCTS
from completo_MCTS import Connect4State

PLAYER = 1
AI = 2
SQUARESIZE = 100
empty_piece = 0
ROWS = 6
EMPTY = 0

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return

def draw_menu(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text1 = font.render("Play against Minimax AI", True, (255, 255, 255))
    text2 = font.render("Play against MCTS AI", True, (255, 255, 255))
    text3 = font.render("AI vs AI", True, (255, 255, 255))
    text4 = font.render("Quit", True, (255, 255, 255))

    screen.blit(text1, (50, 100))
    screen.blit(text2, (50, 150))
    screen.blit(text3, (50, 200))
    screen.blit(text4, (50, 250))

    pygame.display.flip()

def get_menu_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] >= 100 and event.pos[1] < 140:
                    return "minimax"
                elif event.pos[1] >= 150 and event.pos[1] < 190:
                    return "mcts"
                elif event.pos[1] >= 200 and event.pos[1] < 240:
                    return "ai_vs_ai"
                elif event.pos[1] >= 250 and event.pos[1] < 290:
                    return "quit"

def play_game(board2, screen, ai_type):
    turn = 1
    is_game_won = False
    col = 0
    total_moves = 0
    minimax_times = []
    gui.draw_board(screen, board2)

    while not is_game_won:
        total_moves += 1
        if turn == PLAYER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    col += 1
                    place_piece(board2, PLAYER, col)
                    gui.draw_board(screen, board2)
                    is_game_won = game_logic.winning_move(board2, PLAYER)
                    if is_game_won:
                        gui.draw_board(screen, board2)
                        time.sleep(5000)
                        return
                    else:
                        turn = AI
                        gui.draw_board(screen, board2)
                        continue

        elif turn == AI:
            initial_time = time.time()

            if ai_type == "minimax":
                best_move = ai.minimax(board2, 5, PLAYER, -np.inf, np.inf, True)[0]
                best_move-=1
            elif ai_type == "mcts":
                best_move = completo_MCTS.UCT(Connect4State(width=7, height=6, board=board2), itermax=1000, verbose=False)

            place_piece(board2, AI, best_move+1)

            is_game_won = game_logic.winning_move(board2, AI)
            running_time = time.time() - initial_time
            minimax_times.append(running_time)
            if is_game_won:
                gui.draw_board(screen, board2)
                pygame.display.update()
                time.sleep(5000)
                return
            else:
                turn = PLAYER
                gui.draw_board(screen, board2)
                pygame.display.update()
                time.sleep(1)
                continue

    if is_game_won:
        running_time = sum(minimax_times) / len(minimax_times)
        print("Thank you for playing!")
        print("Average minimax running time: %.4f seconds" % running_time)
        print("Total number of moves: %s" % total_moves)

def play_ai_vs_ai(board2, screen):
    turn = 1
    is_game_won = False
    total_moves = 0
    minimax_times = []
    mcts_times = []

    while not is_game_won:
        total_moves += 1
        if turn == 1:
            initial_time = time.time()
            best_move = ai.pick_best_move(board2, AI)
            place_piece(board2, AI, best_move)
            running_time = time.time() - initial_time
            minimax_times.append(running_time)
            is_game_won = game_logic.winning_move(board2, AI)
            turn = 2
        else:
            initial_time = time.time()
            best_move = completo_MCTS.UCT(Connect4State(width=7, height=6, board=board2), itermax=1000, verbose=False)
            place_piece(board2, PLAYER, best_move+1)
            running_time = time.time() - initial_time
            mcts_times.append(running_time)
            is_game_won = game_logic.winning_move(board2, PLAYER)
            turn = 1

        gui.draw_board(screen, board2)
        pygame.display.update()
        time.sleep(1)

    if is_game_won:
        minimax_avg_time = sum(minimax_times) / len(minimax_times)
        mcts_avg_time = sum(mcts_times) / len(mcts_times)
        print("Game over!")
        if(turn==2):
            print("the winner is minmax")
        else:
            print("the winner is MCTS")

        print("Average Minimax running time: %.4f seconds" % minimax_avg_time)
        print("Average MCTS running time: %.4f seconds" % mcts_avg_time)
        print("Total number of moves: %s" % total_moves)

def main():
    board2 = board.create_board()
    screen = gui.init_pygame()

    draw_menu(screen)
    choice = get_menu_choice()

    if choice == "minimax" or choice == "mcts":
        play_game(board2, screen, choice)
    elif choice == "ai_vs_ai":
        play_ai_vs_ai(board2, screen)

if __name__ == "__main__":
    main()