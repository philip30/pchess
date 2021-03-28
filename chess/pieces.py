import enum

from . import ChessBoard


class PieceId(enum.Enum):
  NONE = -1


class WhitePieceId(PieceId):
  PAWN_1 = 0
  PAWN_2 = 1
  PAWN_3 = 2
  PAWN_4 = 3
  PAWN_5 = 4
  PAWN_6 = 5
  PAWN_7 = 6
  PAWN_8 = 7
  ROOK_1 = 8
  KNIGHT_1 = 9
  BISHOP_1 = 10
  QUEEN = 11
  KING = 12
  BISHOP_2 = 13
  KNIGHT_2 = 14
  ROOK_2 = 15


class BlackPieceId(PieceId, enum):
  PAWN_1 = 16
  PAWN_2 = 17
  PAWN_3 = 18
  PAWN_4 = 19
  PAWN_5 = 20
  PAWN_6 = 21
  PAWN_7 = 22
  PAWN_8 = 23
  ROOK_1 = 24
  KNIGHT_1 = 25
  BISHOP_1 = 26
  QUEEN = 27
  KING = 28
  BISHOP_2 = 29
  KNIGHT_2 = 30
  ROOK_2 = 31


class WhitePieceOriginalPosition(object):
  PAWN_1_ORIGINAL_POSITION = (6, 0)
  PAWN_2_ORIGINAL_POSITION = (6, 1)
  PAWN_3_ORIGINAL_POSITION = (6, 2)
  PAWN_4_ORIGINAL_POSITION = (6, 3)
  PAWN_5_ORIGINAL_POSITION = (6, 4)
  PAWN_6_ORIGINAL_POSITION = (6, 5)
  PAWN_7_ORIGINAL_POSITION = (6, 6)
  PAWN_8_ORIGINAL_POSITION = (6, 7)
  ROOK_1_ORIGINAL_POSITION = (7, 0)
  KNIGHT_1_ORIGINAL_POSITION = (7, 1)
  BISHOP_1_ORIGINAL_POSITION = (7, 2)
  QUEEN_ORIGINAL_POSITION = (7, 3)
  KING_ORIGINAL_POSITION = (7, 4)
  BISHOP_2_ORIGINAL_POSITION = (7, 5)
  KNIGHT_2_ORIGINAL_POSITION = (7, 6)
  ROOK_2_ORIGINAL_POSITION = (7, 7)


class BlackPieceOriginalPosition(object):
  PAWN_1_ORIGINAL_POSITION = (1, 0)
  PAWN_2_ORIGINAL_POSITION = (1, 1)
  PAWN_3_ORIGINAL_POSITION = (1, 2)
  PAWN_4_ORIGINAL_POSITION = (1, 3)
  PAWN_5_ORIGINAL_POSITION = (1, 4)
  PAWN_6_ORIGINAL_POSITION = (1, 5)
  PAWN_7_ORIGINAL_POSITION = (1, 6)
  PAWN_8_ORIGINAL_POSITION = (1, 7)
  ROOK_1_ORIGINAL_POSITION = (0, 0)
  KNIGHT_1_ORIGINAL_POSITION = (0, 1)
  BISHOP_1_ORIGINAL_POSITION = (0, 2)
  QUEEN_ORIGINAL_POSITION = (0, 3)
  KING_ORIGINAL_POSITION = (0, 4)
  BISHOP_2_ORIGINAL_POSITION = (0, 5)
  KNIGHT_2_ORIGINAL_POSITION = (0, 6)
  ROOK_2_ORIGINAL_POSITION = (0, 7)


class PieceColor(enum.Enum):
  WHITE = 0
  BLACK = 1


class Piece(object):
  def __init__(self, color: PieceColor, piece_id: PieceId, has_moved=False):
    self.color = color
    self.piece_id = piece_id
    self.has_moved = has_moved

  def point(self) -> int: raise NotImplementedError
  def symbol(self) -> str: raise NotImplementedError

  def __repr__(self):
    if self.color == PieceColor.WHITE:
      return self.symbol().upper()
    else:
      return self.symbol().lower()

  def __hash__(self):
    return self.piece_id

  def __eq__(self, other):
    return self.piece_id == other.piece_id

  def possible_moves(self, before, board: ChessBoard):
    ret = []
    x, y = before
    self.possible_move_fn(x, y, board, self.color, ret)
    return ret

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    raise NotImplementedError

  @staticmethod
  def move_and_check_stop(board, next_pos, color, ret, can_kill=True, must_kill=False):
    if board.in_bounds(*next_pos):
      # Something in my way
      if next_pos in board.pieces:
        # enemy, kill!
        if color != board.pieces[next_pos].color and can_kill:
          ret.append(next_pos)
        # Can't move further
        return True
      else:
        # nothing in my way
        if not must_kill:
          ret.append(next_pos)
        # Should not stop.
        return False
    else:
      # Out of bounds
      return True


class Pawn(Piece):
  def point(self): return 1
  def symbol(self): return "p"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    if color == PieceColor.WHITE:
      dx = -1
    else:
      dx = 1

    # Single Move
    Pawn.move_and_check_stop(board, (x+dx, y), color, ret, can_kill=False)

    if (color == PieceColor.WHITE and x == 6) or (color == PieceColor.BLACK and x == 1):
      Pawn.move_and_check_stop(board, (x+2*dx, y), color, ret, can_kill=False)

    # Killing
    Pawn.move_and_check_stop(board, (x+dx, y-1), color, ret, must_kill=True)
    Pawn.move_and_check_stop(board, (x+dx, y+1), color, ret, must_kill=True)


class Bishop(Piece):
  def point(self): return 3
  def symbol(self): return "b"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    Bishop.bishop_move(x, y, board, board.length, color, ret)

  @staticmethod
  def bishop_move(x, y, board, length, color, ret):
    for dx in [1, -1]:
      for dy in [1, -1]:
        for c in range(1, length):
          if Piece.move_and_check_stop(board, (x + c * dx, y + c * dy), color, ret):
            break


class Knight(Piece):
  def point(self): return 3
  def symbol(self): return "k"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    for dx, dy in [(-2, -1), (-1, -2), (-2, 1), (-1, 2), (1, 2), (2, 1), (1, -2), (2, -1)]:
      Piece.move_and_check_stop(board, (x + dx, y + dy), color, ret)


class Rook(Piece):
  def point(self): return 5
  def symbol(self): return "r"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    Rook.rook_move(x, y, board, board.length, color, ret)

  @staticmethod
  def rook_move(x, y, board, length, color, ret):
    for dx in [1, -1]:
      for c in range(1, length):
        if Piece.move_and_check_stop(board, (x + c * dx, y), color, ret):
          break

    for dy in [1, -1]:
      for c in range(1, length):
        if Piece.move_and_check_stop(board, (x, y + c * dy), color, ret):
          break


class Queen(Piece):
  def point(self): return 9
  def symbol(self): return "q"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    Rook.rook_move(x, y, board, board.length, color, ret)
    Bishop.bishop_move(x, y, board, board.length, color, ret)


class King(Piece):
  def point(self): return 1000
  def symbol(self): return "k"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    Rook.rook_move(x, y, board, 1, color, ret)
    Bishop.bishop_move(x, y, board, 1, color, ret)

