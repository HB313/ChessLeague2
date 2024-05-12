import socket
import threading
import pygame
import sys
from chess_game.constants import *
import pygame
from chess_game.constants import *
from chess_game.game import Game

class ChessClient:
    def __init__(self, host='localhost', port=12345):
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

    def send_move(self, row, col):
        try:
            self.conn.sendall(str(row) + ',' + str(col)).encode('utf-8')

            print("Sent move to server:", row, col)
        except socket.error as e:
            print("Failed to send move to server: " + str(e))
            sys.exit()

    
    def receive_move(self):
        try:
            data = self.conn.recv(2048).decode('utf-8')
            if ',' in data:
                row, col = map(int, data.split(','))
                return row, col
            else:
                return None
        except socket.error as e:
            print("Failed to receive move from server: " + str(e))
            sys.exit()



    def send_moves(self, game, game_over):
        print("Send moves thread started.")
        while not game_over:
            if game is not None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                        if pygame.mouse.get_pressed()[0]:
                            location = pygame.mouse.get_pos()
                            row, col = get_positions(location[0], location[1])
                            game.select(row, col)
                            self.send_move(row, col)
            pygame.event.pump()  # Traiter les événements sans bloquer
            pygame.time.delay(100)



    def receive_moves(client, game_over):
        print("Receive moves thread started.")
        while not game_over:
            # Recevoir les mouvements du serveur
            move = client.receive_move()
            if move is not None:
                row, col = move
                print("Received move from server:", row, col)
                # Utiliser les mouvements reçus pour mettre à jour l'état du jeu
                # TODO: Mettre à jour l'état du jeu avec le mouvement reçu
            pygame.time.delay(100)



def get_positions(x,y):
    row = y // Square
    col = x // Square
    return row, col

def show_menu(screen):
    screen.fill(Green)
    font = pygame.font.Font(None, 46)
    title_text = font.render("Menu", True, brown)
    start_button = font.render("Start", True, brown)

    title_rect = title_text.get_rect(center=(Width//2, Height//2 - 75))
    start_button_rect = start_button.get_rect(center=(Width//2, Height//2 + 30))

    screen.blit(title_text, title_rect)
    screen.blit(start_button, start_button_rect)

    pygame.display.flip()

def show_Checkmate(screen):
        screen.fill(Green)
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 42)

        title_text = font.render("Checkmate !", True, light_brown)
        replay_text = small_font.render("Press Spacebar to play again :)", True, light_brown)
        
        title_rect = title_text.get_rect(center=(Width//2, Height//2 - 50))
        replay_rect = replay_text.get_rect(center=(Width//2, Height//2 + 50))


        screen.blit(title_text, title_rect)
        screen.blit(replay_text, replay_rect)


        pygame.display.flip()

def main():
    pygame.init()
    clock = pygame.time.Clock()

    Win = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("ChessLeague")
       
    run = True
    game_over = False
    turn = White
    FPS = 30
    game = None

    client = ChessClient()

    # Initialiser le jeu avant de démarrer les threads
    game = Game(Width, Height, Rows, Cols, Square, Win)

    # Démarrer les threads
    send_thread = threading.Thread(target=client.send_moves, args=(client, game, game_over))
    receive_thread = threading.Thread(target=client.receive_moves, args=(client, game_over))

    send_thread.start()
    receive_thread.start()

    # Attendre que les threads se terminent
    send_thread.join()
    receive_thread.join()

   
    show_menu(Win)

    while run:
        clock.tick(FPS)
        client.receive_move()
        
        if not game_over and game is not None:
            game.update_window()
            if game.check_game():
                game_over = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    row, col = get_positions(location[0], location[1])
                    if game is not None:
                        game.select(row, col)
                        client.send_move(row, col)
                        
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game.reset(Win)
                    game_over = False
                    game = Game(Width, Height, Rows, Cols, Square, Win)

        if game_over:
            show_Checkmate(Win)
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()