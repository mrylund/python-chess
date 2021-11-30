from inspect import currentframe
from re import A
import timeit
import sys
from ai.eval import evaluate
import movegen

branches_pruned = 0
branches_visited = 0
search_depth = 0


def quiesce(board, alpha, beta, depth):
    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta
    
    alpha = max(alpha, stand_pat)

    for move in movegen.gen_attack_moves(board):
        score = -quiesce(board.apply_move(move), -beta, -alpha, depth-1)

        if score >= beta:
            return beta

        alpha = max(alpha, score)

    return alpha
    

def search(board, depth, start_time, time_limit, alpha, beta):
    global branches_pruned, branches_visited
    branches_visited += 1
    if(timeit.default_timer() - start_time >= time_limit or depth == 0):
        return evaluate(board) #quiesce(board, -beta, -alpha, 8)
    
    best = -sys.maxsize + 1
    for move in movegen.gen_legal_moves(board):
        best = max(best, -search(board.apply_move(move), depth-1, start_time, time_limit, -beta, -beta))
        alpha = max(alpha, best)
        if alpha >= beta:
            break

    return best



def iterative_deepening_search(board, time_limit):
    global branches_pruned, search_depth
    start_time = timeit.default_timer()
    end_time = start_time + time_limit
    depth = 1
    score = 0
    cutOff = False

    while (True):
        current_time = timeit.default_timer()
        if current_time >= end_time:
            branches_pruned +=1
            break
        
        score = -search(board, depth, start_time, time_limit, -1000000, 1000000)
        if depth > search_depth:
            search_depth = depth
        depth += 1
    
    return score



def find_best_move(board, time_limit):
    global branches_pruned, branches_visited
    branches_visited = 0
    branches_pruned = 0

    max = -sys.maxsize
    move_num = 0
    for move in movegen.gen_legal_moves(board):
        move_num += 1
        
    if move_num == 0:
        return None, None, None, None

    search_time_limit = time_limit / move_num
    for move  in movegen.gen_legal_moves(board):
        score = iterative_deepening_search(board.apply_move(move), search_time_limit)
        if score > max:
            max = score
            best_move = move

    return best_move, branches_visited, branches_pruned, search_depth

