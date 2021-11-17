# 翻车的谜语人

## Flag 1

使用`Wireshark`的`File-Extract Objects`功能从抓包数据中获取传输的所有文件，发现其中包含几个`Jupyter Notebook`文件，并能看到`flag1.txt`和`flag2.7z`。

打开`flag1.txt%3ftype=file&format=text&_=1636184605693`，内容为

```json
{"name": "flag1.txt", "path": "flag1.txt", "last_modified": "2021-11-06T07:43:20.952991Z", "created": "2021-11-06T07:43:20.952991Z", "content": "788c3a1289cbe5383466f9184b07edac6a6b3b37f78e0f7ce79bece502d63091ef5b7087bc44", "format": "text", "mimetype": "text/plain", "size": 76, "writable": true, "type": "file"}
```

说明`flag1.txt`的内容为`788c3a1289cbe5383466f9184b07edac6a6b3b37f78e0f7ce79bece502d63091ef5b7087bc44`。

结合`Untitled(1).ipynb`中的内容

```json
{"type":"notebook","content":{"cells":[{"metadata":{"trusted":true},"cell_type":"code","source":"import zwsp_steg\nfrom Crypto.Random import get_random_bytes","execution_count":26,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"import binascii","execution_count":27,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"def genflag():\n    return 'flag{%s}'%binascii.hexlify(get_random_bytes(16)).decode()","execution_count":28,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"flag1 = genflag()\nflag2 = genflag()","execution_count":29,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"key = get_random_bytes(len(flag1))","execution_count":30,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"key","execution_count":31,"outputs":[{"output_type":"execute_result","execution_count":31,"data":{"text/plain":"b'\\x1e\\xe0[u\\xf2\\xf2\\x81\\x01U_\\x9d!yc\\x8e\\xce[X\\r\\x04\\x94\\xbc9\\x1d\\xd7\\xf8\\xde\\xdcd\\xb2Q\\xa3\\x8a?\\x16\\xe5\\x8a9'"},"metadata":{}}]},{"metadata":{"trusted":true},"cell_type":"code","source":"def xor_each(k, b):\n    assert len(k)==len(b)\n    out = []\n    for i in range(len(b)):\n        out.append(b[i]^k[i])\n    return bytes(out)","execution_count":32,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"encoded_flag1 = xor_each(key, flag1.encode())\nencoded_flag2 = xor_each(key, flag2.encode())","execution_count":33,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"with open('flag1.txt', 'wb') as f:\n    f.write(binascii.hexlify(encoded_flag1))","execution_count":35,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"","execution_count":null,"outputs":[]}],"metadata":{"kernelspec":{"name":"python3","display_name":"Python 3 (ipykernel)","language":"python"},"language_info":{"name":"python","version":"3.8.3rc1","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"}},"nbformat":4,"nbformat_minor":4}}
```

可知生成flag的过程为

```python
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


flag1 = genflag()
flag2 = genflag()
key = get_random_bytes(len(flag1))
key
encoded_flag1 = xor_each(key, flag1.encode())
encoded_flag2 = xor_each(key, flag2.encode())

with open('flag1.txt', 'wb') as f:
    f.write(binascii.hexlify(encoded_flag1))

with open('flag2.txt', 'wb') as f:
    f.write(binascii.hexlify(encoded_flag2))
```

其中`key`代码块单独执行时得到了输出`b'\\x1e\\xe0[u\\xf2\\xf2\\x81\\x01U_\\x9d!yc\\x8e\\xce[X\\r\\x04\\x94\\xbc9\\x1d\\xd7\\xf8\\xde\\xdcd\\xb2Q\\xa3\\x8a?\\x16\\xe5\\x8a9'`。但要注意这里的表示经过了二次转义，需要把`\\x`替换为`\x`，把`\\r`替换为`\r`，才能得到`key`的真实值

```python
key = b'\x1e\xe0[u\xf2\xf2\x81\x01U_\x9d!yc\x8e\xce[X\r\x04\x94\xbc9\x1d\xd7\xf8\xde\xdcd\xb2Q\xa3\x8a?\x16\xe5\x8a9'
```

再结合上面的代码，即可求得`flag1`

```python
encoded_flag1 = binascii.unhexlify(
    b'788c3a1289cbe5383466f9184b07edac6a6b3b37f78e0f7ce79bece502d63091ef5b7087bc44')

flag1 = xor_each(key, encoded_flag1)
```

## Flag 2

将`flag2.7z%3fdownload=1`重命名为`flag2.7z`后尝试解压，发现需要密码。

同时，在`Wireshark`中搜索`7z`，跟踪到编号为`11`的TCP流，能够判断出其中记录了终端操作的信息，且包含了对`flag2`的加密过程。

分析发现，首先将`flag2.txt`的内容使用`stego-lsb`包隐写到了`ringtrain.wav`文件中，然后又用`7zip`对得到的`.wav`文件进行了加密。

继续观察终端输出定位到加密时的操作为

```bash
7z ... -p"Wakarimasu! `date` `uname -nom` `nproc`"
```

但需要填入对应的`date`，`uname -nom`和`nproc`。

后两个容易得到，`uname -nom=you-kali-vm x86_64 GNU/Linux`，`nproc=8`；但`date`则需要获取到这一条命令的执行时间，精确到秒。这可以通过最后输入`\r`时的时间获得。

使用密码`Wakarimasu! SAT 06 Nov 2021 03:44:15 AM you-kali-vm x86_64 GNU/Linux 8`成功解压得到`flag2.wav`文件。

使用`stegolsb wavsteg -r -i flag2.wav -o flag2.txt -n 1 -b 76`还原出`flag2.txt`。

使用同样的方法即可还原出`flag2`。
