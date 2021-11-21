import os
from binascii import *
from pwn import *

r = remote('prob08.geekgame.pku.edu.cn', 10008)


def recvline():
    b = r.recvuntil(b'\n')
    line = str(b, 'utf-8')
    return line


def recvuntil(until):
    b = r.recvuntil(until)
    line = str(b, 'utf-8')
    return line


recvuntil(b'Please input your token:\n')

r.send(b'262:MEQCIBqYgFgdoMXZJouXwPFXxtdMvwDQP39d7YP4rLy7vHBhAiBk1MvEZXzzbh7H1lHb5Em1XAqyUVgVhuJPY2864mSGMA==\n')

recvuntil(b'Talk to Richard.\n')

r.send(b'0\n')

nline = recvline()
n = int(nline.strip().split(': ')[1])
e = 65537
recvuntil(b'What is your name?\n')

alice = int.from_bytes(b'Alice\x00\x05', 'big')
nn = 0
ll = 0
for k in range(1, 10000):
    nn = n * k + alice
    b = int.to_bytes(nn, 1000, 'big').lstrip(b'\x00')
    ll = len(b)
    if nn % (1 << 16) == ll - 2:
        break

assert(nn != 0)
assert(ll == (nn.bit_length() + 7) // 8)

hnn = hexlify(int.to_bytes(nn >> 16, ll - 2, 'big'))
r.send(hnn + b'\n')

recvuntil(b'What is your key?\n')
key = os.urandom(128)
r.send(hexlify(key) + b'\n')

recvline()
certline = recvline()
cert = int(certline.strip())

recvuntil(b'Talk to Richard.\n')
r.send(b'1\n')
line1 = recvline()
line2 = recvline()

r.send(certline)
r.interactive()
