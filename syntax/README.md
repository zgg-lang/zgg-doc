# 语法总览与词法

## 源文件与注释

```zgg
// 单行注释
# 也可以这样注释
/* 多行注释
   可以跨行 */
println('ok')
```

- 源文件按 UTF-8 处理。
- 第一行如果是 `#!` 开头的 shebang，会被忽略。
- 语句之间用**换行或分号**分隔；换行不是语法的一部分（空白统一被跳过），所以一行写多条语句需要分号。

## 标识符

标识符可以用字母、`_`、`$` 开头，后续可接数字；**支持中文**：

```zgg
名字 := '张三'
println(名字)
```

`_` 是丢弃占位符：赋值给 `_` 不保留值，读取 `_` 得到 `undefined`。

## 关键字

| 类别 | 关键字 |
|---|---|
| 字面量 | `true` `false` `nil` `undefined` |
| 声明/定义 | `func` `class` `static` `export` `extend` |
| 控制流 | `if` `else` `when` `switch` `case` `default` `fallthrough` `for` `in` `while` `do` `break` `continue` `return` |
| 异常 | `try` `catch` `finally` `assert` |
| 资源 | `defer` `blockDefer` `use` `use@` |
| 导入 | `import`（函数） |
| 类型判断 | `is` |
| 保留未启用 | `throw` |

> `throw` 是词法层的保留字，但当前语法没有对应语句；抛错请使用 `assert` 或运行时错误，详见[错误处理](errors.md)。

## 字面量

```zgg
println(42, 0x2A, 0b101010, 052)   // 42 42 42 42
println(1.5, 1.5e3)                 // 1.5 1500
println(123456789012345678901234567890L)  // 大数（后缀 L）
println('text', r'raw\n', '''raw $x''')
println(true, false, nil, undefined)
println([1, 2, 3], {a: 1})
```

| 字面量 | 说明 |
|---|---|
| `42` `0x2A` `0b1010` `052` | 十进制 / 十六进制 / 二进制 / 八进制（`0` 前缀） |
| `1.5` `1.5e3` | 浮点 / 科学计数 |
| `123L` | `BigNum`（任意精度） |
| `'text'` | 字符串（单引号，支持插值） |
| `r'text'` | 原始字符串（不转义、不插值） |
| `'''text'''` | 原始多行字符串 |
| `true` `false` `nil` `undefined` | 布尔与两种空值 |

## 代码块与语句

```zgg
func demo(x) {
    if x > 0 {
        println('positive')
    }
    {                       // 单独的代码块：引入新的作用域
        inner := x * 2
        println(inner)
    }
}
demo(3)
```

块级作用域内的变量在离开 `{}` 后不可见；块内的变量不会泄漏到外层。

## 表达式语句的限制

不是所有表达式都能单独成句。**可以作为语句的表达式**：

- 函数调用
- 赋值 / 复合赋值 / 自增自减
- 代码块
- 其余语句（`if` / `for` / `while` / `try` / `class` / `func` 定义等）

```zgg
println('ok')     // 函数调用：可以
x := 1            // 赋值：可以
1 + 2             // 单独一行没有意义，会解析报错
```

## 大小写与命名

- 关键字、`true/false/nil/undefined` 均为小写。
- 内置函数与库方法区分大小写：`println`、`@file.readString`、`@http.getJson`。
- 类名、常量没有强制约定，社区风格是类名首字母大写、变量小写。

继续阅读：[变量与作用域](variables.md) →
