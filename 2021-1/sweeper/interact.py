import os
from binascii import *
from pwn import *
import mt_recover


r = remote('prob09.geekgame.pku.edu.cn', 10009)


def recvline():
    b = r.recvuntil(b'\n')
    line = str(b, 'utf-8')
    return line


def recvuntil(until):
    b = r.recvuntil(until)
    line = str(b, 'utf-8')
    return line


recvuntil(b'token: ')

r.send(b'262:MEQCIBqYgFgdoMXZJouXwPFXxtdMvwDQP39d7YP4rLy7vHBhAiBk1MvEZXzzbh7H1lHb5Em1XAqyUVgVhuJPY2864mSGMA==\n')

recvuntil(b'easy mode? (y/n)')

r.send(b'n\n')

recvuntil(b'New Game!\n')

WIDTH = 16
HEIGHT = 16


def attempt(x, y):
    r.send(bytes(f'{x} {y}', 'utf-8') + b'\n')
    line = recvline().strip()
    if 'BOOM' in line:
        return -1
    elif 'You win' in line:
        line = recvline().strip()
        print(line)
        r.interactive()
    else:
        try:
            code = int(line[2:])
            return code
        except Exception:
            return -1


ss = []

for rnd in range(84):
    for i in range(0, HEIGHT):
        code = attempt(0, i)
        if code == -1:
            result = recvuntil(b'try again? (y/n)')
            res = result.split('\n')[:16]
            s = 0
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    idx = i * WIDTH + j
                    if res[i][j] == '*':
                        s |= 1 << idx
            ss.append(s)
            r.send(b'y\n')
            recvline()
            break

mtb = mt_recover.MT19937Recover()
sss = []
for s in ss:
    t = []
    for i in range(8):
        t.append(s % (1 << 32))
        s >>= 32
    sss += t

r2 = mtb.go(sss)
bits = r2.getrandbits(256)

for i in range(HEIGHT):
    for j in range(WIDTH):
        idx = i * WIDTH + j
        if bits & (1 << idx):
            continue
        print(i, j)
        code = attempt(i, j)

r.interactive()
