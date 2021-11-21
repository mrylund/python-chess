import timeit
import numpy as np
from eval import PositionScore

num_loops = 100000



def eval_piece_location1(piece, scores):
    points = 0
    position = 0
    one = np.uint8(1)
    while (piece != 0):
        if (piece & one != 0):
            points += scores[position]
        position += 1
        piece = piece >> one

    return points


def eval_piece_location2(piece, scores):
    points = 0
    position = 0
    while (piece != 0):
        if (piece & np.uint8(1) != 0):
            points += scores[position]
        position += 1
        piece = piece >> np.uint8(1)

    return points



start = timeit.default_timer()
for i in range(num_loops):
    eval_piece_location1(np.uint64(0x00FF000000000000), PositionScore.Black.PAWN.value)

end = timeit.default_timer()


print('Bit shift 1: ', end-start)



start = timeit.default_timer()
for i in range(num_loops):
    eval_piece_location2(np.uint64(0x00FF000000000000), PositionScore.Black.PAWN.value)
end = timeit.default_timer()

print('Bit shift 2: ', end-start)