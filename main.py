import chess
import pprint

game = chess.ChessGame()
pprint.pprint(game.possible_moves(chess.pieces))
pprint.pprint(game.possible_moves(chess.PieceColor.BLACK))

