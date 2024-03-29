#客户端
import socket
from gmssl import sm2 ,sm4
import sys
import random
p='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF'
a='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC'
b='28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93'
n='FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123'
g='32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7'\
'BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0'

#返回u mod v的倒数。
def inverse(u, v):
    u3, v3 = u, v
    u1, v1 = 1, 0
    while v3 > 0:
        q=divmod(u3, v3)[0]
        u1, v1 = v1, u1 - v1*q
        u3, v3 = v3, u3 - v3*q
    while u1<0:
        u1 = u1 + v
    return u1

def generate_d2():
    i=int(n,16)
    d1=random.randint(1,i-1)
    return d1

#产生-G，实现椭圆曲线减法
def generate_G_1(G):
    sm2_c=sm2.CryptSM2(private_key="",public_key="")
    leng=len(G)
    xg=G[0:sm2_c.para_len]
    yg=G[sm2_c.para_len:leng]
    yg=int(yg,16)
    yg=(-yg)%int(p,16)
    yg=hex(yg)[2:]
    G_1=xg+yg
    return G_1

#公钥
def generate_P(d2,P1):
    i=int(n,16)
    sm2_c=sm2.CryptSM2(private_key="",public_key="")
    temp=sm2_c._kg(inverse(d2,i),P1)
    # -G
    G_1=generate_G_1(g)
    # 两个点相加
    P=sm2_c._add_point(temp,G_1)
    # 得到最终的x||y
    P=sm2_c._convert_jacb_to_nor(P)
    return P

def generate_r_s2_s3(d2,Q1,e):
    i=int(n,16)
    sm2_c=sm2.CryptSM2(private_key="",public_key="")
    k2=generate_d2()
    Q2=sm2_c._kg(k2,g)
    k3=generate_d2()
    temp=sm2_c._kg(k3,Q1)
    # 两个点相加
    P=sm2_c._add_point(temp,Q2)
    # 得到最终的x||y
    P=sm2_c._convert_jacb_to_nor(P)
    x1=int(P[0:sm2_c.para_len],16)
    r=(x1+int(e.hex(),16))%i
    s2=(d2*k3)%i
    s3=d2*(r+k2)%i
    return(r,s2,s3)



#建立TCP连接
HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print('Listening on port:',PORT)
conn, addr = s.accept()
print('Connected by', addr)

#接受P1
P1 = conn.recv(1024).decode('utf-8')

d2=generate_d2()
#产生公钥
P=generate_P(d2,P1)
print("产生的公钥为：",P)
conn.sendall("OK".encode("utf-8"))

#接受Q1
Q1=conn.recv(1024).decode('utf-8')
conn.sendall("OK".encode("utf-8"))

#接受e
e=conn.recv(1024)
conn.sendall("OK".encode("utf-8"))

#产生r,s2,s3并发送给另一个人
r,s2,s3=generate_r_s2_s3(d2,Q1,e)

conn.sendall(hex(r)[2:].encode('utf-8'))
an=conn.recv(1024)
assert an.decode('utf-8')=="OK","fail1"

conn.sendall(hex(s2)[2:].encode('utf-8'))
an=conn.recv(1024)
assert an.decode('utf-8')=="OK","fail1"

conn.sendall(hex(s3)[2:].encode('utf-8'))
an=conn.recv(1024)
assert an.decode('utf-8')=="OK","fail1"
