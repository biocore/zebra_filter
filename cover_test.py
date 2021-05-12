from cover import SortedRangeList
import random
from time import perf_counter


def simple_test():
    srl = SortedRangeList(autocompress=None)
    for i in range(9, 0, -2):
        srl.add_range(i,i)
    srl.add_range(4,4)
    srl.compress()
    assert(str(srl) == "[(1, 1), (3, 5), (7, 7), (9, 9)]")


def stress_test(seed, num_reads):
    intset = set()
    srl = SortedRangeList(autocompress=None)

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
        srl.add_range(read_start, read_start+read_len-1)
    print("SRL_ADD: ", perf_counter() - start_srl)
    srl.compress()
    print("SRL_ADD AND COMPRESS: ", perf_counter() - start_srl)
    srl_len = srl.compute_length()
    print("SRL_ADD COMPRESS AND LENGTH: ", perf_counter() - start_srl)

    print(srl_len)
    print(len(intset))
    assert(len(intset) == srl_len)
    print(len(srl.ranges))


def multi_compress_test(seed, num_reads):
    srl = SortedRangeList(autocompress=None)

    for compress_count in [1000, 10000, 100000]:
        start_srl = perf_counter()
        random.seed(seed)
        for i in range(num_reads):
            read_start = random.randint(0, 10000000)
            read_len = random.randint(85, 150)
            srl.add_range(read_start, read_start+read_len-1)
            if i % compress_count == 0:
                srl.compress()
        print(srl.compute_length())
        print("Compress Counter: ", compress_count, " Performance: ", perf_counter() - start_srl)


simple_test()
seed = 127
for reads in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    multi_compress_test(seed, reads)
for reads in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    stress_test(seed, reads)
