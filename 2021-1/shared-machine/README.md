# 共享的机器

在[Etherscan](https://ropsten.etherscan.io/bytecode-decompiler?a=0xa43028c702c3B119C749306461582bF647Fd770a)上直接反编译智能合约，得到类Python语言的结果：

```python
#
#  Panoramix v4 Oct 2019 
#  Decompiled source of ropsten:0xa43028c702c3B119C749306461582bF647Fd770a
# 
#  Let's make the world open source 
# 

def storage:
  stor0 is addr at storage 0
  stor1 is uint256 at storage 1
  stor2 is uint256 at storage 2
  stor3 is uint256 at storage 3

def _fallback() payable: # default function
  revert

def unknown7fbf5e5a(uint256 _param1, uint256 _param2) payable: 
  require calldata.size - 4 >= 64
  if stor0 != caller:
      if stor0 != tx.origin:
          if stor1 != sha3(caller):
              if stor1 != sha3(tx.origin):
                  revert with 0, 'caller must be owner'
  stor2 = _param1
  stor3 = _param2

def unknownded0677d(uint256 _param1) payable: 
  require calldata.size - 4 >= 32
  idx = 0
  s = 0
  while idx < 64:
      idx = idx + 1
      s = s or (Mask(256, -4 * idx, _param1) >> 4 * idx) + (5 * idx) + (7 * Mask(256, -4 * idx, stor2) >> 4 * idx) % 16 << 4 * idx
      continue 
  if stor3 != 0:
      revert with 0, 'this is not the real flag!'
  return 1
```

合约的大致意思是，需要输入一个`param`，使得其与`stor2`经过运算后的结果与`stor3`相等。

在装有MetaMask钱包插件的浏览器中执行下面的查询语句：

```js
try {
  const value = await ethereum.request({
    method: 'eth_getStorageAt',
    params: ['0xa43028c702c3B119C749306461582bF647Fd770a', '2'],
  })
  console.log('stor2:', value)
} catch (error) {
  console.error(error)
}

// stor2: 0x15eea4b2551f0c96d02a5d62f84cac8112690d68c47b16814e221b8a37d6c4d3

try {
  const value = await ethereum.request({
    method: 'eth_getStorageAt',
    params: ['0xa43028c702c3B119C749306461582bF647Fd770a', '3'],
  })
  console.log('stor3:', value)
} catch (error) {
  console.error(error)
}

// stor3: 0x293edea661635aabcd6deba615ab813a7610c1cfb9efb31ccc5224c0e4b37372
```

得到`stor2`和`stor3`的具体数值。

问题是上面反编译结果中的运算部分使用的`Mask`函数，虽然可以推测是一个位掩码，但没有查到具体的定义。保险起见，使用[Online Solidify Decompiler](https://ethervm.io/decompile/ropsten/0xa43028c702c3B119C749306461582bF647Fd770a)再次反编译得到类Solidity的结果

```solidity
contract Contract {
    function main() {
        memory[0x40:0x60] = 0x80;
        var var0 = msg.value;
    
        if (var0) { revert(memory[0x00:0x00]); }
    
        if (msg.data.length < 0x04) { revert(memory[0x00:0x00]); }
    
        var0 = msg.data[0x00:0x20] >> 0xe0;
    
        if (var0 == 0x7fbf5e5a) {
            // Dispatch table entry for 0x7fbf5e5a (unknown)
            var var1 = 0x0071;
            var var2 = 0x04;
            var var3 = msg.data.length - var2;
        
            if (var3 < 0x40) { revert(memory[0x00:0x00]); }
        
            func_0051(var2, var3);
            stop();
        } else if (var0 == 0xded0677d) {
            // Dispatch table entry for 0xded0677d (unknown)
            var1 = 0x009f;
            var2 = 0x04;
            var3 = msg.data.length - var2;
        
            if (var3 < 0x20) { revert(memory[0x00:0x00]); }
        
            var1 = func_0089(var2, var3);
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = !!var1;
            var temp1 = memory[0x40:0x60];
            return memory[temp1:temp1 + (temp0 + 0x20) - temp1];
        } else { revert(memory[0x00:0x00]); }
    }
    
    function func_0051(var arg0, var arg1) {
        var temp0 = arg0;
        arg0 = msg.data[temp0:temp0 + 0x20];
        arg1 = msg.data[temp0 + 0x20:temp0 + 0x20 + 0x20];
        var temp1 = memory[0x40:0x60] + 0x20;
        memory[temp1:temp1 + 0x20] = msg.sender;
        var temp2 = temp1 + 0x20;
        var temp3 = memory[0x40:0x60];
        memory[temp3:temp3 + 0x20] = temp2 - temp3 - 0x20;
        memory[0x40:0x60] = temp2;
        var var0 = keccak256(memory[temp3 + 0x20:temp3 + 0x20 + memory[temp3:temp3 + 0x20]]) >> 0x00;
        var temp4 = memory[0x40:0x60] + 0x20;
        memory[temp4:temp4 + 0x20] = tx.origin;
        var temp5 = temp4 + 0x20;
        var temp6 = memory[0x40:0x60];
        memory[temp6:temp6 + 0x20] = temp5 - temp6 - 0x20;
        memory[0x40:0x60] = temp5;
        var var1 = keccak256(memory[temp6 + 0x20:temp6 + 0x20 + memory[temp6:temp6 + 0x20]]) >> 0x00;
        var var2 = storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff == msg.sender;
    
        if (!var2) {
            var2 = storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff == tx.origin;
        
            if (var2) { goto label_0220; }
            else { goto label_021A; }
        } else if (var2) {
        label_0220:
        
            if (var2) {
            label_022C:
            
                if (var2) {
                label_029E:
                    storage[0x02] = arg0;
                    storage[0x03] = arg1;
                    return;
                } else {
                label_0231:
                    var temp7 = memory[0x40:0x60];
                    memory[temp7:temp7 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
                    var temp8 = temp7 + 0x04;
                    var temp9 = temp8 + 0x20;
                    memory[temp8:temp8 + 0x20] = temp9 - temp8;
                    memory[temp9:temp9 + 0x20] = 0x14;
                    var temp10 = temp9 + 0x20;
                    memory[temp10:temp10 + 0x20] = 0x63616c6c6572206d757374206265206f776e6572000000000000000000000000;
                    var temp11 = memory[0x40:0x60];
                    revert(memory[temp11:temp11 + (temp10 + 0x20) - temp11]);
                }
            } else {
            label_0226:
            
                if (storage[0x01] == var1) { goto label_029E; }
                else { goto label_0231; }
            }
        } else {
        label_021A:
            var2 = storage[0x01] == var0;
        
            if (var2) { goto label_022C; }
            else { goto label_0226; }
        }
    }
    
    function func_0089(var arg0, var arg1) returns (var r0) {
        arg0 = msg.data[arg0:arg0 + 0x20];
        arg1 = 0x00;
        var var0 = 0x00;
        var var1 = 0x00;
    
        if (var1 >= 0x40) {
        label_0301:
        
            if (var0 == storage[0x03]) { return 0x01; }
        
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
            var temp1 = temp0 + 0x04;
            var temp2 = temp1 + 0x20;
            memory[temp1:temp1 + 0x20] = temp2 - temp1;
            memory[temp2:temp2 + 0x20] = 0x1a;
            var temp3 = temp2 + 0x20;
            memory[temp3:temp3 + 0x20] = 0x74686973206973206e6f7420746865207265616c20666c616721000000000000;
            var temp4 = memory[0x40:0x60];
            revert(memory[temp4:temp4 + (temp3 + 0x20) - temp4]);
        } else {
        label_02C9:
            var temp5 = var1;
            var0 = var0 | (((arg0 >> temp5 * 0x04) + temp5 * 0x05 + (storage[0x02] >> temp5 * 0x04) * 0x07 & 0x0f) << temp5 * 0x04);
            var1 = temp5 + 0x01;
        
            if (var1 >= 0x40) { goto label_0301; }
            else { goto label_02C9; }
        }
    }
}
```

从中确认了运算的执行方式

```solidity
var0 = var0 | (((arg0 >> temp5 * 0x04) + temp5 * 0x05 + (storage[0x02] >> temp5 * 0x04) * 0x07 & 0x0f) << temp5 * 0x04);
```

接下来依次枚举十六进制下每一位的数值即可还原出Flag。

```python
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

# b'flag{N0_S3cReT_ON_EThEreuM}'
```
