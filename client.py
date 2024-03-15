import socket
import pickle
import pygame
import sys
import threading
import gui  # Assume gui module is defined elsewhere for drawing the board
import math

SQUARESIZE = 100

def receive_data(conn, update_callback):
    try:
        while True:
            size_bytes = conn.recv(4)
            if not size_bytes:
                break
            size = int.from_bytes(size_bytes, byteorder='big')
            data_bytes = conn.recv(size)
            data = pickle.loads(data_bytes)
            update_callback(data['board'], data['player'])
    finally:
        conn.close()

def send_column(conn, column):
    column_bytes = column.to_bytes(1, byteorder='big')
    conn.sendall(column_bytes)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.68.103', 8888))
    screen = gui.init_pygame()
    clock = pygame.time.Clock()

    def update_display(board, player):
        gui.draw_board(screen, board)
        if player == -1:
            print("Game over!")
        elif player == 0:
            print("Waiting for opponent's move...")
        else:
            print("Your turn!")
        pygame.display.flip()

    receive_thread = threading.Thread(target=receive_data, args=(client_socket, update_display))
    receive_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE)) + 1
                send_column(client_socket, col)
                # Wait for the server to respond before allowing another move
                receive_thread.join()
                receive_thread = threading.Thread(target=receive_data, args=(client_socket, update_display))
                receive_thread.start()

        clock.tick(30)

    receive_thread.join()

if __name__ == '__main__':
    main()
