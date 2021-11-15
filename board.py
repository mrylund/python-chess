import numpy as np
import constants
import helpers

class board:
    def __init__(self):
        self.board = np.zeros(128)
        self.board[70], self.board[71], self.board[72], self.board[73], self.board[74], self.board[75], self.board[76], self.board[77] = -4, -2, -3, -6, -5, -3, -2, -4
        self.board[60], self.board[61], self.board[62], self.board[63], self.board[64], self.board[65], self.board[66], self.board[67] = -1, -1, -1, -1, -1, -1, -1, -1
        
        self.board[10], self.board[11], self.board[12], self.board[13], self.board[14], self.board[15], self.board[16], self.board[17] = 1, 1, 1, 1, 1, 1, 1, 1
        self.board[0], self.board[1], self.board[2], self.board[3], self.board[4], self.board[5], self.board[6], self.board[7] = 4, 2, 3, 6, 5, 3, 2, 4

    def  __str__(self):
        board_str = ''
        for y in range(8):
            linestr = str(y+1) + ' '
            for x in range(8):
                val = self.board[int(str(y) + str(x))]
                if helpers.isBlack(val):
                    if helpers.isKing(val):
                        linestr += constants.BLACK_KING
                    elif helpers.isQueen(val):
                        linestr += constants.BLACK_QUEEN
                    elif helpers.isRook(val):
                        linestr += constants.BLACK_ROOK
                    elif helpers.isBishop(val):
                        linestr += constants.BLACK_BISHOP
                    elif helpers.isKnight(val):
                        linestr += constants.BLACK_KNIGHT
                    elif helpers.isPawn(val):
                        linestr += constants.BLACK_PAWN
                elif helpers.isWhite(val):
                    if helpers.isKing(val):
                        linestr += constants.WHITE_KING
                    elif helpers.isQueen(val):
                        linestr += constants.WHITE_QUEEN
                    elif helpers.isRook(val):
                        linestr += constants.WHITE_ROOK
                    elif helpers.isBishop(val):
                        linestr += constants.WHITE_BISHOP
                    elif helpers.isKnight(val):
                        linestr += constants.WHITE_KNIGHT
                    elif helpers.isPawn(val):
                        linestr += constants.WHITE_PAWN
                elif helpers.isEmpty(val):
                    linestr += constants.EMPTY
                linestr += ' '
            linestr = linestr + ' ' + str(y+1) + '\n'
            board_str = linestr + board_str
            linestr = []
        board_str = '- a b c d e f g h -\n' + board_str + '- a b c d e f g h -'
        return '%s' % board_str   

hej = board()
print(hej)
