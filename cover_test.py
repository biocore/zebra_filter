from cover import SortedRangeList, IndexRange
import random
from time import perf_counter

srl = SortedRangeList()
for i in range(9, 0, -2):
    srl.add_range(IndexRange(i,i))
print(srl)
srl.add_range(IndexRange(4,4))
print(srl)
srl.compress()
print(srl)


def stress_test(seed, num_reads):
    intset = set()
    srl = SortedRangeList()

    start_set = perf_counter()
    random.seed(seed)
    for i in range(num_reads):
        read_start = random.randint(0, 10000000)
        read_len = random.randint(85, 150)
        for j in range(read_start, read_start + read_len):
            intset.add(j)
    print("SET_ADD: ", perf_counter() - start_set)

    start_srl = perf_counter()
    random.seed(seed)
    for i in range(num_reads):
        read_start = random.randint(0, 10000000)
        read_len = random.randint(85, 150)
        srl.add_range(IndexRange(read_start, read_start+read_len-1))
    print("SRL_ADD: ", perf_counter() - start_srl)
    srl.compress()
    print("SRL_ADD AND COMPRESS: ", perf_counter() - start_srl)
    srl_len = srl.compute_length()
    print("SRL_ADD COMPRESS AND LENGTH: ", perf_counter() - start_srl)

    print(srl_len)
    print(len(intset))
    print(len(srl.ranges))

seed = 127
for reads in [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]:
    stress_test(seed, reads)
