from . import ChessBoard
from . import WhitePieceId, WhitePieceOriginalPosition, BlackPieceId, BlackPieceOriginalPosition, PieceColor


# Actions
class Move:
  pass


class SingleMove(Move):
  def __init__(self, piece, before, after):
    self.piece = piece
    self.before = before
    self.after = after


class CastlingRight(Move):
  def __init__(self, color):
    self.color = color


class CastlingLeft(Move):
  def __init__(self, color):
    self.color = color


# Game State
class GameState(object):
  def __init__(self, board, last_move, prev_state):
    self.prev_state = prev_state
    self.last_move = last_move
    self.board = board


class ChessGame(object):
  def __init__(self):
    self.board = ChessBoard.new_8x8_board()

  def possible_moves(self, color, prev_state=None):
    # All possible moves
    current_position = {}
    my_moves = []
    op_attack = set()
    for position, piece in self.board.pieces.items():
      current_position[position] = position
      if piece.color == color:
        possible_positions = piece.possible_moves(position, self.board)
        for possible_position in possible_positions:
          my_moves[piece] = SingleMove(piece, position, possible_position)
      else:
        for attacked_position in piece.possible_moves(position, self.board):
          op_attack.add(attacked_position)

    # Filtering moves
    legal_moves = []

    # Check for castling?
    def positions_are_empty_and_not_under_attack(xs):
      return all([self.board.is_not_occupied(x) and x not in op_attack for x in xs])

    PieceId = WhitePieceId if color == PieceColor.WHITE else BlackPieceId
    OriginalPiecePosition = WhitePieceOriginalPosition if color == PieceColor.WHITE else BlackPieceOriginalPosition

    king_position = current_position[PieceId.KING]
    king = self.board.pieces[king_position]
    if not king.has_moved and king_position not in op_attack:
      right_empty = positions_are_empty_and_not_under_attack([
        OriginalPiecePosition.KNIGHT_2_ORIGINAL_POSITION,
        OriginalPiecePosition.BISHOP_2_ORIGINAL_POSITION
      ])
      left_empty = positions_are_empty_and_not_under_attack([
        OriginalPiecePosition.KNIGHT_1_ORIGINAL_POSITION,
        OriginalPiecePosition.BISHOP_1_ORIGINAL_POSITION,
        OriginalPiecePosition.QUEEN_ORIGINAL_POSITION
      ])

      # Right castling
      if not self.board.pieces[PieceId.ROOK_2].has_moved and right_empty:
        legal_moves.append(CastlingRight(color))

      # Left castling
      if not self.board.pieces[PieceId.ROOK_1].has_moved and left_empty:
        legal_moves.append(CastlingRight(color))

    return legal_moves
