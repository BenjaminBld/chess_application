# Python Chess Game

This repository contains a simple chess game implemented in Python using Pygame for the graphical user interface and python-chess for the chess logic. The game supports player vs. AI mode as well as AI vs. AI mode. It uses the Stockfish chess engine for AI moves.

## Installation

Before you start, ensure you have Python 3 installed on your system. You can download it from here: https://www.python.org/downloads/.

### Step 1: Clone the repository

Use the command: git clone https://github.com/BenjaminBld/chess_application.git, then navigate to the directory using: cd chess_application.

### Step 2: Install the required packages

Use the command: pip install -r requirements.txt
or if you have both Python 2 and Python 3 installed, use: pip3 install -r requirements.txt

### Step 3: Set up Stockfish engine

This application uses the Stockfish engine to calculate AI moves. You'll need to manually download the appropriate Stockfish binary for your operating system from the official Stockfish website: https://stockfishchess.org/download/ and to adapt engine path in ChessGame.py depending on the OS you are using.

### Step 4: Run the game script

Use the command: python ChessGame.py
or if you have both Python 2 and Python 3 installed, use: python3 ChessGame.py

## Gameplay

The game starts with a menu that allows you to choose the mode of play. You can play against the AI or watch the AI play against itself. When playing against the AI, you also have the option to choose your side (white, black or random choice).

To make a move, simply click the piece you want to move, and then click the square you want to move it to. If the move is legal, the piece will move. If the move is not legal, a message will display in the center of the screen for one second.


