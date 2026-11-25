# 运算符与表达式

## 算术运算

```zgg
println(1 + 2, 5 - 3, 2 * 3, 7 / 2, 7 % 3, 2 ** 10)
// 3 2 6 3 1 1024
```

运算符对不同类型的重载：

| 表达式 | 结果 |
|---|---|
| `'ab' + 'cd'` | `'abcd'` |
| `'ab' + 1` / `1 + 'ab'` | 任一侧是字符串时做拼接：`'ab1'` / `'1ab'` |
| `'ab' * 3` | `'ababab'` |
| `[1] + [2]` | `[1, 2]` |
| `[1, 2] * 2` | `[1, 2, 1, 2]` |
| `1 + 1.5` | `2.5`（Int → Float） |
| `大数L + 1` | 自动提升为 `BigNum` |

整数相除会截断，除零抛异常：

```zgg
println(7 / 2, -7 / 2)     // 3 -3
println(7 % 3, -7 % 3)     // 1 -1
try {
    println(1 / 0)
} catch (e) {
    println(e.message)     // division by zero
}
```

`**` 右结合：`2 ** 3 ** 2` = `512`。

## 比较运算

```zgg
println(1 == 1.0)        // true（跨数值类型）
println(1 != 2)          // true
println(1 < 2, 2 <= 2, 3 > 2, 3 >= 4)
println([1, 2] == [1, 2])    // true（结构相等）
println({a: 1} == {a: 1})    // true
```

> **不支持链式比较**：`1 < 2 < 3` 会先算 `1 < 2` 得到 `true`，再算 `true < 3`，结果是 `false`。请写 `1 < 2 && 2 < 3`。

`is` 与 `in` 也是比较类运算符：

```zgg
println(1 is Int, 'x' is Str)          // true true
println(2 in [1, 2, 3], 3 in 1..5)     // true true
println('b' in 'abc')                  // true
```

## 逻辑运算

`&&` / `||` **返回操作数**（短路求值），不是布尔值：

```zgg
println(1 && 2)            // 2
println(0 || 'x')          // x
println(nil || 'default')  // default
println(!0, !'')           // true true
```

条件判断按[真值规则](types.md#真值规则)：`false` / `0` / `''` / `[]` / `{}` / `nil` / `undefined` 为假。

## 位运算

只对整数生效：

```zgg
println(1 & 3)      // 1
println(1 | 2)      // 3
println(5 ^ 1)      // 4
println(~0)         // -1
println(1 << 3)     // 8
println(-8 >> 1)    // -4
```

## 区间

`..`（含右端）与 `..<`（不含右端）不是独立值，只能用在 `for` / `in` / `when` 中：

```zgg
for i in 1..3 { println(i) }    // 1 2 3
for i in 1..<3 { println(i) }   // 1 2
println(3 in 1..5)              // true
```

## 三元与空值合并

```zgg
println(1 > 0 ? 'yes' : 'no')     // yes
println(nil ?? 'default')         // default
println(undefined ?? 0)           // 0
println(0 ?? 5)                   // 0（只有 nil/undefined 会触发）
println(nil ?? 1 ?? 2)            // 1
```

`??` 也可以跟在**调用语句**后面做异常兜底（不产生值）：

```zgg
@file.readBytes('/tmp/not-exists') ?? {
    println('读取失败，已降级')
}
```

## 可选调用 `?.`

`?.` 只能用在"函数与参数表之间"，被调用者为空时返回 `undefined`：

```zgg
f := nil
println(f?.(1))       // undefined

o := {}
println(o.foo?.(1))   // undefined
```

注意：`x?.field`（可选取字段）**不支持**。

## 错误解包 `!`

Go 风格函数可能返回 `(value, error)`；`expr!` 会在 `error` 非空时抛出异常，否则返回 `value`：

```zgg
@file.rewrite('/tmp/data.bin', 'abc')
bs := @file.readBytes('/tmp/data.bin')!    // 失败会抛 Exception
println(bs.len())
```

数组值按 Go 的 `(value..., error)` 约定处理：`!` 检查**最后一个元素**，是 `error` 就抛出，否则丢掉最后一个元素，返回剩余部分（0 个为 `undefined`、1 个为该值、多个为数组）。

```zgg
println([1, 2]!)        // 1
println([1, 2, 3]!)     // [1, 2]
```

## 参数占位符 `%`

调用时用 `%` 占位，得到一个新的可调用对象（偏应用）：

```zgg
func add(a, b) { return a + b }
inc := add(%, 1)
println(inc(10))     // 11
```

## 赋值运算符

`=`、`:=`、`+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`，以及 `++` / `--`。详见[变量](variables.md)。

## 运算符优先级

从高到低（同一行内左结合，`**` 右结合）：

| 优先级 | 运算符 |
|---|---|
| 1 | `.` `[]` `()` `?.(...)` |
| 2 | 一元 `-` `!` `~` `++` `--` |
| 3 | `**` |
| 4 | `*` `/` `%` |
| 5 | `+` `-` |
| 6 | `<<` `>>` |
| 7 | `&` |
| 8 | `\|` |
| 9 | `^` |
| 10 | `==` `!=` `<` `<=` `>` `>=` `is` `in` |
| 11 | `&&` |
| 12 | `\|\|` |
| 13 | `? :`、`when` |
| 14 | `??` |
| 15 | 赋值类 |

> 位运算、比较、逻辑混用时优先级和多数语言不同（例如**位运算高于比较**，`2 & 3 == 3` 等价于 `(2 & 3) == 3`）。不确定就加括号。

继续阅读：[字符串](strings.md) →
