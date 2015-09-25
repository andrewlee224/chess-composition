class Piece(object):

    RELATIVE_MOVES = (0, 0, False)

    def __init__(self):
        # stored absolute possible moves in relation
        # to some specific chessboard
        self._possible_moves = None
        self.bound_chessboard = None
        self.position = None

    @property
    def possible_moves(self):
        if self.bound_chessboard is None or self.position is None:
            return None
        if self._possible_moves is not None:
            return self._possible_moves

        self._possible_moves = self.compute_possible_moves(
            self.position,
            self.bound_chessboard._rows,
            self.bound_chessboard._cols
        )

        return self._possible_moves

    @property
    def blocked_moves(self):
        if self.position is None:
            return None

        return self.possible_moves + self.position

    @classmethod
    def compute_possible_moves(cls, pos, csb_rows, csb_cols):
        """Compute possible absolute coordinates of a
        given piece and chessboard

        """
        x, y = pos

        possible_moves = set()

        for rel_x, rel_y, scale in cls.RELATIVE_MOVES:
            if not scale:
                # check if position not out of chessboard bounds
                x_candidate, y_candidate = x + rel_x, y + rel_y
                if not (x_candidate < csb_cols and y_candidate < csb_rows):
                    continue
                possible_moves.add((y_candidate, x_candidate))
            else:
                # scale the move until out of bounds
                out_of_bounds = False
                factor = 1
                while(not out_of_bounds):
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

    RELATIVE_MOVES = (
        (-1, -1, True), (-1, 1, True),
        (1, -1, True), (1, 1, True)
    )


class Rook(Piece):

    RELATIVE_MOVES = (
        (0, -1, True), (-1, 0, True),
        (0, 1, True), (1, 0, True)
    )


class Queen(Piece):

    RELATIVE_MOVES = Bishop.RELATIVE_MOVES + Rook.RELATIVE_MOVES


class Knight(Piece):

    RELATIVE_MOVES = (
        (-1, -2, False), (-2, -1, False),
        (-2, 1, False), (-1, 2, False),
        (1, 2, False), (2, 1, False),
        (2, -1, False), (1, -2, False)
    )


class King(Piece):

    RELATIVE_MOVES = (
        (-1, -1, False), (-1, 0, False), (-1, 1, False),
        (0, -1, False), (0, 1, False),
        (1, -1, False), (1, 0, False), (1, 1, False)
    )
