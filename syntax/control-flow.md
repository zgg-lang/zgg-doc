# 控制流

## if / else if / else

```zgg
score := 85

if score >= 90 {
    println('A')
} else if score >= 60 {
    println('B')
} else {
    println('C')
}
```

条件里可以带一个赋值（作用域仅限该 if 分支）：

```zgg
if v := 10; v > 5 {
    println('v = $v')      // v = 10
}
```

`if` 是**语句**，不能当作表达式使用；需要"取值"时用 [`when`](#when-表达式)。

## when 表达式

`when` 是表达式，适合替代 if-else 链和多分支取值。

### 形式一：条件分支

```zgg
x := 7
grade := when {
    x >= 90 -> 'A'
    x >= 60 -> 'B'
    else -> 'C'
}
println(grade)
```

### 形式二：值匹配

```zgg
println(when 5 {
    1, 2 -> 'small'
    3..6 -> 'middle'
    is Int -> 'any int'
    else -> 'other'
})
```

匹配规则：

| 条件 | 说明 |
|---|---|
| `1, 2` | 逗号分隔的候选值，任一相等即命中 |
| `3..6` / `3..<6` | 区间（含/不含右端） |
| `is Int` | 类型匹配 |

### 三元运算符

```zgg
println(1 > 0 ? 'yes' : 'no')
```

## switch 语句

```zgg
switch 5 {
    case 1, 2:
        println('low')
    case 3..6:
        println('middle')
    default:
        println('other')
}
```

- `case` 支持逗号列表与区间。
- `default` 可选。
- `switch` 是语句，不是表达式。

> `fallthrough` 的行为与 Go 不同：它只是"不再提前返回"，后续 `case` 仍要满足条件才会执行。除非你确认需要，否则建议不用。

## 循环

### 三段 for

```zgg
for i := 0; i < 3; i++ {
    println(i)
}
```

三段都不能省略（`for ; i < 3; i++` 会解析失败）。

### for-in

```zgg
for i in 5 { println(i) }          // 0 1 2 3 4
for i in 1..3 { println(i) }       // 1 2 3
for i in 1..<3 { println(i) }      // 1 2

for v in ['a', 'b'] { println(v) }
for i, v in ['a', 'b'] { println(i, v) }   // 0 a / 1 b

for ch in 'abc' { println(ch) }            // a b c
for v in {x: 1, y: 2} { println(v) }       // 值：1 2
for k, v in {x: 1, y: 2} { println(k, v) } // 键值对
```

带过滤条件：

```zgg
for i in 1..10 if i % 2 == 0 {
    println(i)
}
```

自定义可迭代对象实现 `__iter__`（返回一个带 `__next__` 的函数）即可被 `for-in` 遍历。

### while / do-while

```zgg
i := 0
while i < 3 {
    println(i)
    i++
}

j := 0
do {
    println(j)
    j++
} while j < 2
```

### break / continue 与标签

```zgg
outer: for i in 3 {
    for j in 3 {
        if j == 1 {
            continue outer
        }
        if i == 2 {
            break outer
        }
        println(i, j)
    }
}
```

## defer、blockDefer 与 use

### defer

`defer` 在**函数返回时**执行，后进先出；参数在注册时就求值：

```zgg
func demo() {
    a := 1
    defer println('defer a =', a)
    a = 2
    println('body a =', a)
}
demo()
```

输出：

```text
body a = 2
defer a = 1
```

### blockDefer

`blockDefer` 在**当前代码块结束**时执行，而不是函数结束：

```zgg
func demo() {
    {
        blockDefer println('block end')
        println('in block')
    }
    println('after block')
}
demo()
```

### defer 代码块

`defer { ... }` 把一段代码块延迟执行：

```zgg
func demo() {
    defer {
        println('cleanup')
    }
    println('work')
}
demo()
```

### use / use@

`use` 用于自动关闭资源：在离开当前块时调用对象的 `close` / `Close` 方法。

```zgg
o := {
    close() {
        println('closed')
    },
}
x := use o
println('using')
```

输出：

```text
using
closed
```

`use@method` 可以指定关闭方法：

```zgg
o := {
    shutdown() {
        println('shutdown')
    },
}
x := use@shutdown(o)
println('body')
```

`use@{ it => ... }` 自定义清理逻辑：

```zgg
o := {name: 'res'}
x := use@{ it => println('cleanup ' + it.name) } o
println('body')
```

> `use` / `use@` 必须出现在**表达式位置**（如 `x := use@close(o)`）；单独一行紧跟其它语句可能解析失败。

继续阅读：[函数与闭包](functions.md) →
