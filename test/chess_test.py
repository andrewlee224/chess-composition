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


def king_compute_moves_test():
    expected_threatened_positions = {
        (0, 1), (0, 2), (1, 1), (2, 1), (2, 2)
    }

    actual_threatened_positions = (
        pcs.King.compute_possible_moves((1, 2), 3, 3)
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

    expected_blocked_positions = expected_threatened_positions.union(
        {bishop_pos})

    nt.assert_equal(chessboard.blocked_positions, expected_blocked_positions)


def multiple_threatened_positions_test():
    chessboard = csb.Chessboard(rows=7, cols=7)
    rook1 = pcs.Rook()
    rook2 = pcs.Rook()

    chessboard.add(rook1, (0, 0))
    chessboard.add(rook2, (6, 6))

    nt.assert_equal(chessboard.threatened_dict[(6, 0)], 2)

    chessboard.remove(rook1)
    chessboard.remove(rook2)

    nt.assert_equal(chessboard.threatened_dict[(6, 0)], 0)
    nt.assert_not_in(chessboard.blocked_positions, (6, 0))
