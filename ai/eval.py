from enum import Enum
import numpy as np
from constants import Piece, Color

PAWN_VALUE = 100
KNIGHT_VALUE = 350
BISHOP_VALUE = 350
ROOK_VALUE = 525
QUEEN_VALUE = 1000


class Score(Enum):
    PAWN = np.int32(100)
    KNIGHT = np.int32(350)
    BISHOP = np.int32(350)
    ROOK = np.int32(525)
    QUEEN = np.int32(1000)
    KING = np.int32(10000)


def evaluate(board):
    print(eval_all_pieces(board))

def eval_piece(board, piece):
    return np.int32(board.pieces[Color.WHITE][piece].item().bit_count()) - np.int32(board.pieces[Color.BLACK][piece].item().bit_count())


def eval_all_pieces(board):
    return(
        Score.PAWN.value * eval_piece(board, Piece.PAWN) +
        Score.KNIGHT.value * eval_piece(board, Piece.KNIGHT) +
        Score.BISHOP.value * eval_piece(board, Piece.BISHOP) +
        Score.ROOK.value * eval_piece(board, Piece.ROOK) +
        Score.QUEEN.value * eval_piece(board, Piece.QUEEN) +
        Score.KING.value * eval_piece(board, Piece.KING)
    )