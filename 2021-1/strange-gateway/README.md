# 诡异的网关

下载解压后运行网关程序，在用户名处的下拉列表里看见名为`flag`的用户，猜测对应的密码即是本题的Flag。但是密码无法直接复制。

首先考虑密码可能保存在本地的配置文件中。尝试删除所有用户信息，发现目录下只有`config`文件的修改日期有更新，但与事先备份的内容进行比较，并无差异。

接下来猜测密码保存在内存中。上`VMWare`，在虚拟机里下载这个网关程序并运行，之后暂停虚拟机，用`Volatility`读取`.vmem`文件。首先用`volatility -f mem.vmem --profile=Win7SP1x64 psscan`扫描出所有进程，找到`ipgwclient.exe`的`PID`。然后把它对应的信息dump出来：`volatility -f mem.vmem --profile=Win7SP1x64 memdump -p <PID> -D ./`。得到`PID.dump`文件后，`strings PID.dump | grep flag{`即得到本题的Flag：`flag{h0w_Did_you_g3T_th3_passw0rd?}`
