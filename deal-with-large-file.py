import os
import time
from concurrent import futures


def _process(path):
    return os.path.exists(path)


if __name__ == '__main__':
    t = time.time()
    pool = futures.ThreadPoolExecutor(max_workers=4)
    with open("large.log", "r") as _f:
        lines = _f.readlines()
        for line in lines:
            pool.submit(_process, line.replace("\n", ""))
            # lines = [line.replace("\n", "") for line in lines]
    #
    # for l in lines:
    #     pool.submit(_process, l)

    print(time.time() - t)


