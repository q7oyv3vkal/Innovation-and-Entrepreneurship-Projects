from gmssl import sm3, func
import random
import Mysm3             #修改python库中的部分sm3函数，方便攻击
import struct
import time

#同样使用将浮点数转化成字符串形式的过程生成
#cip_test:加密密文，cip_hash:加密明文，cip_len:明文长度，append_m:附加消息
start=time.time()
cip_test = str(random.random())
cip_hash = sm3.sm3_hash(func.bytes_to_list(bytes(cip_test, encoding='utf-8')))
cip_len = len(cip_test)
append_m = "202000460066"
pad_str = ""
pad = []

def generate_guess_hash(old_hash, secret_len, append_m):
    vectors = []
    message = ""
    for r in range(0, len(old_hash), 8):
        vectors.append(int(old_hash[r:r + 8], 16))
    if secret_len > 64:
        for i in range(0, int(secret_len / 64) * 64):
            message += 'a'
    for i in range(0, secret_len % 64):
        message += 'a'
    message = func.bytes_to_list(bytes(message, encoding='utf-8'))
    message = padding(message)
    message.extend(func.bytes_to_list(bytes(append_m, encoding='utf-8')))
    return Mysm3.sm3_hash(message, vectors)

def padding(msg):
    mlen = len(msg)
    msg.append(0x80)
    mlen += 1
    tail = mlen % 64
    range_end = 56
    if tail > range_end:
        range_end = range_end + 64
    for i in range(tail, range_end):
        msg.append(0x00)
    bit_len = (mlen - 1) * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_len)])
    for j in range(int((mlen - 1) / 64) * 64 + (mlen - 1) % 64, len(msg)):
        global pad
        pad.append(msg[j])
        global pad_str
        pad_str += str(hex(msg[j]))
    return msg

guess_hash = generate_guess_hash(cip_hash, cip_len, append_m)
new_msg = func.bytes_to_list(bytes(cip_test, encoding='utf-8'))
new_msg.extend(pad)
new_msg.extend(func.bytes_to_list(bytes(append_m, encoding='utf-8')))
new_msg_str = cip_test + pad_str + append_m

new_hash = sm3.sm3_hash(new_msg)
end=time.time()


print("消息:",cip_test)
print("消息长度:%d" % len(cip_test))
print("hash后消息:" + cip_hash)
print("附加消息:", append_m)
print("人为构造的消息（加入附加消息）的hash值",guess_hash)
print("new message:\n " + new_msg_str)
print("hash(new message):" + new_hash)
if new_hash == guess_hash:
    print("success")
else:
    print("fail")

print(end-start,'seconds\n')
