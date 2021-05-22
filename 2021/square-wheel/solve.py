import requests
import urllib
import re
import requests

from bs4 import BeautifulSoup
from base64 import b64encode, b64decode


def gen_ticket(name, stuid, mode='cbc'):
    name = urllib.parse.quote(name)
    stuid = urllib.parse.quote(stuid)
    url = f'http://prob12.geekgame.pku.edu.cn/{mode}/gen-ticket?name={name}&stuid={stuid}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find_all('p')[1].text


def query_ticket(ticket, mode='cbc'):
    ticket = urllib.parse.quote(ticket)
    url = f'http://prob12.geekgame.pku.edu.cn/{mode}/query-ticket?ticket={ticket}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    value = [bytes(str(b.parent).split('</b>')[1].split('</p>')[0].strip().encode())
             for b in soup.find_all('b', string=re.compile(r'^.*$'))]
    return value


def get_flag(ticket, code, token, mode='cbc'):
    ticket = urllib.parse.quote(ticket)
    code = urllib.parse.quote(code)
    token = urllib.parse.quote(token)
    url = f'http://prob12.geekgame.pku.edu.cn/{mode}/getflag?ticket={ticket}&redeem_code={code}&token={token}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find_all('p')[1].text


token = input('Please input your token:')

# Flag 1
name = '0' * 10
stuid = '0000000000'
cbc = gen_ticket(name, stuid)
b = b64decode(cbc)
c = list(b)
c[38] ^= ord('F') ^ ord('T')
c[39] ^= ord('a') ^ ord('r')
c[40] ^= ord('l') ^ ord('u')
c[41] ^= ord('s') ^ ord('e')
c[42] ^= ord('e') ^ ord('|')
ticket = b64encode(bytes(c)).decode()
print('Your CBC ticket:', ticket)
query = query_ticket(ticket)
assert(len(query) == 5 and query[2] == b'True')

code = None
for ch in '+-*/':
    for i in range(len(b)):
        c = list(b)
        c[i] = ord(ch)
        query = query_ticket(b64encode(bytes(c)))
        for j in range(len(query)):
            if b'code=' in query[j]:
                code = query[j][query[j].index(b'code=') + 5:].decode()
                print('Your CBC gift code:', code)
                break
        if code:
            break
    if code:
        break

flag1 = get_flag(ticket, code, token)
print('Flag 1:', flag1)

# Flag2

name = '|flag=True'
stuid = '0000000000'
flag2 = None

while not flag2:
    ecb = gen_ticket(name, stuid, 'ecb')
    b = b64decode(ecb)
    b = list(b)
    c = b[:16] + b[48:64] + b[32:48] + b[16:32] + b[64:]
    query = query_ticket(b64encode(bytes(c)), 'ecb')
    assert(len(query) == 5 and b'=' in query[1])
    code = query[1][query[1].index(b'=') + 1:].decode()

    for i in range(256):
        c = b[:16] + b[32:64] + b[16:32] + b[64:]
        c[64] = i
        query = query_ticket(b64encode(bytes(c)), 'ecb')
        if len(query) == 5 and query[2] == b'True':
            flag2 = get_flag(b64encode(bytes(c)), code, token, 'ecb')
            print('Your ECB ticket:', b64encode(bytes(c)).decode())
            print('Your ECB gift code:', code)
            print('Flag 2:', flag2)
            exit(0)
