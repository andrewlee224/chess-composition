import nose.tools as nt

from .. import pieces as pcs
from .. import chessboard as csb


def bishop_compute_moves_test():
    expected_threatened_positions = {
        # first diagonal (top-left to bottom-right)
        (0, 0), (1, 1), (2, 2),
        (4, 4), (5, 5), (6, 6),
        # second diagonal (bottom-left to top-right)
        (6, 0), (5, 1), (4, 2),
        (2, 4), (1, 5), (0, 6)
    }

    actual_threatened_positions = (
        pcs.Bishop.compute_possible_moves((3, 3), 7, 7)
    )

    nt.assert_equal(
        expected_threatened_positions,
        actual_threatened_positions
    )


def bishop_add_test():
    chessboard = csb.Chessboard(rows=7, cols=7)
    bishop = pcs.Bishop()
    bishop_pos = (3, 3)
    chessboard.add(bishop, bishop_pos)

    expected_threatened_positions = {
        # first diagonal (top-left to bottom-right)
        (0, 0), (1, 1), (2, 2),
        (4, 4), (5, 5), (6, 6),
        # second diagonal (bottom-left to top-right)
        (6, 0), (5, 1), (4, 2),
        (2, 4), (1, 5), (0, 6)
    }

    expected_blocked_positions = expected_threatened_positions.add(bishop_pos)

    nt.assert_equal(chessboard.blocked_positions, expected_blocked_positions)
