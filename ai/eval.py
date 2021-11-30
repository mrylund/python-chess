from aenum import Enum, skip
import numpy as np
from chessboard import ChessBoard
import movegen
from constants import Color, Piece


class Score(Enum):
    PAWN = np.int32(100)
    KNIGHT = np.int32(350)
    BISHOP = np.int32(350)
    ROOK = np.int32(525)
    QUEEN = np.int32(1000)
    KING = np.int32(10000)
    CHECKMATE = np.int32(-1000000)
    CENTER = np.int32(5)

CENTER = np.uint64(0x00003C3C3C3C0000)

MVV_LVA = [
    [15, 14, 13, 12, 11, 10, 0],
    [25, 24, 23, 22, 21, 20, 0],
    [35, 34, 33, 32, 31, 30, 0],
    [45, 44, 43, 42, 41, 40, 0],
    [55, 54, 53, 52, 51, 50, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

class PositionScore(Enum):
    @skip
    class White(Enum):
        PAWN = [
            0, 0, 0, 0, 0, 0, 0, 0,
            -1, -1, 1, 5, 6, 1, -1, -1,
            -4, -4, 0, 4, 6, 0, -4, -4,
            -4, -4, 0, 6, 8, 0, -4, -4,
            -3, -3, 2, 9, 11, 2, -3, -3,
            -2, -2, 4, 12, 15, 4, -2, -2,
            7, 7, 13, 23, 26, 13, 7, 7,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        KNIGHT = [
            -7, -5, -4, -2, -2, -4, -5, -7,
            -5, -3, -1, 0, 0, -1, -3, -5,
            -3, 1, 3, 4, 4, 3, 1, -3,
            0, 5, 8, 9, 9, 8, 5, 0,
            3, 10, 14, 14, 14, 14, 10, 3,
            5, 11, 18, 19, 19, 18, 11, 5,
            1, 4,12, 13, 13, 12, 4, 1,
            -2, 2, 7, 9, 9, 7, 2, -2
        ]
        BISHOP = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 5, 5, 3, 3, 5, 5, 5,
            4, 5, 5, -2, -2, 5, 5, 4,
            4, 5, 6, 8, 8, 6, 5, 4,
            3, 5, 7, 7, 7, 7, 5, 3,
            3, 5, 6, 6, 6, 6, 5, 3,
            4, 7, 7, 7, 7, 7, 7, 4,
            2, 3, 4, 4, 4, 4, 3, 2
        ]
        ROOK = [
            0, 0, 0, 0, 0, 0, 0, 0,
            3, 4, 4, 6, 6, 4, 4, 3,
            4, 5, 5, 5, 5, 5, 5, 4,
            6, 6, 5, 6, 6, 5, 6, 6,
            8, 8, 8, 9, 9, 8, 8, 8,
            9, 10, 10, 11, 11, 10, 10, 9,
            4, 6, 7, 9, 9, 7, 6, 4,
            9, 9, 11, 10, 10, 11, 9, 9
        ]
        QUEEN = [
            0, 0, 0, 0, 0, 0, 0, 0,
            2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 3, 3, 2, 2, 2,
            2, 3, 3, 4, 4, 3, 3, 2,
            3, 3, 4, 4, 4, 4, 3, 3, 
            3, 4, 4, 4, 4, 4, 4, 3,
            2, 3, 4, 4, 4, 4, 3, 2,
            2, 3, 3, 4, 4, 3, 3, 2

        ]
    @skip
    class Black(Enum):
        PAWN = [
            0, 0, 0, 0, 0, 0, 0, 0,
            7, 7, 13, 23, 26, 13, 7, 7,
            -2, -2, 4, 12, 15, 4, -2, -2,
            -3, -3, 2, 9, 11, 2, -3, -3,
            -4, -4, 0, 6, 8, 0, -4, -4,
            -4, -4, 0, 4, 6, 0, -4, -4,
            -1, -1, 1, 5, 6, 1, -1, -1,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        KNIGHT = [
            -2, 2, 7, 9, 9, 7, 2, -2,
            1, 4,12, 13, 13, 12, 4, 1,
            5, 11, 18, 19, 19, 18, 11, 5,
            3, 10, 14, 14, 14, 14, 10, 3,
            0, 5, 8, 9, 9, 8, 5, 0,
            -3, 1, 3, 4, 4, 3, 1, -3,
            -5, -3, -1, 0, 0, -1, -3, -5,
            -7, -5, -4, -2, -2, -4, -5, -7,
        ]
        BISHOP = [
            2, 3, 4, 4, 4, 4, 3, 2,
            4, 7, 7, 7, 7, 7, 7, 4,
            3, 5, 6, 6, 6, 6, 5, 3,
            3, 5, 7, 7, 7, 7, 5, 3,
            4, 5, 6, 8, 8, 6, 5, 4,
            4, 5, 5, -2, -2, 5, 5, 4,
            5, 5, 5, 3, 3, 5, 5, 5,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        ROOK = [
            9, 9, 11, 10, 10, 11, 9, 9,
            4, 6, 7, 9, 9, 7, 6, 4,
            9, 10, 10, 11, 11, 10, 10, 9,
            8, 8, 8, 9, 9, 8, 8, 8,
            6, 6, 5, 6, 6, 5, 6, 6,
            4, 5, 5, 5, 5, 5, 5, 4,
            3, 4, 4, 6, 6, 4, 4, 3,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]
        QUEEN = [
            2, 3, 3, 4, 4, 3, 3, 2,
            2, 3, 4, 4, 4, 4, 3, 2,
            3, 4, 4, 4, 4, 4, 4, 3,
            3, 3, 4, 4, 4, 4, 3, 3, 
            2, 3, 3, 4, 4, 3, 3, 2,
            2, 2, 2, 3, 3, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2,
            0, 0, 0, 0, 0, 0, 0, 0,
        ]


def evaluate(board):
    #print('Piece values: ', eval_all_pieces(board))
    #print('Piece location values: ', eval_all_piece_locations(board))
    return eval_all_pieces(board) + eval_mobility(board) - eval_mobility(board, color=~board.color) + eval_pieces_center(board) # + eval_all_piece_locations(board) +

def eval_piece(board, piece):
    return np.int32(board.pieces[board.color][piece].item().bit_count()) - np.int32(board.pieces[~board.color][piece].item().bit_count())


def eval_all_pieces(board):
    return(
        Score.PAWN.value * eval_piece(board, Piece.PAWN) +
        Score.KNIGHT.value * eval_piece(board, Piece.KNIGHT) +
        Score.BISHOP.value * eval_piece(board, Piece.BISHOP) +
        Score.ROOK.value * eval_piece(board, Piece.ROOK) +
        Score.QUEEN.value * eval_piece(board, Piece.QUEEN) +
        Score.KING.value * eval_piece(board, Piece.KING)
    )


def eval_pieces_center(board):
    return Score.CENTER.value * ((board.combined_color[board.color] ^ board.pieces[board.color][Piece.KING]) & CENTER).item().bit_count()

def eval_piece_location(piece, scores):
    points = 0
    position = 0
    one = np.uint8(1)
    while (piece != 0):
        if (piece & one != 0):
            points += scores[position]
        position += 1
        piece = piece >> one

    return points


def eval_all_piece_locations(board):
    col = board.color == Color.WHITE and PositionScore.White or PositionScore.Black
    enemy = board.color == Color.WHITE and PositionScore.Black or PositionScore.White
    return (
        eval_piece_location(board.pieces[~board.color][Piece.PAWN], enemy.PAWN.value) - eval_piece_location(board.pieces[board.color][Piece.PAWN], col.PAWN.value) +
        eval_piece_location(board.pieces[~board.color][Piece.KNIGHT], enemy.KNIGHT.value) - eval_piece_location(board.pieces[board.color][Piece.KNIGHT], col.KNIGHT.value) +
        eval_piece_location(board.pieces[~board.color][Piece.BISHOP], enemy.BISHOP.value) - eval_piece_location(board.pieces[board.color][Piece.BISHOP], col.BISHOP.value) +
        eval_piece_location(board.pieces[~board.color][Piece.ROOK], enemy.ROOK.value) - eval_piece_location(board.pieces[board.color][Piece.ROOK], col.ROOK.value) +
        eval_piece_location(board.pieces[~board.color][Piece.QUEEN], enemy.QUEEN.value) - eval_piece_location(board.pieces[board.color][Piece.QUEEN], col.QUEEN.value)
        # King has no positional values, hence not included
    )

def eval_mobility(board, color=None):
    if color is None:
        color = board.color
    if color != board.color:
        new_board = ChessBoard()
        new_board.color = color
        new_board.pieces = board.pieces
        new_board.combined_all = board.combined_all
        new_board.combined_color = board.combined_color
        moves = movegen.gen_attack_moves(new_board)
    else:
        moves = movegen.gen_attack_moves(board)


    points = 0
    for move in moves:
        victim = board.piece_on(move.dest)
        victim = victim is None and 6 or victim
        killer = board.piece_on(move.src)
        killer = killer is None and 6 or killer
        points += MVV_LVA[victim][killer]
    return points
