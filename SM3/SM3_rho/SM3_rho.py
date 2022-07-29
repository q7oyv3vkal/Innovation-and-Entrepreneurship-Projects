import random
import time
from SM3_basic import Hash_sm3

def SM3_rho_attack(n):
    #使用随机数形成随机消息（注意攻击长度）
    cip = hex(random.randint(0, 2**(n+1)-1))[2:]
    cip_hash1 = Hash_sm3(cip)
    cip_hash2 = Hash_sm3(Hash_sm3(cip))
    cnt = 1
    while cip_hash1[:int(n/4)] != cip_hash2[:int(n/4)]:
        cnt += 1
        cip_hash1 = Hash_sm3(cip_hash1)
        cip_hash2 = Hash_sm3(Hash_sm3(cip_hash2))
    cip_hash1 = cip
    for j in range(cnt):
        #攻击成功
        if Hash_sm3(cip_hash1)[:int(n/4)] == Hash_sm3(cip_hash2)[:int(n/4)]:
            return [ cip_hash1, cip_hash2,Hash_sm3(cip_hash1)[:int(n/4)],]
        else:
            cip_hash1 = Hash_sm3(cip_hash1)
            cip_hash2 = Hash_sm3(cip_hash2)


if __name__ == '__main__':
    n=int(input("输入攻击bit：\n"))
    start = time.time()
    res=SM3_rho_attack(n)
    end=time.time()
    print("消息1:", res[0])
    print("消息2:", res[1])
    print("碰撞:", res[2])
    print(end-start,"seconds\n")
