import pygame
import chess
import chess.engine
import chess.svg
import random
import os
from typing import Dict, Optional, Tuple


class ChessGame:
    """
    The main class representing the chess game.

    Attributes:
    board (chess.Board): The current state of the chess board.
    engine (chess.engine.SimpleEngine): The chess engine to calculate AI moves.
    width (int): The width of the game window.
    height (int): The height of the game window.
    square_size (int): The size of each square on the chess board.
    clock (pygame.time.Clock): Pygame clock object to control the game's frame rate.
    screen (pygame.Surface): The main surface where the game is displayed.
    pieces (Dict[str, pygame.Surface]): A mapping of piece symbols to their corresponding images.
    """

    def __init__(self):
        """
        Initialization of the chess game.

        Initializes the chess board, the AI engine, the game window, and loads the images for the chess pieces.
        """
        self.board = chess.Board()
        # path to the stockfish executable file
        # self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.engine = chess.engine.SimpleEngine.popen_uci(
            "./stockfish/stockfish-ubuntu-x86-64-avx2"
        )
        self.width, self.height = 640, 640
        self.square_size = min(self.width, self.height) // 8
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess")
        self.pieces = self.load_pieces()
        self.user_side = chess.WHITE

    def load_pieces(self) -> Dict[str, pygame.Surface]:
        """
        Loads the images for the pieces.

        Returns:
            Dict[str, pygame.Surface]: A dictionary where the keys are piece types and the values are the Pygame images for those pieces.
        """
        pieces = {}
        piece_names = {
            "P": "pawn",
            "N": "knight",
            "B": "bishop",
            "R": "rook",
            "Q": "queen",
            "K": "king",
        }
        for piece in piece_names.keys():
            for color in chess.COLORS:
                color_prefix = "w" if color == chess.WHITE else "b"
                key = f"{piece.upper() if color == chess.WHITE else piece.lower()}"
                path = f"images/{color_prefix}_{piece_names[piece]}.png"

                # Error Handling for loading images
                if not os.path.exists(path):
                    raise Exception(f"The image at {path} does not exist.")
                pieces[key] = pygame.image.load(path).convert_alpha()

        return pieces

    def draw_board(self):
        """
        Draws the board and pieces on the screen.

        The squares of the board are colored alternatively, and the images of the pieces are drawn on top.
        The orientation of the board depends on the user's side.
        """

        for rank in range(8):
            for file in range(8):
                rect = pygame.Rect(
                    file * self.square_size,
                    rank * self.square_size,
                    self.square_size,
                    self.square_size,
                )
                pygame.draw.rect(
                    self.screen,
                    (238, 238, 210) if (file + rank) % 2 == 0 else (119, 149, 86),
                    rect,
                )

                if self.user_side == chess.WHITE:
                    piece = self.board.piece_at(8 * (7 - rank) + file)
                else:
                    piece = self.board.piece_at(8 * rank + (7 - file))

                if piece:
                    image = self.pieces[str(piece)]
                    image = pygame.transform.scale(
                        image, (self.square_size, self.square_size)
                    )
                    self.screen.blit(image, rect)

    def ai_move(self) -> chess.Move:
        """
        Makes a move for the AI.

        Returns:
            chess.Move: The move made by the AI.
        """
        result = self.engine.play(self.board, chess.engine.Limit(time=2.0))
        self.board.push(result.move)
        return result.move

    def get_square_from_mouse(self, x: int, y: int) -> int:
        """
        Converts a mouse position to a chess board square.

        Args:
            x (int): The x-coordinate of the mouse position.
            y (int): The y-coordinate of the mouse position.

        Returns:
            int: The corresponding square on the chess board.
        """
        if self.user_side == chess.WHITE:
            return 8 * (7 - y // (self.height // 8)) + (x // (self.width // 8))
        else:
            return 8 * (y // (self.height // 8)) + (7 - x // (self.width // 8))

    def display_message(self, screen: pygame.Surface, message: str, duration: int):
        """
        Displays a message on the screen for a certain duration.

        Args:
            screen (pygame.Surface): The main surface where the message is displayed.
            message (str): The text of the message.
            duration (int): The duration the message is displayed for, in milliseconds.
        """
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, (0, 0, 0))  # Black color
        screen.blit(text_surface, (self.width // 2, self.height // 2))
        pygame.display.flip()
        pygame.time.wait(duration)

    def wait_for_user(self):
        """
        Waits for the user to make an action. The action can be a mouse click or a key press.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    return True

    def game_loop(self, game_mode: int, user_side: Optional[bool] = None):
        """
        The main game loop.

        Args:
            game_mode (int): The game mode. 1 for play vs. IA, 2 for IA vs. IA.
            user_side (bool, optional): The side of the user. chess.WHITE for white, chess.BLACK for black. Default is None.
        """
        self.user_side = user_side
        running = True
        from_square = None
        to_square = None
        while running:
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if game_mode == 1:  # Play vs. IA
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and self.board.turn == user_side
                    ):
                        x, y = pygame.mouse.get_pos()
                        from_square = self.get_square_from_mouse(x, y)
                    elif (
                        event.type == pygame.MOUSEBUTTONUP
                        and self.board.turn == user_side
                    ):
                        x, y = pygame.mouse.get_pos()
                        to_square = self.get_square_from_mouse(x, y)

                        if from_square is not None and to_square is not None:
                            move = chess.Move(from_square, to_square)
                            if move in self.board.legal_moves:
                                self.board.push(move)
                            else:
                                self.display_message(self.screen, "Invalid move!", 1000)
                            # Reset from_square and to_square
                            from_square = None
                            to_square = None

            if self.board.turn != user_side and game_mode != 2:  # IA's turn
                self.board.push(
                    self.engine.play(self.board, chess.engine.Limit(time=0.1)).move
                )
            elif game_mode == 2:  # IA vs. IA
                self.board.push(
                    self.engine.play(self.board, chess.engine.Limit(time=0.1)).move
                )
                pygame.time.delay(500)

            if self.board.is_checkmate():
                if self.board.turn != user_side:
                    self.display_message(self.screen, "You won!", 1000)
                else:
                    self.display_message(self.screen, "You lost!", 1000)
                if not self.wait_for_user():
                    running = False
            elif self.board.is_stalemate() or self.board.is_insufficient_material():
                self.display_message(self.screen, "It's a draw!", 1000)
                if not self.wait_for_user():
                    running = False

            pygame.display.flip()
            self.clock.tick(60)

    def menu(self, screen: pygame.Surface) -> Tuple[Optional[int], None]:
        """
        The menu of the game.

        Args:
            screen (pygame.Surface): The main surface where the menu is displayed.

        Returns:
            Tuple[Optional[int], None]: The game mode and the user side (which is always None from this method).
        """
        font = pygame.font.Font(None, 36)
        play_vs_ia_button = font.render("Play vs. IA", True, (0, 0, 0))
        ia_vs_ia_button = font.render("IA vs. IA", True, (0, 0, 0))

        running = True
        while running:
            screen.fill((255, 255, 255))

            screen.blit(play_vs_ia_button, (100, 100))
            screen.blit(ia_vs_ia_button, (100, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None, None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 100 <= x <= 300 and 100 <= y <= 140:
                        running = False
                        return 1, None
                    elif 100 <= x <= 300 and 200 <= y <= 240:
                        running = False
                        return 2, None
        return None, None

    def side_menu(self, screen: pygame.Surface) -> Optional[bool]:
        """
        The side menu of the game where the user can choose their side.

        Args:
            screen (pygame.Surface): The main surface where the menu is displayed.

        Returns:
            Optional[bool]: The user side. chess.WHITE for white, chess.BLACK for black. Default is None.
        """
        font = pygame.font.Font(None, 36)
        white_button = font.render("White", True, (0, 0, 0))
        black_button = font.render("Black", True, (0, 0, 0))
        random_button = font.render("Random", True, (0, 0, 0))

        running = True
        while running:
            screen.fill((255, 255, 255))

            screen.blit(white_button, (100, 100))
            screen.blit(black_button, (100, 200))
            screen.blit(random_button, (100, 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 100 <= x <= 300 and 100 <= y <= 140:
                        running = False
                        return chess.WHITE
                    elif 100 <= x <= 300 and 200 <= y <= 240:
                        running = False
                        return chess.BLACK
                    elif 100 <= x <= 300 and 300 <= y <= 340:
                        running = False
                        return random.choice([chess.WHITE, chess.BLACK])

        font = pygame.font.Font(None, 36)
        chosen_color = "White" if user_side == chess.WHITE else "Black"
        chosen_color_text = font.render(
            f"You are playing as {chosen_color}", True, (0, 0, 0)
        )
        screen.blit(chosen_color_text, (100, 400))
        pygame.display.flip()
        pygame.time.delay(2000)

        return user_side

    def close(self):
        """
        Closes the game and the engine.

        It's important to call this method when the game ends to properly release resources.
        """
        self.engine.quit()
        pygame.quit()


def main():
    """
    The main function of the program.

    It initializes pygame and the game, displays the menu and the side menu if necessary, and starts the game loop.
    """
    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess Game")
    game = ChessGame()

    game_mode, user_side = game.menu(screen)
    if game_mode == 1:  # Player vs. IA
        user_side = game.side_menu(screen)
        if user_side is not None:
            chosen_color = "White" if user_side == chess.WHITE else "Black"
            font = pygame.font.Font(None, 36)
            chosen_color_text = font.render(
                f"You are playing as {chosen_color}", True, (0, 0, 0)
            )
            screen.blit(chosen_color_text, (100, 400))
            pygame.display.flip()
            pygame.time.delay(2000)

            game.game_loop(game_mode, user_side)

    game.close()


if __name__ == "__main__":
    main()
