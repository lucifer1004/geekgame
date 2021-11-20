# 最强大脑

## Flag1

获得源码后，注意到程序将`flag1`的内容拷贝到了`data`的最后部分。但`data`的长度为4096，而交互端最多输入4094个字符，也就是2047个BF操作符。如果采用最粗暴的`>.`方式，将超过这一限制。

经过搜索，在[Stack Exchange](https://codegolf.stackexchange.com/questions/54432/brainf-code-golf-challenge-write-a-brainf-program-that-searches-for-the)找到了合适的代码，也即移动到第一个非零位。之后再逐位输出即得到Flag`flag{N0_tRaining_@_@Ll}`。

## Flag2
