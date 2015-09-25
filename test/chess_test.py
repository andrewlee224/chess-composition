import nose as ns

from .. import pieces as pcs
from .. import chessboard as csb


def bishop_move_test():
    chessboard = csb.Chessboard(rows=7, cols=7)
    bishop = pcs.Bishop()
    bishop_pos = (3, 3)
    chessboard.add(bishop, row=bishop_pos[0], col=bishop_pos[1])

    expected_possible_positions = {
        # first diagonal (top-left to bottom-right)
        (0, 0), (1, 1), (2, 2),
        (4, 4), (5, 5), (6, 6)
        # second diagonal (bottom-left to top-right)
        (6, 0), (5, 1), (4, 2),
        (2, 4), (1, 5), (0, 6)
    }

    expected_blocked_positions = expected_possible_positions + bishop_pos

    ns.assert_equal(chessboard.blocked_positions, expected_blocked_positions)
