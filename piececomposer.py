import math
import logging
import time
from collections import deque

import pieces as pcs
import chessboard as csb


class PieceComposer(object):

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
            self.chessboard._opt_rows if self.chessboard._is_square
            else self.chessboard._rows)
        self.opt_i_range = range(
            self.chessboard._opt_cols if self.chessboard._is_square
            else self.chessboard._cols)

        self.j_range = range(self.chessboard._rows)
        self.i_range = range(self.chessboard._cols)

        self.pieces = deque(
            sorted(
                self.pieces, key=lambda piece: piece.sort_order, reverse=True)
        )
        self.used_pieces = deque([])

        self.found_compositions = set()

        self.recursions_completed = -1
        self.top_recursive_calls = 0
        self.prev_top_call_time = None
        self.total_recursions = (
            math.factorial(len(self.pieces)) * self.chessboard._num_fields)

    def find_composition(self):
        logging.debug("\n===== Entering find_composition")
        logging.debug("Left pieces: {}".format(self.pieces))
        logging.debug("Used pieces: {}".format(self.used_pieces))

        if len(self.used_pieces) == 1:
            self.top_recursive_calls += 1
            print("Entered {}/{} top recursive call".format(
                self.top_recursive_calls,
                self.chessboard._opt_rows * self.chessboard._opt_cols))
            new_time = time.time()
            if self.prev_top_call_time is not None:
                print("Time from previous top call: {}".format(
                    new_time - self.prev_top_call_time))
            self.prev_top_call_time = new_time

        if not self.pieces:
            self.found_compositions.add(
                self.extract_composition(self.chessboard)
            )

            return

        if len(self.used_pieces) == 0:
            j_range = self.opt_j_range
            i_range = self.opt_i_range
        else:
            j_range = self.j_range
            i_range = self.i_range
        #j_range = (
        #    self.chessboard._opt_rows if len(self.used_pieces) == 0
        #    else self.chessboard._rows)
        #i_range = (
        #    self.chessboard._opt_cols if len(self.used_pieces) == 0
        #    else self.chessboard._cols)


        for j in j_range:
            for i in i_range:
                logging.debug("Considering {} at {}, {}".format(
                    self.pieces[-1], j, i))
                if (j, i) in self.chessboard.blocked_positions:
                    logging.debug("\tPosition blocked")
                    continue
                if not self.pieces:
                    logging.debug("\tNo remaining pieces")
                    continue
                add_status = self.chessboard.add(self.pieces[-1], (j, i))
                if add_status:
                    logging.debug(
                        "Added {} on {}, {}".format(self.pieces[-1], j, i))
                    piece = self.pieces.pop()
                    self.used_pieces.append(piece)

                    self.find_composition()
                    logging.debug("=== Returned from find_composition")
                    last_piece = self.used_pieces.pop()
                    self.pieces.append(last_piece)
                    self.chessboard.remove(last_piece)

    @staticmethod
    def extract_composition(chessboard):
        composition = frozenset({
            (piece.__class__, piece.position[0], piece.position[1])
            for piece in chessboard.pieces
        })

        return composition

    def rotate_composition(self, composition):
        """Rotate all pieces on a chessboard by 90 degrees

        This is useful when optimizing square chessboard compositions
        by leveraging the symmetry of solutions
        """

        cols = self.chessboard._cols

        center_col = None if (cols % 2 == 0) else (cols-1)/2

        new_composition = frozenset({
            (piece, cols - 1 - x, y) if not center_col or x != center_col
            else (piece, x, y)
            for piece, y, x in composition
        })

        return new_composition

    def extract_symmetric_compositions(self):
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
        self.find_composition()

        if self.chessboard._is_square:
            self.extract_symmetric_compositions()
