from . import PieceColor, BlackPieceId, WhitePieceId, BlackPieceOriginalPosition, WhitePieceOriginalPosition
from . import Rook, Knight, Pawn, Queen, King, Bishop


class ChessBoard(object):
  def __init__(self, width, height, now_turn):
    self.pieces = {}
    self.width = width
    self.height = height
    self.length = max(width, height)
    self.turn = now_turn

  @staticmethod
  def new_8x8_board():
    chess_board = ChessBoard(8, 8, PieceColor.WHITE)
    chess_board.__start_anew_8x8()
    return chess_board

  def __start_anew_8x8(self):
    self.pieces.clear()
    self.pieces.update({
      BlackPieceOriginalPosition.ROOK_1_ORIGINAL_POSITION: Rook(PieceColor.BLACK, BlackPieceId.ROOK_1),
      BlackPieceOriginalPosition.KNIGHT_1_ORIGINAL_POSITION: Knight(PieceColor.BLACK, BlackPieceId.KNIGHT_1),
      BlackPieceOriginalPosition.BISHOP_1_ORIGINAL_POSITION: Bishop(PieceColor.BLACK, BlackPieceId.BISHOP_1),
      BlackPieceOriginalPosition.QUEEN_ORIGINAL_POSITION: Queen(PieceColor.BLACK, BlackPieceId.QUEEN),
      BlackPieceOriginalPosition.KING_ORIGINAL_POSITION: King(PieceColor.BLACK, BlackPieceId.KING),
      BlackPieceOriginalPosition.BISHOP_2_ORIGINAL_POSITION: Bishop(PieceColor.BLACK, BlackPieceId.BISHOP_2),
      BlackPieceOriginalPosition.KNIGHT_2_ORIGINAL_POSITION: Knight(PieceColor.BLACK, BlackPieceId.KNIGHT_2),
      BlackPieceOriginalPosition.ROOK_2_ORIGINAL_POSITION: Rook(PieceColor.BLACK, BlackPieceId.ROOK_2),
      BlackPieceOriginalPosition.PAWN_1_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_1),
      BlackPieceOriginalPosition.PAWN_2_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_2),
      BlackPieceOriginalPosition.PAWN_3_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_3),
      BlackPieceOriginalPosition.PAWN_4_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_4),
      BlackPieceOriginalPosition.PAWN_5_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_5),
      BlackPieceOriginalPosition.PAWN_6_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_6),
      BlackPieceOriginalPosition.PAWN_7_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_7),
      BlackPieceOriginalPosition.PAWN_8_ORIGINAL_POSITION: Pawn(PieceColor.BLACK, BlackPieceId.PAWN_8),
      WhitePieceOriginalPosition.ROOK_1_ORIGINAL_POSITION: Rook(PieceColor.WHITE, WhitePieceId.ROOK_1),
      WhitePieceOriginalPosition.KNIGHT_1_ORIGINAL_POSITION: Knight(PieceColor.WHITE, WhitePieceId.KNIGHT_1),
      WhitePieceOriginalPosition.BISHOP_1_ORIGINAL_POSITION: Bishop(PieceColor.WHITE, WhitePieceId.BISHOP_1),
      WhitePieceOriginalPosition.QUEEN_ORIGINAL_POSITION: Queen(PieceColor.WHITE, WhitePieceId.QUEEN),
      WhitePieceOriginalPosition.KING_ORIGINAL_POSITION: King(PieceColor.WHITE, WhitePieceId.KING),
      WhitePieceOriginalPosition.BISHOP_2_ORIGINAL_POSITION: Bishop(PieceColor.WHITE, WhitePieceId.BISHOP_2),
      WhitePieceOriginalPosition.KNIGHT_2_ORIGINAL_POSITION: Knight(PieceColor.WHITE, WhitePieceId.KNIGHT_2),
      WhitePieceOriginalPosition.ROOK_2_ORIGINAL_POSITION: Rook(PieceColor.WHITE, WhitePieceId.ROOK_2),
      WhitePieceOriginalPosition.PAWN_1_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_1),
      WhitePieceOriginalPosition.PAWN_2_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_2),
      WhitePieceOriginalPosition.PAWN_3_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_3),
      WhitePieceOriginalPosition.PAWN_4_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_4),
      WhitePieceOriginalPosition.PAWN_5_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_5),
      WhitePieceOriginalPosition.PAWN_6_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_6),
      WhitePieceOriginalPosition.PAWN_7_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_7),
      WhitePieceOriginalPosition.PAWN_8_ORIGINAL_POSITION: Pawn(PieceColor.WHITE, WhitePieceId.PAWN_8)
    })

  def move(self, before, after):
    point = 0
    if after in self.pieces:
      point = self.pieces.pop(after).point()
    self.pieces[after] = self.pieces.pop(before)
    self.pieces[after].has_moved = True
    return point

  def in_bounds(self, x, y):
    return 0 <= x < self.height and 0 <= y < self.width

  def __repr__(self):
    ret = []
    for i in range(self.height):
      line = []
      for j in range(self.width):
        if (i, j) in self.pieces:
          line.append(repr(self.pieces[i, j]))
        else:
          line.append(".")
      ret.append("".join(line))
    return "\n".join(ret)

  def is_not_occupied(self, position):
    return position in self.pieces
