# 函数与闭包

## 定义函数

### 命名函数

```zgg
func add(a, b) {
    return a + b
}
println(add(1, 2))
```

`func` 定义等价于把函数值赋给同名变量；函数体是一个独立作用域。

### 匿名函数

```zgg
f := func(x) {
    return x * 2
}
println(f(3))
```

### 箭头函数

```zgg
double := x => x * 2                       // 单表达式
sub := (a, b) => a - b                     // 多参数
calc := (a, b) => {                        // 代码块
    return a * b
}
println(double(3), sub(5, 2), calc(2, 3))
```

单个参数时可以省略括号：`x => x + 1`。

### 作为参数的回调

```zgg
println([1, 2, 3].map(v => v * 2))

// 代码块写法：默认入参名为 it
println([1, 2, 3].map({ it * 10 }))

// 隐式 it 的字段访问
println(['a', 'b'].map({ .upper() }))
```

## 调用

### 位置参数与具名参数

```zgg
func range2(begin, end, step) {
    return [begin, end, step]
}
println(range2(1, 10, 2))
println(range2(end: 10, begin: 1, step: 2))   // 顺序无关
```

### 可变参数

最后一个参数前加 `...`：

```zgg
func sum(first, ...rest) {
    total := first
    for v in rest {
        total += v
    }
    return total
}
println(sum(1, 2, 3, 4))     // 10
```

### 参数展开

调用时用 `...数组` 展开：

```zgg
func add(a, b) { return a + b }
args := [1, 2]
println(add(...args))        // 3
```

### 占位符与偏应用

`%` 表示"留一个洞"，调用后得到新函数：

```zgg
func add(a, b) { return a + b }
inc := add(%, 1)
println(inc(10))             // 11
```

等价的 `bind` 写法：

```zgg
func add(a, b) { return a + b }
inc := bind(add, 1)
println(inc(10))             // 11
```

## 返回值

- `return expr` 返回值。
- `return` 无值返回 `undefined`。
- 没有 `return` 的函数也返回 `undefined`。

```zgg
func f() { return }
println(typeName(f()))     // <type Undefined>
```

## 闭包

函数会捕获定义处的作用域，并且捕获的是**变量本身**：

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

### 循环变量的闭包陷阱

`for` 的循环变量由整个循环共享，闭包捕获的是同一个变量：

```zgg
func makeAdders() {
    result := []
    for i in 1..3 {
        result.push(x => x + i)
    }
    return result
}
println(makeAdders().map(f => f(10)))   // [13, 13, 13]
```

需要在每轮捕获独立值时，在循环体内先复制一份：

```zgg
func makeAdders() {
    result := []
    for i in 1..3 {
        cur := i                 // 每轮新建一个变量
        result.push(x => x + cur)
    }
    return result
}
println(makeAdders().map(f => f(10)))   // [11, 12, 13]
```

## arguments

函数内可用 `arguments` 拿到本次调用的全部实参：

```zgg
func show() {
    println(arguments)
}
show(1, 2, 3)      // [1, 2, 3]
```

## 函数是一等值

```zgg
func apply(f, x) {
    return f(x)
}
println(apply(x => x * x, 6))     // 36

ops := {
    inc: x => x + 1,
    dec: x => x - 1,
}
println(ops.inc(1), ops.dec(1))   // 2 0
```

## 递归

```zgg
func fib(n) {
    if n < 2 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}
println(fib(10))     // 55
```

## 没有默认参数

ZGG 不支持参数默认值，用 `??` 在函数体内兜底：

```zgg
func greet(name) {
    name = name ?? 'world'
    return 'hello, ' + name
}
println(greet(), greet('zgg'))
```

继续阅读：[类与对象模型](classes.md) →
