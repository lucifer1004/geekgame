import binascii
import zwsp_steg
from Crypto.Random import get_random_bytes


def genflag():
    return 'flag{%s}' % binascii.hexlify(get_random_bytes(16)).decode()


def xor_each(k, b):
    assert len(k) == len(b)
    out = []
    for i in range(len(b)):
        out.append(b[i] ^ k[i])
    return bytes(out)


# flag1 = genflag()
# flag2 = genflag()
# key = get_random_bytes(len(flag1))
# encoded_flag1 = xor_each(key, flag1.encode())
# encoded_flag2 = xor_each(key, flag2.encode())

# print(len(flag1), len(key), len(encoded_flag1))

# with open('flag1.txt', 'wb') as f:
#     f.write(binascii.hexlify(encoded_flag1))

# with open('flag2.txt', 'wb') as f:
#     f.write(binascii.hexlify(encoded_flag2))

key = b'\x1e\xe0[u\xf2\xf2\x81\x01U_\x9d!yc\x8e\xce[X\r\x04\x94\xbc9\x1d\xd7\xf8\xde\xdcd\xb2Q\xa3\x8a?\x16\xe5\x8a9'

encoded_flag1 = binascii.unhexlify(
    b'788c3a1289cbe5383466f9184b07edac6a6b3b37f78e0f7ce79bece502d63091ef5b7087bc44')

flag1 = xor_each(key, encoded_flag1)

print(flag1)

encoded_flag2 = binascii.unhexlify(
    b'788c3a128994e765373cfc171c00edfb3f603b67f68b087eb69cb8b8508135c5b90920d1b344')

flag2 = xor_each(key, encoded_flag2)

print(flag2)
