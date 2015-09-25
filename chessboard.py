class Chessboard(object):
    """Represents chessboard

    The chessboard positions are accessed using a (row, column) convention
    as is customary with matrices. The zeroth row is the top row, and the
    zeroth column is the left-most column.
    Note that this way of indexing is a bit different than standard (x, y)
    in Cartesian coordinate systems - the order of coordinates is swapped.
    I have chosen this convention to enable easy transition to NumPy ndarrays
    if need arises.

    --> x
      _______
    | |_|_|_|
    | |_|_|_|   (row, column) = (y, x)
    v |_|_|_|
    y

    """

    def __init__(self, rows, cols, add_threatened=False):
        self.pieces = []
        self.occupied_positions = set()
        self.threatened_positions = set()
        self._blocked_positions = set()
        self._rows = rows
        self._cols = cols
        self.add_threatened = add_threatened

    @property
    def blocked_positions(self):
        if not self.add_threatened:
            return self.occupied_positions.update(self.threatened_positions)

        return self.occupied_positions

    def add(self, piece, pos):

        if pos in self.occupied_positions:
            return False

        if pos in self.threatened_positions and not self.add_threatened:
            return False

        piece.bound_chessboard = self
        piece.position = pos

        new_threatened_positions = {
            thr_pos for thr_pos in piece.possible_moves
            if thr_pos not in self.occupied_positions
        }

        self.threatened_positions.update(new_threatened_positions)
        self.occupied_positions.add(pos)

        self.pieces.append(piece)

        return True
