# 类与对象模型

ZGG 的类是基于原型的动态对象模型：类本身是 `Type` 值，实例是 `Object`。没有访问修饰符（`private`/`public`），也没有接口。

## 定义与实例化

```zgg
class Point {
    __init__(x, y) {
        this.x = x
        this.y = y
    }
    length() {
        return (this.x ** 2 + this.y ** 2) ** 0.5
    }
}

p := Point(3, 4)
println(p.length())        // 5
println(p.x, p.y)          // 3 4
```

- `__init__` 是构造方法，由 `Point(...)` 自动调用。
- 实例字段通过 `this.xxx = ...` 动态添加，不需要预先声明。
- 类定义会把类名绑定到当前作用域。

## 继承与 super

```zgg
class Animal {
    __init__(name) {
        this.name = name
    }
    speak() {
        return this.name + ' makes a sound'
    }
}

class Dog(Animal) {
    __init__(name, breed) {
        super.__init__(name)
        this.breed = breed
    }
    speak() {
        return super.speak() + ' woof'
    }
}

d := Dog('wang', 'corgi')
println(d.speak())     // wang makes a sound woof
println(d is Animal, d is Dog)   // true true
```

- 支持最多两个基类：`class C(A, B) {}`，方法查找按声明顺序。
- `super` 只能在方法内使用，`super.method(...)` 调用父类方法。

## 静态成员

用 `static` 声明，挂在类上而不是实例上：

```zgg
class Counter {
    static total: 0
    static create() {
        return Counter()
    }
    __init__() {
        Counter.total += 1
    }
}
Counter.create()
Counter.create()
println(Counter.total)     // 2
```

## 魔术方法

| 魔术方法 | 触发时机 |
|---|---|
| `__init__(...)` | 实例化 `Cls(...)` |
| `__str__()` | `str(obj)`、`println(obj)`、字符串拼接 |
| `__getAttr__(name)` | 访问不存在的成员 |
| `__getItem__(index)` | `obj[i]` |
| `__call__(...)` | 把对象当函数调用 `obj(...)` |
| `__iter__()` / `__next__()` | `for ... in obj` |
| `__contains__(v)` | `v in obj` |
| `__true__()` | 自定义真值（覆盖默认规则） |
| `__eq__(o)` / `__lt__(o)` / `__gt__(o)` / `__le__(o)` / `__ge__(o)` | 比较运算 |
| `__add__/__sub__/__mul__/__div__/__mod__/__pow__` | 算术重载 |
| `__r<op>__`（如 `__radd__`） | 右侧值的反向运算 |
| `__and__` / `__or__` | 位运算重载 |
| `__neg__()` | 一元负号 `-obj` |

示例：

```zgg
class Money {
    __init__(amount) {
        this.amount = amount
    }
    __add__(other) {
        return Money(this.amount + other.amount)
    }
    __eq__(other) {
        return this.amount == other.amount
    }
    __str__() {
        return '¥' + str(this.amount)
    }
}

println(Money(3) + Money(5))     // ¥8
println(Money(3) == Money(3))    // true
```

自定义真值：

```zgg
class Empty {
    __true__() {
        return false
    }
}
println(when Empty() { true -> 'truthy' else -> 'falsy' })   // falsy
```

## 访问缺失成员：`__getAttr__`

```zgg
class Config {
    __getAttr__(name) {
        return 'default-' + name
    }
}
c := Config()
println(c.timeout)      // default-timeout
```

## 方法是一等值

取出的方法会绑定到实例，可以传递和调用：

```zgg
class Adder {
    __init__(base) {
        this.base = base
    }
    add(x) {
        return this.base + x
    }
}
add10 := Adder(10).add
println(add10(5))       // 15
```

## extend：给已有类型加方法

`extend` 可以为任意类型（包括内置类型）添加方法：

```zgg
extend Str {
    shout() {
        return this.upper() + '!'
    }
}
println('hi'.shout())   // HI!
```

也可以扩展用户类：

```zgg
class N {
    __init__(v) { this.v = v }
}
extend N {
    double() {
        return N(this.v * 2)
    }
}
println(N(3).double().v)   // 6
```

> `extend` 的作用域是**声明它的代码块**：在函数内 `extend` 的方法离开函数后失效。需要全局生效时，请在模块顶层声明。

## 类型判断

```zgg
class A {}
class B(A) {}
b := B()
println(b is B, b is A, type(b).__name__)   // true true B
```

## 没有的东西

- 没有 `private` / `protected`，约定用 `_name` 表示内部字段。
- 没有构造函数重载；用可变参数或参数判断实现。
- 没有抽象类 / 接口；用"约定方法名 + `__getAttr__`"替代。

继续阅读：[错误处理](errors.md) →
