import numpy as np
import board
import game_logic
import ai
import MCTS
from MCTS import Connect4State
import json
import random

PLAYER = 1
AI = 2
ROWS = 6
EMPTY = 0

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return

def run_game(board, ai_type, game_states_dict):
    turn = 1
    is_game_won = False
    game_states = []

    while not is_game_won:
        if turn == PLAYER:
            board_tuple = tuple(map(tuple, board))
            if str(board_tuple) in game_states_dict and False:
                best_move = game_states_dict[str(board_tuple)]
            if True:
                if ai_type == "minimax":
                    best_move = ai.minimax(board, random.randint(1, 4), PLAYER, -np.inf, np.inf, True)[0]
                elif ai_type == "mcts":
                    best_move = MCTS.UCT(Connect4State(width=7, height=6, board=board,playerJustMoved=AI), itermax=random.randint(200, 700), verbose=False)+1

            place_piece(board, PLAYER, best_move)
            game_states.append((np.copy(board), f"PLAYER: {best_move}"))
            is_game_won = game_logic.winning_move(board, PLAYER)
            turn = AI

            if not is_game_won and np.count_nonzero(board) == 42:
                break
        else:
            board_tuple = tuple(map(tuple, board))
            if str(board_tuple) in game_states_dict:
                best_move = game_states_dict[str(board_tuple)]
            else:
                if ai_type == "minimax":
                    best_move = ai.minimax(board, random.randint(4, 5), AI, -np.inf, np.inf, True)[0]
                elif ai_type == "mcts":
                    best_move = MCTS.UCT(Connect4State(width=7, height=6, board=board,playerJustMoved=PLAYER), itermax=random.randint(4000, 8000), verbose=False)+1
                game_states_dict[str(board_tuple)] = best_move

            place_piece(board, AI, best_move)
            game_states.append((np.copy(board), f"AI: {best_move}"))
            is_game_won = game_logic.winning_move(board, AI)
            turn = PLAYER

            if not is_game_won and np.count_nonzero(board) == 42:
                break

    return game_states

def main():
    num_games = 1
    ai_type = "mcts"  # or "mcts"
    game_states_dict = {}

    # Load game states from file if it exists
    try:
        with open(r"C:\Project Connect Four\projectcommuction\projectconnectfour1\game_states.json", "r") as file:
            existing_game_states = json.load(file)
            game_states_dict.update(existing_game_states)  # Update our local dict with the existing game states
    except FileNotFoundError:
        pass

    # Run games and save game states
    for game_num in range(1, num_games + 1):
        print(game_num)
        board2 = board.create_board()
        game_states = run_game(board2, ai_type, game_states_dict)
        for state in game_states:
            state_tuple = str(tuple(map(tuple, state[0])))  # Convert the board state to a string key
            if state_tuple not in game_states_dict:  # Only add new states
                game_states_dict[state_tuple] = state[1]  # Assuming the move is the value you want to save

    # Save updated game states to file
    with open(r"C:\Project Connect Four\projectcommuction\projectconnectfour1\game_states.json", "w") as file:
        json.dump(game_states_dict, file, indent=4)  # Use indent for better readability

    print(f"{num_games} games played and data saved to game_states.json")

if __name__ == "__main__":
    main()
