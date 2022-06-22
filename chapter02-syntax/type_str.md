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