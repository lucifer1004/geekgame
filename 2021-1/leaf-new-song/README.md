# 叶子的新歌

用`exiftool`查看元数据，看到提示`Secret in Album Cover!`。

再用`FFMPEG`提取封面图片：

```bash
ffmpeg -i LeafNewSong.mp3 cover.png
```

![Album Cover](./cover.png)

用`stegsolve`提取RGB三个通道的最低位（LSB First），得到一张二维码

![Aztec code extracted from LSB](./bit0.png)

这种中心有一个方框定位的属于Aztec码。用iOS自带的扫码器扫描得到文本`Gur frperg va uvfgbtenz.`。但直接套上`flag{...}`进行提交并不对。

用凯撒密码轮转13位，得到`The secret in histogram.`。按照提示，使用`Audacity`查看音频文件。
