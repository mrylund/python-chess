from inspect import currentframe
from re import A
import timeit
import sys
from ai.eval import evaluate
import movegen

branches_pruned = 0
branches_visited = 0
search_depth = 0
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


def quiesce(board, alpha, beta):
    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta
    
    alpha = max(alpha, stand_pat)

    movecount = 0
    for move in movegen.gen_attack_moves(board):
        print(move)
        movecount += 1
        score = -quiesce(board.apply_move(move), -alpha, -beta)

        if score >= beta:
            return beta

        alpha = max(alpha, score)
    
    if movecount == 0:
        return stand_pat

    return alpha
    
    





def search(board, depth, start_time, time_limit, alpha, beta):
    global branches_pruned, branches_visited
    branches_visited += 1

    best_score = -sys.maxsize
    b = beta

    if(timeit.default_timer() - start_time >= time_limit or depth == 0):
        
        print(evaluate(board), quiesce(board, alpha, beta))
        return quiesce(board, alpha, beta)
    
    for move in movegen.gen_legal_moves(board):
        score = -search(board.apply_move(move), depth-1, start_time, time_limit, -alpha, -b)
        # if score > best:
        #     best = score

        if score > best_score:
            if alpha < score < beta:
                best_score = max(score, best_score)
            else:
                best_score = -search(board.apply_move(move), depth-1, start_time, time_limit, -beta, -score)

        alpha = max(score, alpha)
        if alpha >= beta:
            return alpha

        b = alpha + 1

    return alpha



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
        
        score = -search(board, depth, start_time, time_limit, -100000, 100000)
        if depth > search_depth:
            search_depth = depth
        depth += 1
    
    return score



def find_best_move(board, time_limit):
    global branches_pruned, branches_visited
    branches_visited = 0
    branches_pruned = 0
    for move in movegen.gen_attack_moves(board):
        print(move)

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

    return best_move, branches_visited, branches_pruned, search_depth

