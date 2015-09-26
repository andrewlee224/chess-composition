import nose.tools as nt

from .. import pieces as pcs
from .. import piececomposer as comp


def integration_3x3_test():
    expected_compositions = set((
        frozenset((
            (pcs.Rook, 1, 0), (pcs.King, 0, 2), (pcs.King, 2, 2)
        )),
        frozenset((
            (pcs.Rook, 0, 1), (pcs.King, 2, 0), (pcs.King, 2, 2)
        )),
        frozenset((
            (pcs.Rook, 1, 2), (pcs.King, 0, 0), (pcs.King, 2, 0)
        )),
        frozenset((
            (pcs.Rook, 2, 1), (pcs.King, 0, 0), (pcs.King, 0, 2)
        ))
    ))

    piece_composer = comp.PieceComposer(
        3, 3,
        (pcs.Rook, pcs.King, pcs.King)
    )

    piece_composer.compute()

    nt.assert_equal(piece_composer.found_compositions, expected_compositions)
