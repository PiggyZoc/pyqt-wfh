line = "/Users/mac/Desktop/testo/huhu/ioioi/ASASAS/猫猫猫猫/狗.log"
filename = "large-1.log"
N = 160
with open(filename,"a+") as _f:
    for _ in range(N):
        print(line, file=_f)