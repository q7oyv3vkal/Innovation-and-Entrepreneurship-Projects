from gmssl import sm2
from hashlib import sha256
import time

# 椭圆曲线官方推荐参数,方便int()时进行类型转化
p='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF'
a='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC'
b='28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93'
n='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123'
g='32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7'\
'BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0'

#ECMH函数,返回msghash过后椭圆曲线点横纵坐标拼接:x||y
def ECMH(msg):
    hash_msg= sha256(str(msg).encode()).digest()
    pri = int(hash_msg.hex(), 16)
    # 只是利用其中函数,公钥私钥均设置为0就行
    sm2_c = sm2.CryptSM2(private_key="", public_key="")
    #计算哈希值后坐标x||y
    P1 = sm2_c._kg(pri, g)
    return P1

#哈希过后添加新的元素(另一个输入)并继续哈希
def ECMH_append(hash, msg):

    hash_msg = sha256(str(msg).encode()).digest()
    # 只是利用其中函数,公钥私钥均设置为0就行
    sm2_c = sm2.CryptSM2(private_key="", public_key="")
    pri = int(hash_msg.hex(), 16)
    # 计算哈希值后坐标x||y
    P1 = sm2_c._kg(pri, g)
    #将两个点相加
    P = sm2_c._add_point(P1, hash)
    #得到x||y
    P = sm2_c._convert_jacb_to_nor(P)
    return P


cip1 = input("字符串1：\n")
cip2 = input("字符串2：\n")
start=time.time()
cip_hash1 = ECMH(cip1)
cip_hash2 = ECMH(cip2)
cip_app_hash1_cip2=ECMH_append(cip_hash1, cip2)
cip_app_hash2_cip1=ECMH_append(cip_hash2, cip1)
end=time.time()

print("字符串1hash值", cip_hash1)
print("字符串2hash值", cip_hash2)

print("先hash第一个字符串再添加第二个：", cip_app_hash1_cip2)
print("先hash第二个字符串再添加第一个：", cip_app_hash2_cip1)

print(end-start,'seconds\n')
