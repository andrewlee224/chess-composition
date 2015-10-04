class Piece(object):
    """Class for a chessboard piece

    A chessboard piece can compute it's absolute (that is, relative to the
    chessboard and not relative to itself) possible moves on a given
    chessboard.

    RELATIVE_MOVES is a 3-tuple which specifies the possible moves relative
    to the piece itself. The tuple has (y, x, scale) format, where
        y - specifies the row offset in the down direction relative to piece
            position
        x - specifies the column offset in the right direction relative to
            piece position
        scale - a boolean value which informs whether the relative move should
            be scaled - that is whether the relative move can be repeated
            on the chessboard until encountering the chessboard border.
            This is useful for pieces like Bishop, Rook, or Queen which can
            move essentially any distance limited only by the chessboard
            dimensions.
    """

    RELATIVE_MOVES = (0, 0, False)

    def __init__(self, sort_order=None):
        # stored absolute possible moves in relation
        # to some specific chessboard
        self._possible_moves = None
        self.bound_chessboard = None
        self.position = None

        # this governs the priority of the piece when trying different
        # pieces combinations on the chessboard - usually the pieces with
        # more moves available should be put first
        self.sort_order = sort_order

    def reset(self):
        """Equivalent of taking a piece off a chessboard"""
        self.bound_chessboard = None
        self.position = None
        self._possible_moves = None

    @property
    def possible_moves(self):
        """Lazily evaluate and cache possible moves of a piece."""
        if self.bound_chessboard is None or self.position is None:
            return None
        if self._possible_moves is not None:
            return self._possible_moves

        self._possible_moves = self.compute_possible_moves(
            self.position,
            self.bound_chessboard.rows,
            self.bound_chessboard.cols
        )

        return self._possible_moves

    @property
    def blocked_moves(self):
        """Get positions at which other pieces cannot be put.

        The blocked positions are positions which are threatened by the
        piece and the occupied position.
        """
        if self.position is None:
            return None

        return self.possible_moves + self.position

    @classmethod
    def compute_possible_moves(cls, pos, csb_rows, csb_cols):
        """Compute possible absolute coordinates of moves for a piece."""
        y, x = pos

        possible_moves = set()

        for rel_y, rel_x, scale in cls.RELATIVE_MOVES:
            if not scale:
                # check if position not out of chessboard bounds
                x_candidate, y_candidate = x + rel_x, y + rel_y
                if not (0 <= x_candidate < csb_cols
                        and 0 <= y_candidate < csb_rows):
                    continue
                possible_moves.add((y_candidate, x_candidate))
            else:
                # scale the move until out of bounds
                out_of_bounds = False
                factor = 1
                while not out_of_bounds:
                    x_candidate, y_candidate = (
                        x + rel_x*factor, y + rel_y*factor)
                    if not (0 <= x_candidate < csb_cols
                            and 0 <= y_candidate < csb_rows):
                        out_of_bounds = True
                        break
                    possible_moves.add((y_candidate, x_candidate))
                    factor += 1

        return possible_moves


class Bishop(Piece):
    """Represents Bishop piece."""

    NAME = "Bishop"

    RELATIVE_MOVES = (
        (-1, -1, True), (-1, 1, True),
        (1, -1, True), (1, 1, True)
    )


class Rook(Piece):
    """Represents Rook piece."""

    NAME = "Rook"

    RELATIVE_MOVES = (
        (0, -1, True), (-1, 0, True),
        (0, 1, True), (1, 0, True)
    )


class Queen(Piece):
    """Represents Queen piece."""

    NAME = "Queen"

    RELATIVE_MOVES = Bishop.RELATIVE_MOVES + Rook.RELATIVE_MOVES


class Knight(Piece):
    """Represents Knight piece."""

    NAME = "Knight"

    RELATIVE_MOVES = (
        (-1, -2, False), (-2, -1, False),
        (-2, 1, False), (-1, 2, False),
        (1, 2, False), (2, 1, False),
        (2, -1, False), (1, -2, False)
    )


class King(Piece):
    """Represents King piece."""

    NAME = "King"

    RELATIVE_MOVES = (
        (-1, -1, False), (-1, 0, False), (-1, 1, False),
        (0, -1, False), (0, 1, False),
        (1, -1, False), (1, 0, False), (1, 1, False)
    )
