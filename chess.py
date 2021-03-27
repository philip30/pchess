import enum


class ChessBoard(object):
  def __init__(self, width, height, now_turn):
    self.pieces = {}
    self.width = width
    self.height = height
    self.length = max(width, height)
    self.turn = now_turn

  @staticmethod
  def new_8x8_board():
    chess_board = ChessBoard(8, 8, Color.WHITE)
    chess_board.__start_anew_8x8()
    return chess_board

  def __start_anew_8x8(self):
    self.pieces.clear()
    self.pieces.update({
      (0, 0): Rook(Color.BLACK),
      (0, 1): Knight(Color.BLACK),
      (0, 2): Bishop(Color.BLACK),
      (0, 3): Queen(Color.BLACK),
      (0, 4): King(Color.BLACK),
      (0, 5): Bishop(Color.BLACK),
      (0, 6): Knight(Color.BLACK),
      (0, 7): Rook(Color.BLACK),
      (7, 0): Rook(Color.WHITE),
      (7, 1): Knight(Color.WHITE),
      (7, 2): Bishop(Color.WHITE),
      (7, 3): Queen(Color.WHITE),
      (7, 4): King(Color.WHITE),
      (7, 5): Bishop(Color.WHITE),
      (7, 6): Knight(Color.WHITE),
      (7, 7): Rook(Color.WHITE)
    })

    for j in range(8):
      self.pieces[1, j] = Pawn(Color.BLACK)
      self.pieces[6, j] = Pawn(Color.WHITE)

  def move(self, before, after):
    point = 0
    if after in self.pieces:
      point = self.pieces.pop(after).point()
    self.pieces[after] = self.pieces.pop(before)
    return point

  def in_bounds(self, x, y):
    return 0 <= x < self.height and 0 <= y <= self.width

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


class Color(enum.Enum):
  WHITE = 0
  BLACK = 1


class Piece(object):
  def __init__(self, color: Color):
    self.color = color

  def point(self) -> int: raise NotImplementedError
  def symbol(self) -> str: raise NotImplementedError

  def __repr__(self):
    if self.color == Color.WHITE:
      return self.symbol().upper()
    else:
      return self.symbol().lower()

  def possible_moves(self, before, board: ChessBoard):
    ret = []
    x, y = before
    self.possible_move_fn(x, y, board, self.color, ret)
    return ret

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    raise NotImplementedError

  @staticmethod
  def move_and_check_stop(board, next_pos, color, ret):
    if board.in_bounds(*next_pos):
      # Something in my way
      if next_pos in board.pieces:
        # enemy, kill!
        if color != board.pieces[next_pos]:
          ret.append(next_pos)
        # Can't move further
        return True
      else:
        # Nothing in my way
        ret.append(next_pos)
        # Should not stop.
        return False
    else:
      # Out of bounds
      return True


class Pawn(Piece):
  def __init__(self, color):
    super().__init__(color)

  def point(self): return 1
  def symbol(self): return "p"

  @staticmethod
  def possible_move_fn(x, y, board, color, ret):
    if color == Color.WHITE:
      dy = 1
    else:
      dy = -1

    # Single Move
    if (x, y+dy) not in board.pieces:
      ret.append((x, y+dy))
    # Double Move
    if (x, y+2*dy) not in board.pieces:
      if (color == Color.WHITE and y == 6) or (color == Color.BLACK and y == 1):
        ret.append((x, y+2*dy))

    # Killing
    if (x-1, y+dy) in board.pieces:
      ret.append((x-1, y+dy))
    if (x+1, y+dy) in board.pieces:
      ret.append((x+1, y+dy))

    # TODO CHECK for double move after advanced position


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
        if Piece.move_and_check_stop(board, (x, y + c * dy), ret, color):
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


# Action
class Move(object):
  def __init__(self, moves):
    self.moves = moves


class ChessGame(object):
  def __init__(self):
    self.board = ChessBoard.new_8x8_board()
    self.under_attack = {}

  def possible_moves(self, color):
    moves = []
    for position, piece in self.board.pieces.items():
      if piece.color == color:
        moves.append(piece.possible_moves(position, self.board))