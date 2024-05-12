import socket
import pygame
import sys

class ChessClient:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.conn = None
        self.connect_to_server()

    def connect_to_server(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((self.host, self.port))
            print("Connected to server at {}:{}.".format(self.host, self.port))
        except socket.error as e:
            print("Error connecting to server: " + str(e))
            sys.exit()

    def send_move(self, move):
        try:
            self.conn.sendall(str(move).encode('utf-8'))
        except socket.error as e:
            print("Failed to send move to server: " + str(e))
            sys.exit()

    def receive_move(self):
        try:
            return self.conn.recv(2048).decode('utf-8')
        except socket.error as e:
            print("Failed to receive move from server: " + str(e))
            sys.exit()

def main():
    pygame.init()
    Win = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess Client")

    client = ChessClient()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = pygame.mouse.get_pos()
                    move = (x // 100, y // 100)  # Example move format
                    client.send_move(move)

        # Here, we would handle updating the game board
        # For example, receive moves from the server
        move_from_server = client.receive_move()
        print("Received move from server:", move_from_server)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()