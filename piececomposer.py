import logging
import time
from collections import deque

import pieces as pcs
import chessboard as csb


class PieceComposer(object):
    """Compute all compositions of non-threatening pieces positions.

    Given the chessboard dimensions and and iterable of desired piece types
    computes all possible compositions of pieces in which none of them
    threatens any other. A piece threatens another piece if it can capture
    the other piece within one move.
    """
    DEFAULT_COMPOSE_ORDER = (
        pcs.Queen, pcs.Bishop, pcs.Rook, pcs.Knight, pcs.King
    )

    def __init__(self, rows, cols, piece_types):
        self.chessboard = csb.Chessboard(rows, cols, add_threatened=False)
        self.examined_fields = 0
        self.pieces = [
            PieceClass(sort_order=self.DEFAULT_COMPOSE_ORDER.index(PieceClass))
            for PieceClass in piece_types
        ]
        self.opt_j_range = range(
            self.chessboard.opt_rows if self.chessboard.is_square
            else self.chessboard.rows)
        self.opt_i_range = range(
            self.chessboard.opt_cols if self.chessboard.is_square
            else self.chessboard.cols)

        self.j_range = range(self.chessboard.rows)
        self.i_range = range(self.chessboard.cols)

        self.pieces = deque(
            sorted(
                self.pieces, key=lambda piece: piece.sort_order, reverse=True)
        )
        # this is used instead of chessboards pieces for
        # performance reasons
        self.all_pieces = frozenset(self.pieces)
        self.used_pieces = deque([])

        self.found_compositions = set()
        self.num_found = 0

        self.top_recursive_calls = 0
        self.prev_top_call_time = None

    def find_composition(self):
        """Find a next available position for a given chessboard.

        Finds a next available position given a chessboard and a piece.
        This data is stored as object state and updated accordingly.
        This is a recursive function. It is called repeatedly
        for every newly considered piece - therefore the maximum recursion
        depth is the maximum number of considered pieces - i.e. all the given
        pieces in self.all_pieces.

        This function uses an optimization when dealing with square
        chessboards - because of a symmetry of solutions one can consider
        only the first quadrant of the board in the first recursion.
        In this approach it is necessary to iterate through those solutions
        and find the symmetric ones by rotating the original solutions by
        90, 180 and 270 degrees.
        """
        logging.debug("\n===== Entering find_composition")
        logging.debug("Left pieces: %s", self.pieces)
        logging.debug("Used pieces: %s", self.used_pieces)

        if len(self.used_pieces) == 1:
            self.top_recursive_calls += 1
            print("Entered {}/{} top recursive call".format(
                self.top_recursive_calls,
                self.chessboard.opt_rows * self.chessboard.opt_cols))
            new_time = time.time()
            if self.prev_top_call_time is not None:
                print("Time from previous top call: {}".format(
                    new_time - self.prev_top_call_time))
            self.prev_top_call_time = new_time

        if not self.pieces:
            self.num_found += 1
            self.found_compositions.add(
                self.extract_composition()
            )

            return

        if len(self.used_pieces) == 0:
            j_range = self.opt_j_range
            i_range = self.opt_i_range
        else:
            j_range = self.j_range
            i_range = self.i_range

        for j in j_range:
            for i in i_range:
                logging.debug(
                    "Considering %s at %s, %s", self.pieces[-1], j, i)
                if (j, i) in self.chessboard.blocked_positions:
                    logging.debug("\tPosition blocked")
                    continue

                add_status = self.chessboard.add(self.pieces[-1], (j, i))
                if add_status:
                    logging.debug(
                        "Added %s on %s, %s", self.pieces[-1], j, i)
                    piece = self.pieces.pop()
                    self.used_pieces.append(piece)

                    self.find_composition()
                    logging.debug("=== Returned from find_composition")
                    last_piece = self.used_pieces.pop()
                    self.pieces.append(last_piece)
                    self.chessboard.remove(last_piece)

    def extract_composition(self):
        """Extract the chess pieces composition from the chessboard."""
        composition = frozenset((
            (piece.__class__, piece.position[0], piece.position[1])
            for piece in self.all_pieces
        ))

        return composition

    def rotate_composition(self, composition):
        """Rotate all pieces on a square chessboard by 90 degrees.

        This is useful when optimizing square chessboard compositions
        by leveraging the symmetry of solutions.
        The rotation direction is counter-clockwise.
        """

        cols = self.chessboard.cols

        center_col = None if (cols % 2 == 0) else (cols-1)/2

        new_composition = frozenset((
            (piece, cols - 1 - x, y) if not center_col or x != center_col
            else (piece, x, y)
            for piece, y, x in composition
        ))

        return new_composition

    def extract_symmetric_compositions(self):
        """Extract symmetric composition solutions given the existing ones."""
        unique_new = set()

        print("Computing symmetric solutions..")
        for composition in self.found_compositions:
            new_composition1 = self.rotate_composition(composition)
            new_composition2 = self.rotate_composition(new_composition1)
            new_composition3 = self.rotate_composition(new_composition2)

            unique_new.update(
                {
                    new_composition1,
                    new_composition2,
                    new_composition3
                }.difference(
                    self.found_compositions
                )
            )
        print("Done")

        self.found_compositions.update(unique_new)

    def compute(self):
        """Find compositions and symmetric solutions."""
        self.find_composition()

        if self.chessboard.is_square:
            self.extract_symmetric_compositions()
