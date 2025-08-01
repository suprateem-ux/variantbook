import chess
import chess.polyglot
import chess.pgn
import os

BOOK_PATH = "books/antichess.bin"
OUTPUT_PATH = "output/antichess.pgn"
GAMES = 100
MAX_MOVES = 40

os.makedirs("output", exist_ok=True)

reader = chess.polyglot.open_reader(BOOK_PATH)

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for game_index in range(GAMES):
        board = chess.Board()  # Standard board
        game = chess.pgn.Game()
        node = game

        for _ in range(MAX_MOVES):
            try:
                entry = reader.weighted_choice(board)
                move = entry.move()
                board.push(move)
                node = node.add_variation(move)
            except IndexError:
                break

        game.headers["Event"] = "Book Extraction"
        game.headers["Round"] = str(game_index + 1)
        game.headers["Result"] = "*"
        print(game, file=out, end="\n\n")
