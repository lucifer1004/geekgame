# Future Machine

A simple encoder/decoder.

```shell
USAGE:
    future-machine [FLAGS] [OPTIONS] <input>

ARGS:
    <input>    The string to be encoded/decoded

FLAGS:
    -d, --decode-mode    Decode instead of encode
    -h, --help           Prints help information
    -V, --version        Prints version information

OPTIONS:
    -i, --iv <iv>            The initial value [default: 114514]
    -m, --modulo <modulo>    The modulo [default: 334363]
        --mul <mul>          The multiplication factor [default: 1919]
    -o, --offset <offset>    The offset [default: 7]
```

