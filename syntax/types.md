# 类型系统

## 类型一览

| 类型 | 字面量 / 构造 | 说明 |
|---|---|---|
| `Bool` | `true` `false` | 布尔 |
| `Int` | `42` `0xFF` `0b1010` `052` | 64 位有符号整数 |
| `Float` | `1.5` `1.5e3` | 64 位浮点 |
| `BigNum` | `123456789012345678901234567890L` | 任意精度数（后缀 `L`） |
| `Str` | `'text'` `r'raw'` `'''raw'''` | UTF-8 字符串 |
| `Bytes` | `bytes('abc')`、读文件 | 字节数组 |
| `Nil` | `nil` | 显式空值 |
| `Undefined` | `undefined` | "未定义"，多用于缺失字段/变量 |
| `Array` | `[1, 2, 3]` | 动态数组 |
| `Object` | `{a: 1}` | 键值对象（也是类的实例） |
| `Func` | `func(){}`、`x => x` | 函数 / 闭包 |
| `Type` | `class A {}`、`Int` | 类型本身 |
| `GoValue` / `GoType` | `@go` 桥接 | 包装的 Go 值与反射类型 |

## 空值：`nil` 与 `undefined`

ZGG 有两个"空"：

- `nil`：你显式赋的空值（类似其它语言的 `null`）。
- `undefined`：不存在的变量、缺失的字段、无返回值的表达式结果。

```zgg
println(nil == undefined)     // false
println(nil, undefined)       // nil undefined
println(str(nil), str(undefined))   // nil undefined

o := {a: 1}
println(o.b)                  // undefined
println(o.b ?? 'default')     // default
```

规则：

| 表达式 | 结果 |
|---|---|
| `nil == undefined` | `false` |
| 两者作为条件 | 均为假 |
| `x ?? y` | 当 `x` 是 `nil` 或 `undefined` 时取 `y` |
| `str(nil)` / `str(undefined)` | `'nil'` / `'undefined'` |

## 真值规则

| 值 | 真假 |
|---|---|
| `false`、`0`、`0.0`、`''`、`[]`、`{}`、`nil`、`undefined` | 假 |
| 其余（非零数、非空字符串/数组/对象、函数、类型） | 真 |

```zgg
println(when 0 { true -> 'truthy' else -> 'falsy' })     // falsy
println(when [] { true -> 'truthy' else -> 'falsy' })    // falsy
println(when {} { true -> 'truthy' else -> 'falsy' })    // falsy
println(when 'x' { true -> 'truthy' else -> 'falsy' })   // truthy
```

> 注意：空对象/空数组为假，这一点和 JavaScript/Python 都不同，写 `if obj { ... }` 时要小心。

## 类型判断与获取

### `is`

```zgg
println(1 is Int)          // true
println(1 is Float)        // false
println('x' is Str)        // true
println([1] is Array)      // true
println({a: 1} is Object)  // true
println(nil is Nil)        // true
println(undefined is Undefined)  // true
```

`is` 也支持用户类，并会沿继承链判断：

```zgg
class Animal {}
class Dog(Animal) {}
println(Dog() is Animal)   // true
println(Dog() is Dog)      // true
```

### `type` / `typeName`

```zgg
println(type(1).__name__)  // Int
println(type(1) == Int)    // true
println(typeName(1))       // <type Int>
```

> `typeName(v)` 返回的是类型的展示字符串（`<type Int>`），需要纯名字时用 `type(v).__name__`，判断类型用 `v is T`。

## 数值

### 整数

- 64 位有符号：`-9223372036854775808` ~ `9223372036854775807`。
- **溢出会回绕**，不报错：

```zgg
println(9223372036854775807 + 1)   // -9223372036854775808
```

- 除法向零取整，取模符号随被除数（与 Go 一致）：

```zgg
println(7 / 2, -7 / 2)     // 3 -3
println(7 % 3, -7 % 3)     // 1 -1
```

- 除以 0 抛异常：`Exception! division by zero`。

### 浮点

```zgg
println(1 / 2)       // 0（整数相除）
println(1.0 / 2)     // 0.5
println(2 ** -1)     // 0.5
println(0.1 + 0.2)   // 0.30000000000000004
```

### 大数（BigNum）

加 `L` 后缀，按任意精度计算，与 `Int`/`Float` 混合时自动提升：

```zgg
big := 123456789012345678901234567890L
println(big + 1)          // 123456789012345678901234567891
println(big * 2)          // 24691357802469135780（仍是 BigNum）
println(typeName(big))    // <type BigNum>
```

### 数制与转换

```zgg
println(0x2A, 0b101010, 052)     // 42 42 42
println(int('42'), int('0x10'), int('10', 2), int('ff', 16))
println(int(1.9), int(true))     // 1 1
println(float('1.5'))            // 1.5
println(str(255, 16), str(3.14)) // ff 3.14
```

## 字符串与字节

```zgg
s := '你好'
println(len(s))              // 2（按字符计）
println(s[0])                // 你

b := bytes('abc')
println(b.hex(), b.len())    // 616263 3
println(str(b))              // abc
```

## 结构相等

`==` 对数组/对象做**结构化比较**，对数值做跨类型比较：

```zgg
println(1 == 1.0)              // true
println(1 == true)             // false（不做布尔转换）
println('1' == 1)              // false
println([1, 2] == [1, 2])      // true
println({a: 1} == {a: 1})      // true
```

用户类可以通过魔术方法自定义相等与比较，见[类与对象模型](classes.md)。

## Go 值

从 Go 侧注入或由标准库返回的值是 `GoValue`，可以：

```zgg
tls := import('gostd/crypto/tls')
println(typeName(tls))          // <type Object>（模块是对象）
```

- 调用 Go 方法：`obj.Method(args)`。
- 取 Go 结构体字段：`structField`（导出字段）。
- 转成 ZGG 原生值：用 `@go.convert` 或标准库封装（如 `time.fromGoTime`）。

继续阅读：[运算符与表达式](operators.md) →
