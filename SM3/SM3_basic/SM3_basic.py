from math import ceil

#初始向量IV
IV="7380166f 4914b2b9 172442d7 da8a0600 a96f30bc 163138aa e38dee4d b0fb0e4e"
IV = int(IV.replace(" ", ""), 16)
a = []
for i in range(0, 8):
    a.append(0)
    a[i] = (IV >> ((7 - i) * 32)) & 0xFFFFFFFF
IV = a

#左移函数
def rotate_left(a, k):
    k = k % 32
    return ((a << k) & 0xFFFFFFFF) | ((a & 0xFFFFFFFF) >> (32 - k))

T_j = []
for i in range(0, 16):
    T_j.append(0)
    T_j[i] = 0x79cc4519
for i in range(16, 64):
    T_j.append(0)
    T_j[i] = 0x7a879d8a

def FF_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | (X & Z) | (Y & Z)
    return ret

def GG_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | ((~ X) & Z)
    return ret

def P_0(X):
    return X ^ (rotate_left(X, 9)) ^ (rotate_left(X, 17))

def P_1(X):
    return X ^ (rotate_left(X, 15)) ^ (rotate_left(X, 23))

#压缩函数，进行压缩。ABCDEFGH为字寄存器，SS1,SS2,TT1,TT2为中间变量。在此过程中，子的储存为大端格式
def CF(V_i, B_i):
    W = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + B_i[k]*weight
            weight = int(weight/0x100)
        W.append(data)

    for j in range(16, 68):
        W.append(0)
        W[j] = P_1(W[j-16] ^ W[j-9] ^ (rotate_left(W[j-3], 15))) ^ (rotate_left(W[j-13], 7)) ^ W[j-6]
        str1 = "%08x" % W[j]

    W_1 = []
    for j in range(0, 64):
        W_1.append(0)
        W_1[j] = W[j] ^ W[j+4]
        str1 = "%08x" % W_1[j]

    A, B, C, D, E, F, G, H = V_i

    for j in range(0, 64):
        SS1 = rotate_left(((rotate_left(A, 12)) + E + (rotate_left(T_j[j], j))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ (rotate_left(A, 12))
        TT1 = (FF_j(A, B, C, j) + D + SS2 + W_1[j]) & 0xFFFFFFFF
        TT2 = (GG_j(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = rotate_left(B, 9)
        B = A
        A = TT1
        H = G
        G = rotate_left(F, 19)
        F = E
        E = P_0(TT2)

        A = A & 0xFFFFFFFF
        B = B & 0xFFFFFFFF
        C = C & 0xFFFFFFFF
        D = D & 0xFFFFFFFF
        E = E & 0xFFFFFFFF
        F = F & 0xFFFFFFFF
        G = G & 0xFFFFFFFF
        H = H & 0xFFFFFFFF

    V_i_1 = []
    V_i_1.append(A ^ V_i[0])
    V_i_1.append(B ^ V_i[1])
    V_i_1.append(C ^ V_i[2])
    V_i_1.append(D ^ V_i[3])
    V_i_1.append(E ^ V_i[4])
    V_i_1.append(F ^ V_i[5])
    V_i_1.append(G ^ V_i[6])
    V_i_1.append(H ^ V_i[7])
    return V_i_1

def hash_msg(msg):
    # print(msg)
    len1 = len(msg) #长度
    msg.append(0x80)
    reserve1 = len1 % 64  # 分组数
    reserve1 = reserve1 + 1

#将消息填充到64byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64
    for i in range(reserve1, range_end):
        msg.append(0x00)
    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])
    # print(msg)

#消息扩展
    group_count = round(len(msg) / 64)
    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])
#迭代压缩
    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(CF(V[i], B[i]))
    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

#字符串转换成byte数组
def str2byte(msg):
    ml = len(msg)
    msg_byte = []
    msg_bytearray = msg.encode('utf-8')
    for i in range(ml):
        msg_byte.append(msg_bytearray[i])
    return msg_byte

#16进制字符串转换成byte数组
def hex2byte(msg):
    ml = len(msg)
    if ml % 2 != 0:
        msg = '0'+ msg
    ml = int(len(msg)/2)
    msg_byte = []
    for i in range(ml):
        msg_byte.append(int(msg[i*2:i*2+2],16))
    return msg_byte

def KDF(Z,klen):
    # Z：16进制表示的比特串（str），klen：密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen/32)
    Zin = hex2byte(Z)
    Ha = ""
    for i in range(rcnt):
        msg = Zin  + hex2byte('%08x'% ct)
        # print(msg)
        Ha = Ha + hash_msg(msg)
        # print(Ha)
        ct += 1
    return Ha[0: klen * 2]

def Hash_sm3(msg):
    msg_byte = str2byte(msg)
    return hash_msg(msg_byte)

if __name__ == '__main__':
    str = input("请输入加密内容：");
    y = Hash_sm3(str)
    print(y)
