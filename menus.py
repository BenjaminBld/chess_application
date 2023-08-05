import pygame
from typing import Tuple, Optional
import chess
import random

class ChessGameMenus:
    """
    The ChessGameMenus class provides two menu functions: a main menu to choose game mode and a side menu to choose a side.
    """

    def menu(self, screen: pygame.Surface) -> Tuple[Optional[int], None]:
        """
        The main menu function. It displays a menu to choose the game mode.
        """
        font = pygame.font.Font(None, 36)
        running = True
        # Define the buttons of the main menu
        buttons = {
            "Play vs. IA": (100, 100, 1),
            "IA vs. IA": (100, 200, 2)
        }

        while running:
            screen.fill((255, 255, 255))

            # Render the buttons on the screen
            for text, (x, y, return_value) in buttons.items():
                button = font.render(text, True, (0, 0, 0))
                screen.blit(button, (x, y))

            # Check for events (button clicks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None, None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for text, (x, y, return_value) in buttons.items():
                        if x <= mouse_x <= x + 200 and y <= mouse_y <= y + 40:
                            running = False
                            return return_value, None

            pygame.display.flip()

        return None, None

    def side_menu(self, screen: pygame.Surface) -> Optional[bool]:
        """
        The side menu function. It displays a menu to choose a side.
        """
        font = pygame.font.Font(None, 36)
        running = True
        # Define the buttons of the side menu
        buttons = {
            "White": (100, 100, chess.WHITE),
            "Black": (100, 200, chess.BLACK),
            "Random": (100, 300, random.choice([chess.WHITE, chess.BLACK]))
        }

        while running:
            screen.fill((255, 255, 255))

            # Render the buttons on the screen
            for text, (x, y, return_value) in buttons.items():
                button = font.render(text, True, (0, 0, 0))
                screen.blit(button, (x, y))

            # Check for events (button clicks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for text, (x, y, return_value) in buttons.items():
                        if x <= mouse_x <= x + 200 and y <= mouse_y <= y + 40:
                            running = False
                            user_side = return_value
                            chosen_color = "White" if user_side == chess.WHITE else "Black"
                            chosen_color_text = font.render(f"You are playing as {chosen_color}", True, (0, 0, 0))
                            screen.blit(chosen_color_text, (100, 400))
                            pygame.display.flip()
                            pygame.time.delay(2000)

                            return user_side

            pygame.display.flip()

        return None
