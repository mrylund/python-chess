from ai.eval import Score, evaluate
from chessboard import ChessBoard
from move import Move
from square import Square
from constants import Piece, Color
import re
import ai.search as ai
import movegen


status ="""
===================================
== Eval for {player} is {score} points
== 
== AI stats:
==    - {states_visited} states visisted
==    - {branch_cutoff} branches cut off
==    - Search depth: {depth}
==
== Move performed:
==    {move}
===================================
{board}
===================================
"""


def check_user_input_in_game(user_input):
    if re.match('([A-Ha-h][1-8])', user_input):
        return True
    return False

def check_start_player_input(user_input):
    if (user_input == "H" or user_input == "AI"):
        return True
    return False

def get_move(board):
    src, dest, promo = "", "", ""
    accepted_chars = {'q', 'r', 'n', 'b'}
    
    while True:
        src = input("From: ").upper()
        if(check_user_input_in_game(src)):
            break
        else:
            print("Input invalid -> ( valid e.g. H5 )")
    while True:        
        dest = input("To:   ").upper()
        if(check_user_input_in_game(dest)):
            if ((board.color == Color.WHITE and dest[1] == "8") or (board.color == Color.BLACK and dest[1] == "1")):
                while True:
                    print("Type what you would like to promote your piece to ( e.g \"r\", \"q\", \"n\" or \"b\" ) ")
                    promo = input("Promo: ").lower()
                    if(promo.lower() in accepted_chars):
                        break
                    else:
                        print("Invalid input -> ( try e.g. \"r\", \"q\", \"n\" or \"b\" ) \n")
                        
            break
        else: 
            print("Input invalid -> ( valid e.g. H5 )")
        
    promo_piece = next((p for p in Piece if p.to_char() == promo and p.to_char() != 'k'), None)
    return Move(Square.from_str(src), Square.from_str(dest), promo_piece)

def main():
    # NOTE: currently doesn't validate move or stop at checkmate, just plays
    # This is really just for generating example game gif
    board = ChessBoard()
    board.init_game()
    print("Who starts? ( type \"H\" or \"AI\" )")
    player_turn = "H"

    while True:
        first_player = input().upper()
        if(check_start_player_input(first_player)):
            if(first_player == "H"):
                player_turn = "H"
                break
            elif(first_player == "AI"):
                player_turn = "AI"
                break
        else:
            print("Invalid input -> Type either \"H\" or \"AI\"")
    

    print(status.format(player = player_turn,  score = 0, states_visited=0, branch_cutoff=0, depth=0, move='No move yet', board=str(board)))

    branches_visited, branches_cutoff, depth = 0, 0, 0
    while True:
        move = None
        if(player_turn == "H"):
            prev_player = 'Human'
            #for move in movegen.gen_legal_moves(board):
            #    print(str(move).split(' -> '))
            print("Enter your move ( e.g. From: B2 or To: B3 )")
            movefound = False
            while not movefound:
                player_move = get_move(board)
                for move in movegen.gen_legal_moves(board):
                    if str(move) == str(player_move):
                        movefound = True
                        break
                if not movefound:
                    print('Illegal move, please try again!')
            player_turn = "AI"
        elif(player_turn == "AI"):
            prev_player = player_turn
            engine_move, branches_visited, branches_cutoff, depth = ai.find_best_move(board, 15)
            move = engine_move
            player_turn = "H"

        board_value = evaluate(board)
        board = board.apply_move(move)

        print(status.format(player = prev_player,  score = board_value, states_visited=branches_visited, branch_cutoff=branches_cutoff, depth=depth, move=str(move), board=str(board)))
        branches_visited, branches_cutoff, depth = 0, 0, 0

if __name__ == "__main__":
    main()