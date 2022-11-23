# 给钱不要

查看网站前端源码可知，按下 `Go` 按钮时，进行了对 `location.href` 的赋值操作。这是一个危险操作，因为会自动执行 `javascript:` 标签语句。

对此，`XSSBOT` 的防范是使用 `Chrome Omnibox` 进行安全检查。

根据提示，阅读 `omnibox` 有关源码，在 [`autocomplete_input.cc`](https://github.com/chromium/chromium/blob/main/components/omnibox/browser/autocomplete_input.cc) 中找到如下的代码：

```cpp
  // Treat javascript: scheme queries followed by things that are unlikely to
  // be code as UNKNOWN, rather than script to execute (URL).
  if (base::EqualsCaseInsensitiveASCII(parsed_scheme_utf8,
                                       url::kJavaScriptScheme) &&
      RE2::FullMatch(base::UTF16ToUTF8(text), "(?i)javascript:([^;=().\"]*)")) {
    return metrics::OmniboxInputType::UNKNOWN;
  }
```

可以看到，如果 `javascript:` 语句中不包含 `;=()."`，就不会被识别为 `url`，而是会识别为 `unknown`。那么，如何不使用这些字符，而又能执行我们想要的操作呢？

- `"` 可以用 `'` 直接代替
- `a.b` 可以用 `a['b']` 代替
- 函数调用可以用 `apply` + [模板字面量](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates) 代替

## Flag 2

可以看到 `XSSBOT` 直接将 Flag 2 放在了 `<p class="flag"></p` 标签中，而我们是可以得到按下 `Go` 按钮后的页面标题的。所以我们只要将页面标题设置为包含 Flag 2 的标签的内容即可。

使用的代码为：

```javascript
javascript: Object['assign']['apply']`${[document, { 'title': document['getElementsByClassName']`flag`[0]['innerText'] }]}`
```

## Flag 1

Flag 2 需要的安全等级为 `safe`，但是 Flag 1 需要的安全等级为 `very safe`，也即只有被识别为 `query` 才可以通过。

没做出来。
