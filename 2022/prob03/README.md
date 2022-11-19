# 智慧检测器

阅读[源码](./src.py)之后发现两处问题：

```py
    DisplayData.append(map[z][0])
    for i in range(1, len(map[z]) - 1):
        DisplayData.append([map[z][i][0]] + [" "]*(size-2) + [map[z][i][-1]])
    DisplayData.append(map[z][-1])
```

```py
                CurPos = NewPos
                if map[CurPos[0]][CurPos[1]][CurPos[2]] == "E":
                    print("Congratulations! You finished within %d moves." %
                          MoveCount)
                    FoundEnd = True
                    break
```

这两处都犯了没有对 `list` 进行深拷贝的错误。利用第二处错误，可以在走了一个合法操作之后再多走一步；利用第一处错误，可以将第一行和最后一行的 `#` 修改为 `@`。下面给出一个利用这两处错误的例子：

```txt
#######
#@    #
# XXX #
#     #
# X   #
#     #
####E##
Input direction and press enter. Available directions: SE R(estart)
SSSSS
Invalid Direction
#######
#     #
#     #
#     #
# X   #
# X   #
#@##E##
Input direction and press enter. Available directions: N R(estart)
NSS
Invalid Direction
got <class 'IndexError'>
flag{game.exe-stops-respondiNg...sEnd-ERror-report?}
```

可以看到，在第一个操作序列（最后一步不合法）后，我们成功地移动到了最后一行上，并且此时最后一行第二格的 `#` 被永久修改为了 `@`。之后我们再进行一个类似的操作序列（最后一步不合法），就成功地将 `CurPos` 修改为了越界值，之后就会触发 `IndexError`，从而得到 flag。
