# regex 正则表达式

ZGG 提供两个正则模块，行为一致，只有**匹配结果形态**不同：

| 模块 | 匹配结果 |
|---|---|
| `@regex` | 数组：`[text, begin, end]` |
| `@regex2` | 对象：`{text, begin, end}` |

`begin` / `end` 是**字符下标**（不是字节）。

## 顶层函数

```zgg
re := @regex

println(re.find(r'\d+', 'a1b22'))        // [1, 1, 2]
println(re.findAll(r'\d+', 'a1b22'))     // [[[1, 1, 2]], [[22, 3, 5]]]
println(re.split(r',', 'a,b,c'))         // [a, b, c]
println(re.replaceAll(r'\d+', 'a1b22', '#'))   // a#b#
```

| 函数 | 说明 |
|---|---|
| `find(pattern, text[, offset])` | 第一个匹配的分组数组 |
| `findAll(pattern, text)` | 所有匹配；每个匹配是一个分组数组 |
| `split(pattern, text)` | 按正则分割 |
| `replaceAll(pattern, src, repl)` | 替换全部；`repl` 可为字符串或函数 |

`find` 的返回值是**分组数组**：第 0 项是整体匹配，后续是捕获组。

```zgg
m := @regex.find(r'(\w+)@(\w+)', 'mail: a@b')
println(m)          // [[a@b, 6, 9], [a, 6, 7], [b, 8, 9]]
println(m[0][0])    // a@b
println(m[1][0])    // a
```

`regex2` 用对象更好读：

```zgg
m := @regex2.find(r'(\w+)@(\w+)', 'mail: a@b')
println(m[1].text, m[1].begin, m[1].end)   // a 6 7
```

## 替换回调

```zgg
println(@regex.replaceAll(r'\d+', 'a1b22', m => '[' + m[0] + ']'))
// a[1]b[22]
```

回调参数是分组数组，`m[0]` 是匹配文本。

## 编译复用：Regexp 对象

```zgg
re := @regex.Regexp(r'\d+')
println(re.find('x9y'))          // [[9, 1, 2]]
println(re.findAll('x9y8'))      // [[[9, 1, 2]], [[8, 3, 4]]]
println(re.split('a1b2c'))       // [a, b, c]
println(re.replaceAll('a1b22', '#'))   // a#b#
```

方法：`find(text[, offset])`、`findAll(text)`、`split(text[, n])`、`replaceAll(src, repl)`。

## 注意事项

- 正则字面量请用 `r'...'`（原始字符串），避免 `\d` 被当成转义序列。
- `findAll` 的结果比想象中多一层：外层是"所有匹配"，内层是"每个匹配的所有分组"。
- 非法正则会抛出 `compile regexp ... error`。

## 与字符串方法的区别

`str.find` 也接受正则，但只返回匹配文本（不是分组）：

```zgg
println('a1b22'.find(r'\d+'))    // 1
```
