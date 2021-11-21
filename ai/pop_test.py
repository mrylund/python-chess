import timeit
import numpy as np
num_loops = 1000000

test = np.uint64(3)

EMPTY_BB = np.uint64(0)

def pop(x):
    n = (x >> 1) & 0x77777777
    x = x - n
    n = (n >> 1) & 0x77777777
    x = x - n
    n = (n >> 1) & 0x77777777
    x = x - n
    x = (x + (x >> 4)) & 0x0F0F0F0F
    x = x * 0x01010101
    return x >> 24


def pop_count(bb):
    bb = np.uint64(bb)
    count = np.uint8(0)
    while bb != EMPTY_BB:
        count += np.uint8(1)
        bb &= bb - np.uint64(1)
    return count

start = timeit.default_timer()

for i in range(num_loops):
    i.bit_count()

end = timeit.default_timer()

print('Time built in: ', end-start)


start = timeit.default_timer()

for i in range(num_loops):
    test.item().bit_count()

end = timeit.default_timer()

print('Time built in: ', end-start)


start = timeit.default_timer()

for i in range(num_loops):
    pop(i)

end = timeit.default_timer()

print('Time reddit: ', end-start)


start = timeit.default_timer()

for i in range(num_loops):
    pop_count(i)

end = timeit.default_timer()

print('Time Kernighan: ', end-start)