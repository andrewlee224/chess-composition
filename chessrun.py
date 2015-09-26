"""Module for running the app"""


import argparse

import piececomposer as composer
import pieces as pcs


PIECE_CLASSES = {
    'K': pcs.King,
    'Q': pcs.Queen,
    'B': pcs.Bishop,
    'R': pcs.Rook,
    'N': pcs.Knight
}


def setup_args():
    parser = argparse.ArgumentParser(
        description="""
        Find non-threatening chess piece compositions.

        Pieces are specified by supplying the number of pieces (1-9) and 
        the piece letter.
        K - King
        Q - Queen
        B - Bishop
        R - Rook
        N - Knight

        Dimensions are limited to 16x16.
        E.g.
        chessrun.py 3 3 2N 1R
        """
    )

    parser.add_argument('cols', type=int, help='Chessboard columns')
    parser.add_argument('rows', type=int, help='Chessboard rows')
    parser.add_argument('pieces', nargs='+', help='List of pieces')

    args = parser.parse_args()

    if args.cols < 0 <= 16:
        print("Cols should be a positive integer less than 17")
        return False
    if args.rows < 0 <= 16:
        print("Rows should be a positive integer less than 17")
        return False

    piece_types = []
    for part in args.pieces:
        #import ipdb
        #ipdb.set_trace()
        if not len(part) == 2:
            print("Only two characters per piece declaration are allowed")
            return False
        if not part[0].isdigit():
            print(
                "Make sure that number of pieces appears before piece symbol")
            return False
        if not part[1] in PIECE_CLASSES:
            print("Make sure that proper piece symbol is used")
            return False

        count = int(part[0])
        PieceClass = PIECE_CLASSES[part[1]]

        part_list = [PieceClass] * count
        piece_types.extend(part_list)

    return args.rows, args.cols, piece_types


def main():
    arguments = setup_args()

    if not arguments:
        return

    rows, cols, piece_types = arguments

    piece_composer = composer.PieceComposer(
        rows, cols, piece_types
    )

    piece_composer.compute()

    print("Found {} solutions".format(
        len(piece_composer.found_compositions)
    ))


if __name__ == '__main__':
    main()
