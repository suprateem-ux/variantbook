import chess
import chess.polyglot
import chess.pgn

BOOK_PATH = "books/antichess.bin"
OUTPUT_PATH = "output/antichess.pgn"
GAMES = 100  # Number of games to generate
MAX_MOVES = 40  # Limit moves per game

with open(BOOK_PATH, "rb") as book_file:
    reader = chess.polyglot.Reader(book_file)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        for game_index in range(GAMES):
            board = chess.Board(variant="antichess")  # For Antichess variant
            game = chess.pgn.Game()
            node = game

            for _ in range(MAX_MOVES):
                try:
                    entry = reader.weighted_choice(board)
                    move = entry.move()
                    board.push(move)
                    node = node.add_variation(move)
                except IndexError:
                    break  # No more book moves

            game.headers["Event"] = "Antichess Book Extraction"
            game.headers["Site"] = "Generated from Polyglot"
            game.headers["Round"] = str(game_index + 1)
            game.headers["White"] = "Book"
            game.headers["Black"] = "Book"
            game.headers["Result"] = "*"

            print(game, file=out, end="\n\n")
