from collections import defaultdict


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
        # a position may be threatened multiple times, the dict is for keeping
        # track of this number
        self.threatened_dict = defaultdict(lambda: 0)
        self._blocked_positions = set()
        self._rows = rows
        self._cols = cols
        self._num_fields = rows*cols
        self.add_threatened = add_threatened

    @property
    def blocked_positions(self):
        if not self.add_threatened:
            return self.occupied_positions.union(self.threatened_positions)

        return self.occupied_positions

    def add(self, piece, pos):

        if pos in self.occupied_positions:
            return False

        if pos in self.threatened_positions and not self.add_threatened:
            return False

        piece.bound_chessboard = self
        piece.position = pos

        # check if new possible moves don't threaten existing pieces
        if piece.possible_moves.intersection(self.occupied_positions):
            piece.reset()
            return False

        new_threatened_positions = piece.possible_moves

        self.threatened_positions.update(new_threatened_positions)

        # update the threatened positions counts
        for position in new_threatened_positions:
            self.threatened_dict[position] += 1

        self.occupied_positions.add(pos)

        self.pieces.append(piece)

        return True

    def remove(self, piece):
        if piece not in self.pieces:
            return False

        self.occupied_positions.remove(piece.position)

        for position in piece.possible_moves:
            self.threatened_dict[position] -= 1
            if self.threatened_dict[position] == 0:
                self.threatened_positions.remove(position)

        piece.reset()

        return True

