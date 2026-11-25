# template / url / base64 / hash / compress / binary

## template：模板渲染

基于 Go `text/template` 与 `html/template`。

```zgg
println(@template.renderText('hello {{.name}}', {name: 'zgg'}))
// hello zgg

println(@template.renderText('{{range .items}}[{{.}}]{{end}}', {items: [1, 2, 3]}))
// [1][2][3]

println(@template.renderHtml('<p>{{.name}}</p>', {name: 'zgg'}))
// <p>zgg</p>（HTML 转义）
```

| 方法 | 说明 |
|---|---|
| `renderText(src, params?)` | 文本模板 |
| `renderHtml(src, params?)` | HTML 模板（自动转义） |

模板语法即 Go template：`{{.Field}}`、`{{range}}`、`{{if}}`、`{{end}}`。

## url：URL 编解码

```zgg
println(@url.encodeURIComponent('a b&c'))     // a+b%26c
println(@url.decodeURIComponent('a%20b%26c')) // a b&c
println(@url.encodeForm({a: 1, b: 'x y'}))    // a=1&b=x+y
println(@url.decodeForm('a=1&b=x+y'))         // {a: [1], b: [x y]}
```

| 方法 | 说明 |
|---|---|
| `encodeURIComponent(s)` | 组件编码 |
| `decodeURIComponent(s)` | 组件解码 |
| `encodeForm(obj)` | 表单编码 |
| `decodeForm(str)` | 表单解码（值为数组） |

## base64

```zgg
println(@base64.encode('hello'))        // aGVsbG8=
println(@base64.decode('aGVsbG8='))     // hello
println(@base64.encodeN('hello', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))
```

| 方法 | 说明 |
|---|---|
| `encode(v)` / `decode(s)` | 标准 Base64（带填充） |
| `encodeN(v, alphabet)` / `decodeN(s, alphabet)` | 自定义字符表编码 |

`decode` 返回 `Bytes`，需要字符串时用 `str(...)`。

## hash：摘要与 HMAC

```zgg
h := @hash
println(h.md5('hello').hex())
println(h.sha1('hello').hex())
println(h.sha256('hello').hex())
println(h.crc32('hello'))                 // 整数
println(h.hmac.sha256('key', 'msg').hex())
```

| 成员 | 返回 |
|---|---|
| `md5` / `sha1` / `sha256` / `fnv128` 等 | `Bytes`（用 `.hex()` 转十六进制） |
| `crc32` / `fnv32` / `crc64iso` 等 | `Int` |
| `hmac.md5` / `hmac.sha1` / `hmac.sha256` | `Bytes` |

> 注意与内置函数区分：`md5('x')`（内置）返回十六进制字符串，`@hash.md5('x')` 返回 `Bytes`。

## compress：压缩

```zgg
c := @compress
data := c.GZIP.compress('hello world')
println(data.len())              // 压缩后字节数
println(c.GZIP.decompress(data)) // hello world

// 指定压缩级别
c.GZIP.compress('hello', 9)
```

| 算法 | 说明 |
|---|---|
| `GZIP` | gzip |
| `ZLIB` | zlib |
| `FLATE` | raw deflate |

方法：`compress(data[, level])`、`decompress(bytes)`。

## binary：二进制读写

```zgg
w := @binary.Writer()
w.i32(42)
w.u8(7)
w.bytes(bytes('ab'))
bs := w.toBytes()
println(bs.hex())          // 2a000000076162

r := @binary.Reader(bs)
println(r.i32(), r.u8(), r.bytes(2))
```

| Writer | Reader |
|---|---|
| `i8` `u8` `i16` `u16` `i32` `u32` `i64` | 同名读取方法 |
| `varint` / `uvarint` | `varint` / `uvarint` |
| `bytes(b)` | `bytes(n)` |
| `toBytes()` | — |

适合自定义二进制协议、解析文件头。

## msgpack

```zgg
data := @msgpack.encode({a: 1, b: [2, 3]})
println(@msgpack.decode(data))     // {a: 1, b: [2, 3]}
```

比 JSON 更紧凑，适合内部服务通信与缓存。
