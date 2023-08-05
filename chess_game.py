import pygame
from menus import ChessGameMenus
import chess
import random
import os
import chess.engine
from typing import Dict, Optional


class ChessGame(ChessGameMenus):
    def __init__(self, engine_path="/usr/local/bin/stockfish"):
        """
        Initialization of the chess game.

        Initializes the chess board, the AI engine, the game window, and loads the images for the chess pieces.
        
        Args:
            engine_path (str): Path to the Stockfish engine. Default is "/usr/local/bin/stockfish".
        """
        self.board = chess.Board()
        # Check if the Stockfish engine exists at the provided path
        if not os.path.exists(engine_path):
            raise FileNotFoundError("The Stockfish engine was not found at the provided path.")
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.width, self.height = 640, 640
        self.square_size = min(self.width, self.height) // 8
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess")
        # Load images for chess pieces
        self.pieces = self.load_pieces()
        # Default user side is white
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
        # Load images for each piece for both colors
        for piece in piece_names.keys():
            for color in chess.COLORS:
                color_prefix = "w" if color == chess.WHITE else "b"
                key = f"{piece.upper() if color == chess.WHITE else piece.lower()}"
                path = f"images/{color_prefix}_{piece_names[piece]}.png"

                # Check if the image for the piece exists at the given path
                if not os.path.exists(path):
                    raise FileNotFoundError(f"The image at {path} does not exist. Please check the path.")
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

    def display_message(self, screen: pygame.Surface, message: str, duration: int, color=(0, 0, 0)):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, color)
        screen.blit(text_surface, (100, 400))
        pygame.display.flip()
        pygame.time.delay(duration)

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

        The game keeps running until the user quits or the game ends (due to checkmate, stalemate, or insufficient material).
        The user can interact with the game by clicking the mouse to move pieces. The AI makes moves automatically.

        Args:
            game_mode (int): The game mode (1 for playing against the AI, 2 for watching the AI play against itself).
            user_side (Optional[bool]): The user's side (chess.WHITE for white, chess.BLACK for black). If None, the user side is not changed.
        """
        self.user_side = user_side
        clock = pygame.time.Clock()
        from_square = None
        to_square = None
        while True:
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if game_mode == 1 and self.board.turn == user_side:  # Play vs. IA
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        from_square = self.get_square_from_mouse(x, y)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        to_square = self.get_square_from_mouse(x, y)

                        if from_square is not None and to_square is not None:
                            move = chess.Move(from_square, to_square)
                            if move in self.board.legal_moves:
                                self.board.push(move)
                            else:
                                self.display_message(self.screen, "Invalid move!", 1000)
                            from_square = None
                            to_square = None

            # If it's the AI's turn or if the game mode is 2 (AI vs AI), let the AI make a move
            if self.board.turn != user_side or game_mode == 2:
                self.board.push(
                    self.engine.play(self.board, chess.engine.Limit(time=0.1)).move
                )

            # Check if the game has ended due to checkmate, stalemate, or insufficient material, and display a message if so
            if self.board.is_checkmate():
                if self.board.turn != user_side:
                    self.display_message(self.screen, "You won!", 1000)
                else:
                    self.display_message(self.screen, "You lost!", 1000)
                if not self.wait_for_user():
                    return
            elif self.board.is_stalemate() or self.board.is_insufficient_material():
                self.display_message(self.screen, "It's a draw!", 1000)
                if not self.wait_for_user():
                    return

            pygame.display.flip()
            clock.tick(60)

    def close(self):
        """
        Closes the game and the engine.

        This method should be called when the game ends to properly release resources. It closes the Pygame window and shuts down the Stockfish engine.
        """
        self.engine.quit()
        pygame.quit()
