# file 文件操作

```zgg
f := @file
```

| 方法 | 说明 | 返回 |
|---|---|---|
| `readString(path)` | 读整个文件为字符串 | `Str` |
| `readBytes(path)` | 读整个文件为字节 | `Bytes` |
| `readLines(path)` | 按行读取 | `Array<Str>` |
| `rewrite(path, content)` | 覆盖写入（内容可为 `Str` 或 `Bytes`） | 写入字节数 |
| `append(path, content...)` | 追加写入 | 写入字节数 |
| `exists(path[, followLink])` | 是否存在 | `Bool` |
| `isFile(path[, followLink])` | 是否普通文件 | `Bool` |
| `isDir(path[, followLink])` | 是否目录 | `Bool` |

```zgg
@file.rewrite('/tmp/demo.txt', 'hello\nworld\n')

println(@file.readString('/tmp/demo.txt'))
println(@file.readLines('/tmp/demo.txt'))     // [hello, world, ]
println(@file.readBytes('/tmp/demo.txt').len())

println(@file.exists('/tmp/demo.txt'))        // true
println(@file.isFile('/tmp/demo.txt'))        // true
println(@file.isDir('/tmp'))                  // true
```

## 写入二进制

```zgg
@file.rewrite('/tmp/demo.bin', bytes('xyz'))
println(@file.readBytes('/tmp/demo.bin').hex())   // 78797a
```

## 追加写入的替代方案

当前版本 `append` 打开文件时缺少写权限标志，会报：

```text
Exception! write file error: write /tmp/x.txt: bad file descriptor
```

替代写法（读 + 覆盖）：

```zgg
path := '/tmp/log.txt'
old := @file.exists(path) ? @file.readString(path) : ''
@file.rewrite(path, old + 'new line\n')
```

## 常见组合

### 读写 JSON 配置

```zgg
@file.rewrite('/tmp/conf.json', '{"name": "demo", "port": 8080}')

conf := @json.decode(@file.readString('/tmp/conf.json'))
conf.updated = @time.now().format('%Y-%m-%d')
@file.rewrite('/tmp/conf.json', @json.encode(conf, 2))
println(len(@file.readString('/tmp/conf.json')) > 0)
```

### 按行处理大文件

```zgg
count := 0
for line in @file.readLines('/tmp/demo.txt') {
    if line.trim() != '' {
        count += 1
    }
}
println('非空行数：$count')
```

> `readLines` 会保留文件末尾换行产生的空行，过滤时注意 `trim()`。

## 目录遍历

`@file` 不含目录遍历；用 `@path.glob` / `@path.walk`（见 [math/path/misc](math-path-misc.md)），或直接调用 `gostd`：

```zgg
os := import('gostd/os')
entries := os.ReadDir('/tmp')!
for e in entries {
    println(e.Name())
}
```
