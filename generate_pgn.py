import chess
import chess.polyglot
import chess.pgn
from chess.variant import AntichessBoard  # from python-chess-variants

BOOK_PATH = "books/antichess.bin"
OUTPUT_PATH = "output/antichess.pgn"
GAMES = 100  # Number of games
MAX_MOVES = 40

reader = chess.polyglot.open_reader(BOOK_PATH)

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for game_index in range(GAMES):
        board = AntichessBoard()  # Antichess variant
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

        game.headers["Event"] = "Antichess Book Extraction"
        game.headers["Site"] = "Generated from Polyglot"
        game.headers["Round"] = str(game_index + 1)
        game.headers["White"] = "Book"
        game.headers["Black"] = "Book"
        game.headers["Result"] = "*"

        print(game, file=out, end="\n\n")
