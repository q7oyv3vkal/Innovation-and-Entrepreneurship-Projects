import random
import time
from gmssl import sm3, func

#通过生成随机浮点数转化成str的形式生成随即长度的字符串，并用库函数加密
cip_text = str(random.random())
cip_len = len(cip_text)
cip_hash = sm3.sm3_hash(func.bytes_to_list(bytes(cip_text, encoding='utf-8')))

#攻击函数（test_len:攻击长度）
def Birthday_attack(test_len):
    num = int(2 ** (test_len / 2))
    ans = [-1] * 2**test_len
    #循环遍历，对于每一位
    for i in range(num):
        temp = int(cip_hash[0:int(test_len / 4)], 16)
        if ans[temp] == -1:
            ans[temp] = i
        else:
            return hex(temp)

if __name__ == '__main__':
    test_len = 24
    start = time.time()
    res = Birthday_attack(test_len)
    end = time.time()
    print("前",test_len,"位碰撞为{}".format(res))
    print(end- start,'seconds\n')
