import math
import logging
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

        self.pieces = deque(
            sorted(
                self.pieces, key=lambda piece: piece.sort_order, reverse=True)
        )
        self.used_pieces = deque([])

        self.found_compositions = set()

        self.recursions_completed = -1
        self.total_recursions = (
            math.factorial(len(self.pieces)) * self.chessboard._num_fields)

    def find_composition(self):
        logging.debug("\n===== Entering find_composition")
        logging.debug("Left pieces: {}".format(self.pieces))
        logging.debug("Used pieces: {}".format(self.used_pieces))

        self.recursions_completed += 1
        if (self.recursions_completed % 100) == 0:
            print("Completed {:.2%}".format(
                self.recursions_completed/float(self.total_recursions)
            ))

        if not self.pieces:
            self.found_compositions.add(
                self.extract_composition(self.chessboard)
            )

            return

        for j in range(self.chessboard._rows):
            for i in range(self.chessboard._cols):
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
