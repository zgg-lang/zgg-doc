# 概述与设计定位

## 一句话定位

ZGG 是一门**运行在 Go 之上的动态脚本语言**：写起来像 Python / JavaScript，能力边界却接近 Go —— 可以直接 import 整个 Go 标准库、调用 Go 结构体方法、把 Go 的 `error` 用 `!` 解包。

它适合"需要快速写、又要能碰系统"的场景：内部工具、数据清洗、HTTP 服务、定时任务、运维脚本。

## 设计取向

从语法和标准库可以看出四条明确的取舍：

1. **可读性优先**
   变量必须先用 `:=` 声明；`if` / `for` 等语句强制使用代码块；赋值与声明用不同符号（`=` / `:=`）。这些规则牺牲了一点灵活性，换来"看代码就知道作用域"。

2. **动态类型 + 强运行时检查**
   没有类型标注，但类型错误会在运行时立即报错，且不会做隐式数字/布尔转换（`1 == true` 为 `false`）。数值之间会自动提升：`Int` → `Float` → `BigNum`。

3. **Go 能力直通**
   `import('gostd/fmt')` 拿到的是真实 Go 包；`@http`、`@db`、`@xlsx` 等标准库是用 Go 写的原生模块；Go 值、结构体、`io.Reader` 都能在脚本里直接使用。

4. **脚本化的工程能力**
   模块缓存与热重载、`defer` / `use` 资源释放、`try/catch/finally`、goroutine 风格并发、终端表格、命令行参数解析 —— 都是为"写完就能用"服务的。

## 语言速览

```zgg
// 变量与插值
name := 'ZGG'
println('hello, $name')

// 数组、推导式、函数式
nums := [1, 2, 3, 4, 5]
evens := [x for x in nums if x % 2 == 0]
println(evens.map(v => v * v))        // [4, 16]

// when 表达式
func grade(score) {
    return when score {
        90..100 -> 'A'
        60..<90 -> 'B'
        else -> 'C'
    }
}

// 类与运算符重载
class Vec {
    __init__(x, y) { this.x = x
 this.y = y }
    __add__(o) { return Vec(this.x + o.x, this.y + o.y) }
    __str__() { return 'Vec(${this.x}, ${this.y})' }
}
println(Vec(1, 2) + Vec(3, 4))        // Vec(4, 6)
```

## 能力地图

| 领域 | 你可以用到的能力 |
|---|---|
| 语法 | 字符串插值、`when`、切片、推导式、解构、隐式 `it`、`bind` 占位符、标签跳转 |
| 面向对象 | 单/双继承、`super`、`static`、`__getAttr__`、`__getItem__`、`__call__`、`__str__`、`__eq__`、`__add__` 等 |
| 函数 | 一等函数、闭包、可变参数、具名参数、参数展开、偏应用 |
| 错误 | `try/catch/finally`、`assert`、`x!` 解包 Go error、`??` 默认值、`?? {}` 兜底 |
| 模块 | `export`、`import`、`@mod` 短导入、文本/JSON/CSV 导入、mtime 热重载、`ZGGPATH` |
| 并发 | future（`concurrent.start`）、`concurrent.all` / `map`、`Chan`、`Mutex`、`Limiter` |
| Go 互操作 | `gostd/*` 全量标准库、Go 值/结构体/`io.Reader`、`.so` 插件 |
| 标准库 | json / yaml / file / time / regex / http / db / xlsx / ptable / sys / sh / flag / template / url / base64 / hash / compress / binary / tcp / udp / kv / redis / nsq / ip2region / cron / fsnotify / psutil / drawing / etree / dom / graph / msgpack / go |

## 执行模型

```text
源码 ──ANTLR 词法/语法──▶ AST ──树遍历求值──▶ 结果
                              │
                              ├─ 模块缓存（按 mtime 热重载）
                              ├─ Go 值桥接（reflect）
                              └─ 异常：panic/recover → RuntimeError
```

没有中间字节码，也没有 JIT；每次执行都是 AST 解释。这决定了它**启动快（约 20ms）、长于胶水逻辑、不适合 CPU 密集型计算**（性能数据见[附录](../appendix/internals.md)）。

## 与其它语言的关系

- **像 Python 的地方**：`for x in`、缩进式思维（但用大括号）、`try/except` 风格的错误处理、`str/int/len` 等内置函数。
- **像 JavaScript 的地方**：对象字面量、闭包、`?.`、`&&/||` 返回操作数、`undefined`。
- **像 Ruby 的地方**：`extend` 开放类、魔术方法、运算符重载。
- **像 Go 的地方**：`:=`、`defer`、goroutine 式并发、`x!` 解包 error、标准库直通。

这也是它最大的优点和最大的坑：**四种语言的语义混在一起**，写之前最好先读一遍[类型系统](../syntax/types.md)和[运算符](../syntax/operators.md)里的真值/相等规则。

## 什么时候适合用 ZGG

**适合**：一次性数据脚本、内部工具 CLI、小型 HTTP API、Excel/CSV 报表、定时巡检、给 Go 服务写扩展脚本。

**不适合**：对启动/执行性能极敏感的计算、需要静态类型保障的大型工程、需要成熟 IDE 生态的团队协作项目。

继续阅读：[安装、运行与 CLI](install.md) →
