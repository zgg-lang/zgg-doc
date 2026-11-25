# 字符串

ZGG 只有**单引号**字符串；双引号不是字符串语法（会报词法错误）。

## 字面量与转义

```zgg
println('hello')
println('it\'s ok')          // 单引号用 \ 转义
println('a\tb\nc')           // \t \n \r \\ \b \f \v
println('\u4f60\u597d')      // 你好
println('\x41')              // A
```

多行字符串直接换行即可：

```zgg
text := '第一行
第二行'
println(text)
```

### 原始字符串

不转义、不插值：

```zgg
println(r'C:\path\to\file')     // C:\path\to\file
println(r'no $interpolation')   // no $interpolation

println('''也可以三个单引号
跨多行''')
```

## 字符串插值

`$name` 插入变量，`${expr}` 插入任意表达式，可嵌套：

```zgg
name := 'ZGG'
println('hello, $name')
println('1 + 2 = ${1 + 2}')
println('嵌套：${name + '(${1 + 2})'}')
```

转义 `$` 用 `\$`：

```zgg
println('\$100')      // $100
println(r'$100')      // $100
```

> 所有单引号串都会做 `$` 插值。写 JSONPath、模板占位等含 `$` 的文本时，请用 `r'...'` 或 `'\$...'`。
>
> 注意 `$` 后面必须跟标识符或 `{`：`'$100'` 会直接词法报错，要写成 `'\$100'` 或 `r'$100'`。

## 索引、切片与长度

```zgg
s := 'abcdef'
println(s[0], s[-1])        // a f
println(s[1:3])             // bc
println(s[:2], s[3:])       // ab def
println(len(s))             // 6
```

索引与切片按**字符（rune）**计算，中文不会被拆开：

```zgg
println('你好'[0], len('你好'))   // 你 2
```

## 拼接与重复

```zgg
println('ab' + 'cd')        // abcd
println('ab' + 12)          // ab12
println('ab' * 3)           // ababab
```

## 方法一览

| 方法 | 说明 | 示例 |
|---|---|---|
| `upper()` / `lower()` | 大小写 | `'aB'.upper()` → `AB` |
| `trim()` | 去首尾空白 | `'  x '.trim()` → `x` |
| `substr(begin, end?)` | 截取，负下标从尾部算 | `'hello'.substr(-3)` → `llo` |
| `split(sp, limit?)` | 按字面量分割 | `'a,b'.split(',')` → `[a, b]` |
| `splitr(sp?, limit?)` | 按正则分割（默认 `\s+`） | `'a  b'.splitr()` → `[a, b]` |
| `lines()` | 按换行拆分 | `'a\nb'.lines()` → `[a, b]` |
| `indexOf(sub)` | 子串首次位置，找不到 `-1` | `'abc'.indexOf('b')` → `1` |
| `lastIndexOf(sub)` | 子串最后位置 | `'aba'.lastIndexOf('a')` → `2` |
| `find(pattern, start?)` | 正则查找，返回匹配文本 | `'a1'.find('[0-9]')` → `1` |
| `replaceOne(sub, repl, beginAt?)` | 替换第一个 | `'aXa'.replaceOne('a', 'b')` → `bXa` |
| `replaceAll(sub, repl)` | 替换全部字面量 | `'aXa'.replaceAll('a', 'b')` → `bXb` |
| `replace(pattern, repl)` | 正则替换，`repl` 可为函数 | `'a1b22'.replace('[0-9]+', m => '<' + m[0] + '>')` |
| `startsWith(s...)` / `endsWith(s...)` / `contains(s...)` | 任一命中即 true | `'abc'.startsWith('x', 'a')` → `true` |
| `hash()` | 字符串哈希（int） | `'abc'.hash()` |
| `code(i?)` / `codes()` | 单字符码点 / 全部码点 | `'abc'.codes()` → `[97, 98, 99]` |
| `width()` | 终端显示宽度 | `'中文'.width()` → `4` |
| `isBlank()` / `notBlank()` | 是否全空白 / 非空白 | `''.isBlank()` → `true` |
| `decodeHex()` | 十六进制串转字节 | `'616263'.decodeHex()` |
| `decodeBase64()` | Base64 串转字节 | `'aGk='.decodeBase64()` |

示例：

```zgg
s := 'Hello, World'
println(s.upper(), s.lower())            // HELLO, WORLD hello, world
println(s.substr(0, 5), s.substr(-5))    // Hello World
println(s.indexOf('o'), s.lastIndexOf('o'))   // 4 8
println(s.find('[A-Z]+'))                // H
println(s.replaceAll('l', 'L'))          // HeLLo, WorLd
println('a1b22'.replace('[0-9]+', m => '<' + m[0] + '>'))  // a<1>b<22>
println('a, b, c'.split(', '))           // [a, b, c]
println('  x  '.trim())                  // x
println('abc'.startsWith('x', 'a'))      // true
println('中文'.width())                  // 4
```

## 输出与格式化

```zgg
println('a', 1, [1, 2])          // a 1 [1 2]
printf('name=%s age=%d pi=%.2f\n', 'zgg', 5, 3.14159)
println(sprintf('%05d|%x|%v', 42, 255, [1, 2]))   // 00042|ff|[1 2]
```

`printf` / `sprintf` 使用 Go 的格式化动词（`%s` `%d` `%f` `%v` `%q` 等），不是 `%Y` 这类时间格式。

## 字符串与字节

```zgg
b := bytes('abc')
println(b.hex())        // 616263
println(b.base64())     // YWJj
println(str(b))         // abc
```

继续阅读：[数组与对象](collections.md) →
