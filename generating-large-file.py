# import random
# line_1 = "/Users/mac/Desktop/testo/huhu/ioioi/ASASAS/猫猫猫猫/狗.log"
# line_2 = "/Users/mac/Desktop/testo/hehe"
# line_5 = "error_path"
# m_list = [line_1,line_2,line_1,line_2,line_5]
# filename = "large.log"
# N = 18000000*2
# with open(filename,"a+") as _f:
#     for _ in range(N):
#         line = random.choice(m_list)
#         print(line, file=_f)
import random

filename = "/Users/mac/Desktop/testo/huhu/ioioi/ASASAS/猫猫猫猫/project/test.log"

l1 = "asdhukljlkjiohiuhkjshiuahiodqwidqjilksdkasdklajskldfuih"
l2 = "asiqiwiksklajdklasjlkdqaaateyttaijopjpojonjkl"
l3 = "wqqwqwqweerqwrqwqwequdaasttrttyuytyutyrty"
l4 = "assajioqwklklklklklklklklklklklkl"
l5 = "2718721897281973kjjhhahjshjajhsahjajhskj"
m_list = [l1, l2, l3, l4, l5, l1, l2, l1, l2, l1, l1, l1, l3]

N = 20000000
with open(filename,"a+") as _f:
    for _ in range(N):
        line = random.choice(m_list)
        print(line, file=_f)
