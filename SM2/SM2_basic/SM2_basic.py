from random import randint
import math
import Mysm3
import time

#椭圆曲线官方推荐参数
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

#欧几里得求逆运算
def Euclid_inverts(a,m):
    x1=1
    x2=0
    x3=a
    y1=0
    y2=1
    y3=m
    while y3!=0:
        q=x3//y3
        t1=x1-q*y1
        x1=y1
        t2=x2-q*y2
        x2=y2
        t3=x3-q*y3
        x3=y3
        y1=t1
        y2=t2
        y3=t3
    return x1%m

#椭圆曲线E上的点在素数域下加法运算
def Add(x1,y1,x2,y2,a,p):
    if x1==x2 and y1==p-y2:
        return False
    if x1!=x2:
        lamda=((y2-y1)*Euclid_inverts(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+a)%p)*Euclid_inverts(2*y1, p))%p
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3

#椭圆曲线E上的倍点运算
def Mutipoint(x,y,k,a,p):
    k=bin(k)[2:]
    qx,qy=x,y
    for i in range(1,len(k)):
        qx,qy=Add(qx, qy, qx, qy, a, p)
        if k[i]=='1':
            qx,qy=Add(qx, qy, x, y, a, p)
    return qx,qy

#密钥派生函数
def kdf(z,klen):
    ct=1
    k=''
    for _ in range(math.ceil(klen/256)):
        k=k+sm3.sm3_hash(hex(int(z+'{:032b}'.format(ct),2))[2:])
        ct=ct+1
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:klen]

dB=randint(1,n-1)
xB,yB=Mutipoint(gx,gy,dB,a,p)
  
#加密函数
def SM2_encrypt(m:str):
    plen=len(hex(p)[2:])
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    klen=len(m)
    while True:
        k=randint(1, n)
        while k==dB:
            k=randint(1, n)
        x2,y2=Mutipoint(xB, yB, k, a, p)
        x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
        t=kdf(x2+y2, klen)
        if int(t,2)!=0:
            break
    x1,y1=Mutipoint(gx, gy, k, a, p)
    x1,y1=(plen-len(hex(x1)[2:]))*'0'+hex(x1)[2:],(plen-len(hex(y1)[2:]))*'0'+hex(y1)[2:]
    c1='04'+x1+y1
    c2=((klen//4)-len(hex(int(m,2)^int(t,2))[2:]))*'0'+hex(int(m,2)^int(t,2))[2:]
    c3=sm3.sm3_hash(hex(int(x2+m+y2,2))[2:])
    return c1,c2,c3

f=open('E://text.txt','r')
fstr=f.read()
f.close()
print("加密密文为:\n",fstr)
start=time.time()
c1,c2,c3=SM2_encrypt(fstr)
c=(c1+c2+c3).upper()
end=time.time()
print('加密结果:\n')
for i in range(len(c)):
    print(c[i*8:(i+1)*8],end=' ')
print("\n",end-start,"seconds)


