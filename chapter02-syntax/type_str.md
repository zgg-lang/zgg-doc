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
| substr      | 截取子串 |
| upper       | 转大写 |
| lower       | 转小写 |
| find        | 查找第一个符合正则的子串 |
| hash        | 返回一个字符串的哈希值，Int |
| split       | 用指定分隔符分割字符串 |
| splitr      | 用指定正则模式分割字符串 |
| lines       | 把多行字符串分割成一个数组，每行一个元素。即.split('\n') |
| indexOf     | 找到子串在字符串中第一次出现的位置 |
| lastIndexOf | 找到子串在字符串中最后一次出现的位置 |
| replaceOne  | 替换第一个匹配到的子串 |
| replaceAll  | 替换所有匹配的子串 |
| replace     | 替换所有正则匹配到的子串 |
| trim        | 去掉字符串前后的空格 |
| startsWith  | 判断字符串是否有指定前缀 |
| endsWith    | 判断字符串是否有指定后缀 |
| contains    | 判断字符串是否包含指定子串 |
| decodeHex   | 将十六进制串解析为Bytes |
| decodeBase64| 将Base64编码字符串解析为Bytes |
| fillParams  | 模板填充值 |

