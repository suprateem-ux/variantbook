import chess.polyglot
import chess.pgn
from datetime import datetime

BOOK_PATH = "books/antichess.bin"
OUTPUT_PATH = "antichess.pgn"
GAMES = 100
MAX_MOVES = 40

reader = chess.polyglot.open_reader(BOOK_PATH)
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

        # Use a dummy starting position, but don't enforce legality
        board = chess.Board()  # Needed for UCI parsing
        try:
            for _ in range(MAX_MOVES):
                entry = reader.random()  # Pick any entry from the book
                move = entry.move()
                try:
                    board.push(move)  # Push for PGN formatting
                except:
                    # If illegal, just skip legality check and add UCI move text
                    pass
                node = node.add_variation(move)
                move_count += 1
        except StopIteration:
            pass

        if move_count > 0:
            print(game, file=out, end="\n\n")
