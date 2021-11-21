from ai.eval import evaluate
from chessboard import ChessBoard
from move import Move
from square import Square
from constants import Piece
import re

def check_user_input_in_game(user_input):
    if re.match('([A-Ha-h][1-8])', user_input):
        return True
    return False

def check_start_player_input(user_input):
    if (user_input == "H" or user_input == "AI"):
        return True
    return False

def get_move():
    while True:
        src = input("From: ")
        if(check_user_input_in_game(src)):
            break
        else:
            print("Input invalid -> ( valid e.g. H5 )")
    while True:        
        dest = input("To: ")
        if(check_user_input_in_game(dest)):
            break
        else: 
            print("Input invalid -> ( valid e.g. H5 )")
    promo = input("Promo: ").lower()
    promo_piece = next(
            (p for p in Piece if p.to_char() == promo),
            None)
    return Move(Square.from_str(src), Square.from_str(dest), promo_piece)

def main():
    # NOTE: currently doesn't validate move or stop at checkmate, just plays
    # This is really just for generating example game gif
    board = ChessBoard()
    board.init_game()
    print("Initial board")
    print("\n")
    print(board)
    print("\n")
    print("Who starts? ( type \"H\" or \"AI\" )")
    print("\n")
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
    
    while True:
        if(player_turn == "H"):
            print("Player turn: H")
            print("\n")
            print("Enter your move ( e.g. From: B2 or To: B3 )")
            print("\n")
            player_move = get_move()
            board = board.apply_move(player_move)
            evaluate(board)
            print("\n")
            print("Board is now:")
            print(board)
            print("\n")
            player_turn = "AI"
        elif(player_turn == "AI"):
            engine_move = get_move()
            print(engine_move)
            board = board.apply_move(engine_move)
            print("\n")
            print("Board is now:")
            print(board)
            print("\n")
            player_turn = "H"


if __name__ == "__main__":
    main()