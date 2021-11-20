# 扫雷

## Flag1

一开始尝试通过解扫雷的方法做题。后来发现由于雷数太多，没有一种有效的策略能够达到合理的获胜概率。

根据提示，查阅Python `getrandbits`的实现，了解到底层默认使用了[Mersenne_Twister](https://en.wikipedia.org/wiki/Mersenne_Twister)。而在能够连续获取到至少625个生成结果的情况下，是可以完美还原随机数生成器的状态的。

在困难模式下，不存在重新生成，因此我们可以获取到需要的连续的随机数生成结果。因为本题中棋盘是16*16的，一次生成了256位，对应于`Mersenne Twister`前进8个状态，因此我们进行84轮游戏后，就可以收集到一共632个结果，可以还原出生成器状态。参考[GitHub 项目](https://github.com/eboda/mersenne-twister-recover)实现随机数生成器状态的还原，之后直接生成下一次的棋盘再答题即可。最后得到Flag`flag{easy_to_guess-EAsy_to_sweep}`。

## Flag2

简单模式中，存在开局重随的情况，上面的方法无法直接套用。
