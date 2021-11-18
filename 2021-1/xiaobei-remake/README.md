# 小北问答 Remake

## 第一题

最高编号为理科五号楼。因此答案为`5`。

## 第二题

从北京大学新闻网的相关[报道](https://news.pku.edu.cn/xwzh/203d197d93c245a1aec23626bb43d464.htm)中得到答案`407`。

## 第三题

在[crt.sh](https://crt.sh)查询`geekgame.pku.edu.cn`，得到证书签发历史。比较证书开始和结束时间，发现在2021年7月11日至14日之间有一段证书缺失的时间。查看编号为`4362003382`的证书的详情，得到准确的过期时间`Jul 11 00:49:53 2021 GMT`，再转换为格式要求的`+8`时区，得到最后的答案`2021-07-11T08:49:53+08:00`。

## 第四题

找到DC2020资格赛签到题的[归档页](https://archive.ooo/c/welcome-to-dc2020-quals/358/)，下载`welcome.txt`得到答案`OOO{this_is_the_welcome_flag}`。

## 第五题

在[OEIS-A047659](https://oeis.org/A047659)的正文中找到公式：

$$F(m,n)=n^3/6*(m^3 - 3m^2 + 2m) - n^2/2*(3m^3 - 9m^2 + 6m) + n/6*(2m^4 + 20m^3 - 77m^2 + 58m) - 1/24*(39m^4 - 82m^3 - 36m^2 + 88m) + 1/16*(2m - 4n + 1)*(1 + (-1)^{m+1}) + 1/2*(1 + |n - 2m + 3| - |n - 2m + 4|)*(1/24*((n - 2m + 11)^4 - 42*(n - 2m + 11)^3 + 656*(n - 2m + 11)^2 - 4518*(n - 2m + 11) + 11583) - 1/16*(4m - 2n - 1)*(1 + (-1)^{n+1}))\quad m\le n,n\ge3$$

高精度

```python
from fractions import *

def F(m, n):
  if m > n:
    m, n = n, m
    
  assert(n >= 3)
  
  return Fraction(n**3,6)*(m**3 - 3*m**2 + 2*m) - Fraction(n**2,2)*(3*m**3 - 9*m**2 + 6*m) + Fraction(n,6)*(2*m**4 + 20*m**3 - 77*m**2 + 58*m) - Fraction(1, 24)*(39*m**4 - 82*m**3 - 36*m**2 + 88*m) + Fraction(1, 16)*(2*m - 4*n + 1)*(1 + (-1)**(m+1)) + Fraction(1,2)*(1 + abs(n - 2*m + 3) - abs(n - 2*m + 4))*(Fraction(1, 24)*((n - 2*m + 11)**4 - 42*(n - 2*m + 11)**3 + 656*(n - 2*m + 11)**2 - 4518*(n - 2*m + 11) + 11583) - Fraction(1, 16)*(4*m - 2*n - 1)*(1 + (-1)**(n+1))) 
```

计算得到答案`2933523260166137923998409309647057493882806525577536`。

## 第六题

根据上届比赛归档中小北问答一题的[源码](https://github.com/PKU-GeekGame/geekgame-0th/blob/main/src/choice/game/db.py)，得到答案`submits`。

## 第七题

搜索`Peking University ASN`找到北大AS在[IPInfo](https://ipinfo.io/AS59201)的页面，得到答案`AS59201`。

## 第八题

在[信科官网](https://eecs.pku.edu.cn/)检索得到答案`区域光纤通信网与新型光通信系统国家重点实验室`。
