from inspect import currentframe
import timeit
import sys
from ai.eval import evaluate
import movegen


# def negmax(board, start_time, time_limit, depth):
#     print(timeit.default_timer() - start_time )
#     if(timeit.default_timer() - start_time >= time_limit or depth == 0):
#         return evaluate(board)
    
#     max = -sys.maxsize
#     for move in movegen.gen_legal_moves(board):
#         score = -negmax(board.apply_move(move), start_time, time_limit, depth - 1)
#         if score > max:
#             max = score

#     return max

# def find_best_move(board, time_limit):
#     start_time = timeit.default_timer()
#     max = -sys.maxsize
#     for move  in movegen.gen_legal_moves(board):
#         score = -negmax(board.apply_move(move), start_time, time_limit, 10)
#         if score > max:
#             max = score
#             best_move = move

#     return best_move




def search(board, depth, start_time, time_limit, alpha, beta):
    if(timeit.default_timer() - start_time >= time_limit or depth == 0):
        return evaluate(board)
    
    best = -sys.maxsize + 1
    for move in movegen.gen_legal_moves(board):
        score = -search(board.apply_move(move), depth-1, start_time, time_limit, -alpha, -beta)
        # if score > best:
        #     best = score

        if score > alpha:
            alpha = score

        if score >= beta:
            break

    return alpha



def iterative_deepening_search(board, time_limit):
    start_time = timeit.default_timer()
    end_time = start_time + time_limit
    depth = 1
    score = 0
    cutOff = False

    while (True):
        current_time = timeit.default_timer()
        if current_time >= end_time:
            break
        
        score = -search(board, depth, start_time, time_limit, -sys.maxsize, sys.maxsize)
        print(depth)
        depth += 1
    
    return score



def find_best_move(board, time_limit):
    start_time = timeit.default_timer()
    max = -sys.maxsize
    move_num = 0
    for move in movegen.gen_legal_moves(board):
        move_num += 1

    search_time_limit = time_limit / move_num
    for move  in movegen.gen_legal_moves(board):
        score = iterative_deepening_search(board.apply_move(move), search_time_limit)
        if score > max:
            max = score
            best_move = move

    return best_move