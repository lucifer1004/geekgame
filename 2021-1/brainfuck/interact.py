from binascii import *
from pwn import *

r = remote('prob13.geekgame.pku.edu.cn', 10013)


def recvline():
    b = r.recvuntil(b'\n')
    line = str(b, 'utf-8')
    return line


def recvuntil(until):
    b = r.recvuntil(until)
    line = str(b, 'utf-8')
    return line


recvuntil(b'Please input your token: ')

r.send(b'262:MEQCIBqYgFgdoMXZJouXwPFXxtdMvwDQP39d7YP4rLy7vHBhAiBk1MvEZXzzbh7H1lHb5Em1XAqyUVgVhuJPY2864mSGMA==\n')

recvuntil(b'give me code (hex): ')

code = hexlify(b'>+[>[<-]<[->+<]>]>' + b'.>' * 24)

r.send(code + b'\n')

while True:
    try:
        print(str(r.recv(1), 'utf-8'), end='')
    except:
        exit(0)
