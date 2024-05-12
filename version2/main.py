import pygame
from chess_game.constants import *
from chess_game.game import Game

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("ChessLeague")

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
    run = True
    game_over = False
    turn = White
    FPS = 30
    game = None

    # Afficher le menu au début
    show_menu(Win)

    while run:
        clock.tick(FPS)

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
                    else:
                        game = Game(Width, Height, Rows, Cols, Square, Win)

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game.reset(Win)
                    game_over = False
                    game = Game(Width, Height, Rows, Cols, Square, Win)

        if game_over:
            show_Checkmate(Win)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
