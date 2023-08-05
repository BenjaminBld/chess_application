import pygame
import chess
from chess_game import ChessGame

def main():
    """
    Main function that initializes the chess game, runs the game loop, and properly closes the game.
    """

    # Initialize Pygame
    pygame.init()

    # Set up the main game screen with a size of 800x800 pixels
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess Game")

    # Create an instance of the ChessGame class
    game = ChessGame()

    # Show the main menu and get the selected game mode and user side
    game_mode, user_side = game.menu(screen)
    # Check if the selected game mode is Player vs. IA
    if game_mode == 1:
        # Show the side menu and get the selected user side
        user_side = game.side_menu(screen)
        # If a side was selected, start the game loop
        if user_side is not None:
            game.game_loop(game_mode, user_side)
    # Check if the selected game mode is IA vs. IA
    elif game_mode == 2:
        # Start the game loop without specifying a user side
        game.game_loop(game_mode)

    # Close the game and release any resources
    game.close()

if __name__ == "__main__":
    # Call the main function when the script is run directly (not imported as a module)
    main()
