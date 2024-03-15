import socket
import pickle
import numpy as np
import threading

# Assuming the game_logic and board (bd) modules are defined elsewhere.
import game_logic
import board as bd

ROWS, COLUMNS = 6, 7
EMPTY = 0

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return

def create_board():
    return np.zeros((ROWS, COLUMNS), dtype=np.int8)

def send_data(clients, board, current_player):
    for client in clients:
        data = {'board': board, 'player': current_player}
        data_bytes = pickle.dumps(data)
        size_bytes = len(data_bytes).to_bytes(4, byteorder='big')
        client[0].sendall(size_bytes)
        client[0].sendall(data_bytes)

def handle_client(conn, player, board, players_turn, next_turn_event, game_over_event, clients):
    while not game_over_event.is_set():
        next_turn_event.wait()  # Wait for their turn
        next_turn_event.clear()  # Clear the event for the next cycle

        # It's this client's turn, so notify them and wait for their move
        send_data([(conn, player)], board, player)

        try:
            column_bytes = conn.recv(1)
            if not column_bytes:
                raise ValueError("Disconnected")
            column = int.from_bytes(column_bytes, byteorder='big') - 1
            
            if players_turn[0] == player and bd.is_valid_column(board, column+1):
                place_piece(board, player, column+1)
                send_data(clients, board, 3 - player)  # Send updated board to both players
                if game_logic.winning_move(board, player):
                    game_over_event.set()
                players_turn[0] = 3 - player  # Switch turns
            else:
                send_data([(conn, player)], board, player)  # Send the same board state back to the player
        except Exception as e:
            print(f"Error: {e}")
            game_over_event.set()

        next_turn_event.set()  # Signal the next client's turn

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    board = create_board()
    players_turn = [1]  # Start with player 1
    next_turn_event = threading.Event()
    game_over_event = threading.Event()
    clients = [None, None]  # Store clients in a list

    for player in range(1, 3):
        conn, addr = server_socket.accept()
        print(f"New connection from {addr}")
        clients[player-1] = (conn, addr)
        threading.Thread(target=handle_client, args=(conn, player, board, players_turn, next_turn_event, game_over_event, clients)).start()

    next_turn_event.set()  # Start the game

    game_over_event.wait()  # Wait for the game to be over
    send_data(clients, board, -1)  # Notify clients the game is over
    for client in clients:
        client[0].close()

if __name__ == '__main__':
    start_server('192.168.68.103', 8888)
