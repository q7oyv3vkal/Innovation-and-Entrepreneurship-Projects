import random
import time
from gmssl import sm3, func

def SM3_rho_attack(n):
    #使用随机数形成随机消息（注意攻击长度）
    cip = hex(random.randint(0, 2**(n+1)-1))[2:]
    cip_hash1 = sm3.sm3_hash(func.bytes_to_list(bytes(cip, encoding='utf-8')))
    cip_hash2 = sm3.sm3_hash(func.bytes_to_list(bytes(sm3.sm3_hash(func.bytes_to_list(bytes(cip, encoding='utf-8'))), encoding='utf-8')))
    cnt = 1
    while cip_hash1[:int(n/4)] != cip_hash2[:int(n/4)]:
        cnt += 1
        cip_hash1 = sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash1, encoding='utf-8')))
        cip_hash2 = sm3.sm3_hash(func.bytes_to_list(bytes(sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash2, encoding='utf-8'))), encoding='utf-8')))
    for j in range(cnt):
        if sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash1, encoding='utf-8')))[:int(n/4)] == sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash2, encoding='utf-8')))[:int(n/4)]:
            return [cip_hash1, cip_hash2,sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash1, encoding='utf-8')))[:int(n/4)]]
        else:
            cip_hash1 = sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash1, encoding='utf-8')))
            cip_hash2 = sm3.sm3_hash(func.bytes_to_list(bytes(cip_hash2, encoding='utf-8')))


if __name__ == '__main__':
    n=int(input("输入攻击bit：\n"))
    start = time.time()
    res=SM3_rho_attack(n)
    end=time.time()
    print("消息1:", res[0])
    print("消息2:", res[1])
    print("碰撞:", res[2])
    print(end-start,"seconds\n")
