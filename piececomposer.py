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
        
        self.pieces.sort(key=lambda piece: piece.sort_order, reverse=True)
        self.used_pieces = []

        self.found_compositions = set()

    def find_composition(self):
        #import pdb
        #pdb.set_trace()
        print("\n===== Entering find_composition")
        print("Left pieces: {}".format(self.pieces))
        print("Used pieces: {}".format(self.used_pieces))
        if not self.pieces:
            self.found_compositions.add(
                self.extract_composition(self.chessboard)
            )
            #last_piece = self.used_pieces.pop()
            #self.pieces.append(last_piece)
            #self.chessboard.remove(last_piece)

            return

        for j in range(self.chessboard._rows):
            for i in range(self.chessboard._cols):
                print("Considering {}, {}, {}".format(self.pieces[-1], j, i))
                if (j, i) in self.chessboard.blocked_positions:
                    if (j, i) == (1, 0):
                        print("At 1,0: ")
                        print("threatened_positions: {}".format(
                            self.chessboard.threatened_positions))
                        print("threatened_dict: {}".format(
                            self.chessboard.threatened_dict))
                        print("occupied positions: {}".format(
                            self.chessboard.occupied_positions))
                    print("\tPosition blocked")
                    continue
                if not self.pieces:
                    print("\tNo remaining pieces")
                    continue
                add_status = self.chessboard.add(self.pieces[-1], (j, i))
                if add_status:
                    print("Added {} on {}, {}".format(self.pieces[-1], j, i))
                    piece = self.pieces.pop()
                    self.used_pieces.append(piece)

                    # self.used_pieces.append(piece)
                    # if no more pieces left to put
                    #if not self.pieces:
                        # self.pieces = reversed(self.used_pieces)
                    #else:
                    self.find_composition()
                    print("=== Returned from find_composition")
                    last_piece = self.used_pieces.pop()
                    self.pieces.append(last_piece)
                    print("threatened_dict[(1, 0)] before remove: {}".format(
                        self.chessboard.threatened_dict[(1, 0)]))
                    print("occupied_positions before remove: {}".format(
                        self.chessboard.occupied_positions))
                    self.chessboard.remove(last_piece)
                    print("occupied_positions after remove: {}".format(
                        self.chessboard.occupied_positions))
                    print("threatened_dict after remove: {}".format(
                        self.chessboard.threatened_dict[(1, 0)]))

                #else:
                #    self.pieces.append(self.used_pieces.pop())

    def find_composition_rec(self):
        
        if len(self.used_pieces) == len(self.pieces):
            self.found_compositions.add(
                self.extract_composition(self.chessboard))

        if self.examined_fields == self.chessboard.num_fields:
            return

        # examine fields row by row
        # examined_field = 

    # @staticmethod
    # def find_composition(chessboard, 

    @staticmethod
    def extract_composition(chessboard):
        composition = frozenset({
            (piece.__class__, piece.position[0], piece.position[1]) 
            for piece in chessboard.pieces
        })

        return composition

