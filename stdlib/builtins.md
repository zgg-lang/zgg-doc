# 内置函数与类型方法

## 内置函数

无需 `import`，直接调用。

| 函数 | 说明 | 示例 |
|---|---|---|
| `println(...)` | 打印一行，参数按 `str()` 转换 | `println('a', 1)` → `a 1` |
| `printf(fmt, ...)` | 按 Go 格式化输出 | `printf('%d\n', 1)` |
| `sprintf(fmt, ...)` | 格式化并返回字符串 | `sprintf('%03d', 7)` → `007` |
| `int(v[, base])` | 转整数；字符串支持 `0x`/`0b`/`0` 前缀与进制 | `int('ff', 16)` → `255` |
| `float(v)` | 转浮点 | `float('1.5')` |
| `str(v[, base])` | 转字符串；整数可按进制输出 | `str(255, 16)` → `ff` |
| `bytes(v)` | 转字节数组 | `bytes('abc').hex()` |
| `typeName(v)` | 类型展示名 | `typeName(1)` → `<type Int>` |
| `type(v)` | 类型对象 | `type(1).__name__` → `Int` |
| `len(v)` | 长度（字符串/数组/对象/字节） | `len([1, 2])` → `2` |
| `range([begin,] end[, step])` | 生成整数数组（不含 end） | `range(3)` → `[0, 1, 2]` |
| `seq(from, to)` | 按 `__next__` 递增生成序列（含两端） | `seq(1, 5)` → `[1, 2, 3, 4, 5]` |
| `sha1(v)` / `sha256(v)` / `md5(v)` | 摘要，返回**十六进制字符串** | `md5('hello')` |
| `import(name[, reload[, type]])` | 导入模块 | 见[模块](../syntax/modules.md) |
| `isUndefined(v)` / `isCallable(v)` / `isArray(v)` / `isObject(v)` | 类型判断 | `isCallable(println)` → `true` |
| `assertError(v)` | 解包 `(value, error)`（`!` 的函数形式） | `assertError([1, err])` |
| `rand()` / `rand(n)` / `rand(m, n)` | 随机浮点 / `[0, n)` / `[m, n)` | `rand(1, 10)` |
| `eval(code[, sandbox])` | 执行代码字符串（需 `CAN_EVAL=1`） | 见下 |
| `bind(fn, ...args)` | 预绑定参数 | `bind(add, 1)(2)` |
| `max(...)` / `min(...)` | 最大值 / 最小值 | `max(1, 5, 3)` → `5` |
| `input([prompt])` | 读一行标准输入 | `input('name? ')` |
| `lookup(value, path)` | 按 JSONPath 取值 | `lookup(o, r'$.a.b')` |

### 示例

```zgg
println(range(5))                 // [0, 1, 2, 3, 4]
println(range(2, 6))              // [2, 3, 4, 5]
println(range(1, 10, 3))          // [1, 4, 7]
println(seq(1, 5))                // [1, 2, 3, 4, 5]
println(int('0x10'), int('101', 2), str(255, 16))
println(md5('hello'))
println(lookup({a: {b: 2}}, r'$.a.b'))
println(max(1, 5, 3), min(1, 5, 3))
```

> 内置的 `md5` / `sha1` / `sha256` 返回十六进制**字符串**；`@hash` 模块的同名函数返回 `Bytes`，需要 `.hex()` 转换。

### eval 与安全

```zgg
// 需要在启动时设置 CAN_EVAL=1
println(eval('1 + 2'))
```

默认禁止 `eval`（防止不可信脚本执行任意代码）。`eval(code, {x: 1})` 可以传入沙箱变量。

### log

`log` 是一个内置对象，按级别输出日志：

```zgg
log.logLevel = log.INFO
log.debug('不会输出')
log.info('info 日志')
log.error('error 日志')
```

输出格式：`2026-11-25 10:47:30|INF|info 日志`。

可用级别：`log.DEBUG` / `log.INFO` / `log.WARN` / `log.ERROR` / `log.ASSERT`，方法同名小写。还可设置 `log.writer`（`io.Writer`）与 `log.handler`（自定义回调）。

## 类型方法速查

完整说明见[字符串](../syntax/strings.md)与[数组与对象](../syntax/collections.md)。

### Str

`upper` `lower` `trim` `substr` `split` `splitr` `lines` `indexOf` `lastIndexOf` `find` `replaceOne` `replaceAll` `replace` `startsWith` `endsWith` `contains` `hash` `code` `codes` `width` `isBlank` `notBlank` `decodeHex` `decodeBase64` `fillParams`

### Array

`map` `filter` `flatMap` `filterMap` `reduce` `sum` `each` `push` `slice` `sort` `join` `toMap` `count` `countIf` `toGroup` `uniq` `chunk` `find` `findIndex` `times` `groupBy` `reverse`

### Object

`keys` `values` `pairs` `each`

### Int / Float

数值支持迭代协议 `__next__`（用于 `seq` 等场景）。

### Bytes

`hex` `base64` `dumpHex` `toArray` `slice`

```zgg
println(bytes('abc').hex())        // 616263
println(bytes('abc').base64())     // YWJj
println(bytes('\x00\x01').toArray())
```

## 静态成员

少数内置类型带静态方法，例如从码点构造字符串：

```zgg
println(Str.fromCodes(97, 98, 99))   // abc
```
