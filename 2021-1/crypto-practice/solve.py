import os
from rsa import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from binascii import hexlify, unhexlify


def MESsolve(raw, encoded):
    a = bytes_to_long(raw[0:8])
    b = bytes_to_long(raw[8:16])
    c = bytes_to_long(raw[16:24])
    d = bytes_to_long(raw[24:32])
    A = bytes_to_long(encoded[0:8])
    B = bytes_to_long(encoded[8:16])
    C = bytes_to_long(encoded[16:24])
    D = bytes_to_long(encoded[24:32])
    return A ^ c, B ^ d, C ^ (a ^ c), D ^ (b ^ d)


def MESdec(encoded, key):
    raw = b''
    k1, k2, k3, k4 = key
    for i in range(8):
        mess = encoded[i * 32: (i + 1) * 32]
        A = bytes_to_long(mess[0:8])
        B = bytes_to_long(mess[8:16])
        C = bytes_to_long(mess[16:24])
        D = bytes_to_long(mess[24:32])
        c = A ^ k1
        d = B ^ k2
        a = C ^ k3 ^ c
        b = D ^ k4 ^ d
        raw += long_to_bytes(a) + long_to_bytes(b) + \
            long_to_bytes(c) + long_to_bytes(d)

    return raw


def MESenc2(raw, key):
    encoded = b''
    k1, k2, k3, k4 = key
    for it in range(0, len(raw), 32):
        mess = raw[it: it + 32]
        a = bytes_to_long(mess[0:8])
        b = bytes_to_long(mess[8:16])
        c = bytes_to_long(mess[16:24])
        d = bytes_to_long(mess[24:32])
        A = c ^ k1
        B = d ^ k2
        C = a ^ c ^ k3
        D = b ^ d ^ k4
        encoded += long_to_bytes(A) + long_to_bytes(B) + \
            long_to_bytes(C) + long_to_bytes(D)

    return encoded


# encoded_welcome = input('Please enter the encoded welcome message:')
encoded_welcome = b'31cf2a75ef73e7236e13017f4dfd91382a3d394e6036a7acb15e993039ff5dfc22c97c66aa6ceb656e5c0d6218ecd4230e31735b3571f28db127963a6af809e752b71d149d16995200246f072f98a6466e431a34081e8df1d1188f2d2be809b5'
key = MESsolve(pad(('Sorry, I forget to verify your identity. Please give me your certificate.').encode(
    'utf-8')), unhexlify(encoded_welcome))

# encoded_flag = input('Please enter the encoded flag message:')
encoded_flag = b'32c9666faa66e7337213017f4dafc52632316b4a3323a7b4e15195277fe834e236d42a6af93bae237b521f6b7eca800211692d4f6e35bdcba42d80334dcb51941ac1645cc556c8381f3b70183087b9592639494a5d5afc89d062cc7a4d8532d9'
print(MESdec(unhexlify(encoded_flag), key))

mess1 = pad(("I can give you the second flag n").encode("utf-8"))
encoded = b'0e02b10c7f40638befa71aebc9adcb5bf1bf54869832a87fc1dbc88be147920d3414d0202b505388feeb08cef8a68256edfe78ebeb76df7cd5c8dab1d3589c0f051a9f71142d02eb85897289a6c4e53b87f370ecd820e619b0a0cdff930bd450'
key = MESsolve(mess1, unhexlify(encoded))
print(MESdec(unhexlify(encoded), key))