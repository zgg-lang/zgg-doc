# ZGG的字符串

ZGG语言提供了强大的字符串功能。

## 数组的声明与访问

```
'asdfadsfdsa'
```

## 字符串的运算

### 加法
### 乘法

## 字符串的内置方法

为了提高工作效率，ZGG内置了大量实用的字符串方法

| 方法名       |       作用 |
|-------------|------|
| [substr](#substr      )      | 截取子串 |
| [upper](#upper       )       | 转大写 |
| [lower](#lower       )       | 转小写 |
| [find](#find        )        | 查找第一个符合正则的子串 |
| [hash](#hash        )        | 返回一个字符串的哈希值，Int |
| [split](#split       )       | 用指定分隔符分割字符串 |
| [splitr](#splitr      )      | 用指定正则模式分割字符串 |
| [lines](#lines       )       | 把多行字符串分割成一个数组，每行一个元素。即.split('\n') |
| [indexOf](#indexOf     )     | 找到子串在字符串中第一次出现的位置 |
| [lastIndexOf](#lastIndexOf ) | 找到子串在字符串中最后一次出现的位置 |
| [replaceOne](#replaceOne  )  | 替换第一个匹配到的子串 |
| [replaceAll](#replaceAll  )  | 替换所有匹配的子串 |
| [replace](#replace     )     | 替换所有正则匹配到的子串 |
| [trim](#trim        )        | 去掉字符串前后的空格 |
| [startsWith](#startsWith  )  | 判断字符串是否有指定前缀 |
| [endsWith](#endsWith    )    | 判断字符串是否有指定后缀 |
| [contains](#contains    )    | 判断字符串是否包含指定子串 |
| [decodeHex](#decodeHex   )   | 将十六进制串解析为Bytes |
| [decodeBase64](#decodeBase64)| 将Base64编码字符串解析为Bytes |
| [fillParams](#fillParams  )  | 模板填充值 |

## 函数详解

### Str.substr(start, end?)

生成一个子串。具体用法请看下方例子

#### Examples:
```
zgg> 'zgg lang'.substr(1) // 只有一个参数时
gg lang
zgg> 'zgg lang'.substr(-4) // start可以为负数，表示“倒数第几个字符”
lang
zgg> 'zgg lang'.substr(1, 3) // 两个参数时
gg
zgg> 'zgg lang'.substr(1, -1) // end也可以未负数
gg lan
zgg> 'zgg lang'.substr(-4, -1) // start与end都可以为负数
lan
zgg> 'zgg lang'.substr(0, -1)
zgg lan
```

### Str.upper()

字符串转大写

### Str.lower()

字符串转小写

### Str.find(regexp)

#### Examples:

查找第一个符合正则的子串，找不到返回空字符串。更多正则相关功能，请看regex和regex2标准库

```
zgg> 'sdfsaf1231sdf'.find(r'\d+')
1231
```

#### Str.hash()

返回字符串的哈希值，使用bkdr算法

### Str.split(sp, limit?)

用指定分隔符分割字符串

### Str.splitr(spRegexp, limit?)

指定正则模式分割字符串

### Str.lines()

用指定换行符"\n"分割字符串，相当于xxx.split('\n')

### Str.indexOf(sub, start?)

从第start个字符开始，查找子串sub第一次出现的位置。start缺省值为0。找不到时返回-1

#### Examples:
```
zgg> 'abcabcabc'.indexOf('a')
0
zgg> 'abcabcabc'.indexOf('a', 1)
3
```

### Str.lastIndexOf(sub)

返回sub在字符串最后出现时的位置，找不到返回-1

### Str.replaceOne(sub, repl)

替换换第一个匹配到的子串。不修改原字符串，返回新的字符串

#### Examples:
```
zgg> 'zgg:welcome to zgg lang'.replaceOne('zgg', 'ZGG')
ZGG:welcome to zgg lang
```

### Str.replaceAll(sub, repl)

替换所有匹配的子串。不修改原字符串，返回新的字符串

#### Examples:
```
zgg> 'zgg:welcome to zgg lang'.replaceAll('zgg', 'ZGG')
ZGG:welcome to ZGG lang
```

### Str.replace(regexp, repl)

强大的字符串替换方法，替换所有正则匹配到的子串。

* 当repl为字符串时，所有匹配到的子串都直接替换为repl。此时，支持正则捕获组
* 当repl为函数或其他可执行对象时，所有匹配到的子串都会作为唯一参数传入该函数执行，然后替换为函数返回值

#### Examples:
```
// 一般字符串替换
zgg> 'ID:100 Number:1024'.replace(r'\d+', '***') 
ID:*** Number:***

// 带捕获组的字符串替换
zgg> 'ID:100 Number:1024'.replace(r'(\d)(\d*)', r'$2$1') 
ID:001 Number:0241

// 函数替换
zgg> 'ID:100 Number:1024'.replace(r'\d+', v => int(v)+1) 
ID:101 Number:1025
```

### Str.trim()

去掉字符串前后的空格

### Str.startsWith(prefix)

判断字符串是否有指定前缀prefix

### Str.endsWith(suffix)

判断字符串是否有指定后缀suffix

### Str.contains(sub)

判断字符串是否包含指定子串

### Str.decodeHex()

将十六进制字符串，转为Bytes。如果字符串不是一个合法的十六进制字符串则抛出异常

#### Examples:
```
zgg> '303132'.decodeHex()
012
zgg> '303132!'.decodeHex()
Exception! str.decodeHex decode failed: encoding/hex: invalid byte: U+0021 '!'
:0 (str.decodeHex)
:0 (<root>)
```

### Str.decodeBase64()

将Base64编码字符串解析为Bytes。如果字符串不是一个合法的Base64字符串则抛出异常