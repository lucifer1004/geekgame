stor2 = 0x15eea4b2551f0c96d02a5d62f84cac8112690d68c47b16814e221b8a37d6c4d3
stor3 = 0x293edea661635aabcd6deba615ab813a7610c1cfb9efb31ccc5224c0e4b37372

flag = [0] * 64

for idx in range(64):
    target = stor3 >> idx * 4 & 15
    for i in range(16):
        if i + idx * 5 + (stor2 >> idx * 4) * 7 & 15 == target:
            flag[63 - idx] = i
            break

h = ''.join(map(lambda x: hex(x)[2:], flag))
print(bytes.fromhex(h).lstrip(b'\x00'))
