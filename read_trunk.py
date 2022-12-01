import os.path
from concurrent import futures
import time
from itertools import islice, chain


def to_chunks(iterable, chunk_size):
    it = iter(iterable)
    while True:
        first = next(it)
        # Above raises StopIteration if no items left, causing generator
        # to exit gracefully.
        rest = islice(it, chunk_size-1)
        yield chain((first,), rest)

def _process(path):
    # print(path)
    return os.path.exists(path)

def read_trunk(filename,chunk_start,chunk_size):
    with open(filename,"r") as _f:
        _f.seek(chunk_start)
        lines = _f.read(chunk_size).splitlines()
        return lines[0], lines[-1]


def chunkify(fname,size=2*1024*1024):
    file_end = os.path.getsize(fname)
    with open(fname,"rb") as f:
        chunk_end = f.tell()
        while True:
            chunk_start = chunk_end
            f.seek(size,1)
            f.readline()
            chunk_end = f.tell()
            yield chunk_start, chunk_end - chunk_start
            if chunk_end > file_end:
                break


if __name__ == '__main__':
    # it = 0
    # for chunk_start, chunk_size in chunkify("large.log"):
    #     print(chunk_start, chunk_size)
    #     # it += 1
    #     # if it == 100:
    # print(read_trunk("large.log",1323342784,2097216))

    # _f =
    # with open("large.log", "r") as _f:
    #     lines = _f.readlines(1024*1024)
    #     print(lines)
    # print(chunkify("large.log"))
    # filename = "large.log"
    # s = 0
    # size = 1048590
    # lines = read_trunk(filename,s,size)
    # print(lines)

    # pool = futures.ThreadPoolExecutor(max_workers=10)
    #
    t1 = time.time()
    big_file = open("large.log", "r")
    # # 950
    file_size = os.path.getsize("large.log")

    BUF_SIZE =  file_size // 18
    line_num = 0
    tem_lines = big_file.readlines(BUF_SIZE)
    idx = 0
    while tem_lines:
        line_num += len(tem_lines)
        # print(tem_lines[-1].replace("\n",""))
        # for line in tem_lines:
        #     pool.submit(_process, line.replace("\n", ""))
        tem_lines = big_file.readlines(BUF_SIZE)
    print(line_num)
    print(time.time() - t1)

    # t = time.time()
    # with open("large.log","r") as _f:
    #     lines = _f.readlines()
    #     for line in lines:
    #         pool.submit(_process, line.replace("\n", ""))
    # print(time.time() - t)

    #
    # t2 = time.time()
    # with open("large.log") as _f:
    #     sum = 0
    #     for chunk in to_chunks(_f,10):
    #         l = [l for l in chunk]
    #         sum += len(l)
    #
    # print(sum)
    # print(time.time() -  t2)
    #
