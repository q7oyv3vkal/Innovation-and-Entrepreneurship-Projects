
from gmssl import sm2, sm4
import random
import time

str36 = "shandongdaxue202000460066yangkaige00"
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# 以下均是接受者的密钥
private_key = '010203040506070809000A0B0C0D0E0F010203040506070809000A0B0C0D0E0F01'
public_key = '04E9C91B81872260BEF331A83081A693747D7EA88042927317EB06B9C9A6EF5DDEB0BB2FF6CF5AF347B483F7B9487C018FB4162B8993F3F5D6EADDDE24620207'

#生成随机k，随机从私钥中找16个元素，并且将其返回为utf-8编址形式
def generate_random_k():
    k = ""
    for i in range(0, 16):
        k += str36[random.randint(0, 35)]
    return k.encode('utf-8')

#发送者，分别对消息和密钥进行加密
def sender(msg):
    # 生成一个随机的k
    K = generate_random_k()
    #SM4加密
    sm4_enc = sm4.CryptSM4()
    sm4_enc.set_key(K, sm4.SM4_ENCRYPT)
    #对消息加密
    enc_msg = sm4_enc.crypt_ecb(msg.encode("utf-8"))
    #sm2加密，过程中不需要私钥
    sm2_enc = sm2.CryptSM2(public_key=public_key, private_key="")
    #对密钥加密
    enc_key = sm2_enc.encrypt(K)
    return (enc_msg, enc_key)

#接收者，先解密得到密钥，再使用密钥解密得到消息
def receiver(enc_msg, enc_key):
    # 布置sm2加密
    sm2_enc = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    #解密密钥
    K = sm2_enc.decrypt(enc_key)
    #布置sm4堆成加密器
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(K, sm4.SM4_DECRYPT)
    #解密消息
    decrypt_m = crypt_sm4.crypt_ecb(enc_msg)
    return decrypt_m.decode("utf-8")


msg = input("输入需要加密的数据:\n")
start=time.time()
enc_msg, enc_key = sender(msg)

dec_m = receiver(enc_msg, enc_key)
end=time.time()
print("加密后的消息为：", enc_msg)
print("加密后的会话秘钥为：\n",enc_key)
if dec_m==msg:
    print("成功！")
print(end-start,'seconds')
