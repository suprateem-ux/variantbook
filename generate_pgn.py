import chess
import chess.polyglot
import chess.pgn
import random
from datetime import datetime

BOOK_PATH = "books/antichess.bin"
OUTPUT_PATH = "antichess.pgn"
GAMES = 100
MAX_MOVES = 40

reader = chess.polyglot.open_reader(BOOK_PATH)
entries = list(reader)  # Load all entries for random choice
today = datetime.today().strftime("%Y.%m.%d")

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for game_index in range(GAMES):
        game = chess.pgn.Game()
        game.headers["Event"] = "Book Extraction"
        game.headers["Site"] = "Polyglot Book"
        game.headers["Date"] = today
        game.headers["Round"] = str(game_index + 1)
        game.headers["White"] = "Book"
        game.headers["Black"] = "Book"
        game.headers["Result"] = "*"

        node = game
        move_count = 0
        board = chess.Board()  # For PGN formatting

        for _ in range(MAX_MOVES):
            entry = random.choice(entries)  # Pick random entry globally
            move = entry.move()
            try:
                board.push(move)  # Try normal push
            except:
                # Ignore legality errors
                pass
            node = node.add_variation(move)
            move_count += 1

        if move_count > 0:
            print(game, file=out, end="\n\n")
