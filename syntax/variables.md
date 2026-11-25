# 变量与作用域

## 声明：`:=`

变量第一次出现必须用 `:=` 声明，不能只写 `=`：

```zgg
name := 'ZGG'
count := 0
items := []
```

再次赋值用 `=`：

```zgg
count := 0
count = count + 1
println(count)
```

对未声明的变量赋值会报错：

```text
Exception! variable y not exists
```

对同一作用域重复声明会报错：

```text
Exception! variable x redefined
```

## 复合赋值与自增

```zgg
n := 10
n += 5      // 15
n -= 3      // 12
n *= 2      // 24
n /= 5      // 4（整数除法）
n %= 3      // 1
n <<= 2     // 4
n |= 1      // 5
n++         // 6
n--         // 5
println(n)
```

对象字段与数组下标同样支持：

```zgg
user := {age: 20}
user.age += 1
user['age'] *= 2
arr := [1, 2, 3]
arr[1] += 10
println(user.age, arr)     // 42 [1, 12, 3]
```

## 解构声明（数组）

```zgg
[a, b] := [1, 2]
println(a, b)              // 1 2

pairs := [[1, 'a'], [2, 'b']]
for p in pairs {
    println(p[0], p[1])
}
```

> 对象解构（`{a, b} := obj`）在当前语法中不可用；请用 `obj.a` / `obj['a']` 取值。

## 作用域

变量是**块级作用域**，从声明处开始、到所在 `{}` 结束：

```zgg
x := 1
{
    x := 2          // 新的局部变量，遮蔽外层
    println(x)      // 2
}
println(x)          // 1
```

函数内部可以读取外层变量（闭包），修改会作用于同一个变量：

```zgg
func counter() {
    n := 0
    return () => {
        n += 1
        return n
    }
}
c := counter()
println(c(), c(), c())     // 1 2 3
```

## 特殊变量

| 名称 | 说明 |
|---|---|
| `_` | 丢弃占位：`[_, b] := [1, 2]` 只取第二个；`_` 本身读到 `undefined` |
| `this` | 方法内的当前对象（由调用方绑定） |
| `super` | 子类方法内指向父类（用于 `super.method()`） |
| `arguments` | 函数内当前调用的参数数组 |
| `it` | 以 `{ ... }` 形式作为回调参数时的默认入参 |
| `isMain` | 是否作为主脚本运行（被 import 时为 `false`） |
| `__file__` / `__dir__` / `__line__` | 当前文件名 / 目录 / 行号 |

```zgg
println(__file__, __line__)
func f() {
    println(arguments)
}
f(1, 2, 3)
```

## 模块级变量

模块顶层声明的变量是**模块私有**的；只有 `export` 出去的才会被 `import` 方看到：

```zgg
// lib.zgg
version := '1.0'
export version
```

```zgg
@file.rewrite('./lib.zgg', 'version := \'1.0\'\nexport version')
v := import('./lib.zgg')
println(v)          // {version: 1.0}
```

继续阅读：[类型系统](types.md) →
