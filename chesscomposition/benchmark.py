"""Simple benchmark to measure the runtime of example chessboards configs"""

import time
import logging

import pieces as pcs
import piececomposer as composer


logging.basicConfig(level=logging.INFO)


BENCH_PARAMS1 = {
    'rows': 3,
    'cols': 3,
    'piece_types': (
        pcs.Rook, pcs.King, pcs.King
    )
}


BENCH_PARAMS2 = {
    'rows': 4,
    'cols': 4,
    'piece_types': (
        pcs.Rook, pcs.Rook, pcs.Knight, pcs.Knight,
        pcs.Knight, pcs.Knight
    )
}


BENCH_PARAMS3 = {
    'rows': 5,
    'cols': 5,
    'piece_types': (
        pcs.King, pcs.Queen,
        pcs.Bishop, pcs.Bishop, pcs.Knight
    )
}


BENCH_PARAMS4 = {
    'rows': 6,
    'cols': 6,
    'piece_types': (
        pcs.King, pcs.Queen,
        pcs.Bishop, pcs.Bishop, pcs.Knight
    )
}


BENCH_PARAMS5 = {
    'rows': 7,
    'cols': 7,
    'piece_types': (
        pcs.King, pcs.King, pcs.Queen, pcs.Queen,
        pcs.Bishop, pcs.Bishop, pcs.Knight
    )
}


def main():
    """Main benchmark function."""
    piece_composer = composer.PieceComposer(**BENCH_PARAMS4)

    time0 = time.time()

    piece_composer.compute()

    time1 = time.time()

    print("Found compositions in {}".format(time1 - time0))
    print(
        "Number of found compositions: {}".format(
            len(piece_composer.found_compositions))
    )

if __name__ == '__main__':
    main()
