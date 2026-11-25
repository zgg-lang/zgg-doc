# ZGG 语言文档

> 面向 Go 生态的通用脚本语言 —— 语法轻量、动态类型、内置全部 Go 标准库能力。
>
> 本文档基于 `zgg-go` 源码（2026-06-24，commit `1c341d4`）整理，所有示例均已在 `zgg` 解释器上验证运行。

## ZGG 是什么

ZGG 是一门**动态类型的通用脚本语言**，由 Go 实现（ANTLR 语法 + AST 树遍历解释器）。它的设计目标是：用接近 Python/JavaScript 的书写体验，直接使用 Go 生态的能力，适合写 Web 服务、数据处理脚本、自动化运维工具。

```zgg
println('Hello, ZGG!')

func fib(n) {
    if n < 2 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

println([fib(i) for i in 1..10])
```

运行：

```bash
zgg hello.zgg
```

## 核心特性

| 特性 | 说明 |
|---|---|
| 动态类型 | 无需声明类型；`Int` / `Float` / `BigNum` / `Str` / `Bytes` / `Bool` / `Nil` / `Undefined` / `Array` / `Object` / `Func` / `Type` |
| 现代语法 | 字符串插值、箭头函数、闭包、解构、切片、推导式、`when` 表达式、可选调用 `?.`、空值合并 `??` |
| 面向对象 | `class`、继承、`super`、静态成员、魔术方法（`__init__` / `__getAttr__` / `__call__` / 运算符重载） |
| 函数式 | 一等函数、`map/filter/reduce`、隐式 `it`、占位符偏应用 `add(%, 1)` |
| 资源管理 | `defer` / `blockDefer` / `defer {}` / `use` / `use@close` |
| 错误处理 | `try/catch/finally`、`assert`、Go error 解包 `expr!`、语句级兜底 `?? {}` |
| 模块系统 | `import` / `export`、`@mod` 与 `@@fmt` 短导入、文本/JSON/CSV/字节导入、热重载 |
| 并发 | `concurrent.start`（future）、`concurrent.map`、`Chan`、`Mutex`、`Limiter` |
| Go 直通 | `import('gostd/...')` 使用任意 Go 标准库；`reflect` 桥接 Go 值与结构体 |
| 标准库 | 40 个内置模块入口（含别名）：json / yaml / http / db / xlsx / time / regex / ptable / tcp / redis … |
| 可嵌入 | 通过 `github.com/zgg-lang/zgg-go` 在 Go 程序中执行 ZGG 脚本 |

## 适用场景

- **Web 服务**：`@http.createServer` 路由 + JSON 接口 + 静态文件 + WebSocket。
- **数据脚本**：JSON/YAML、Excel（xlsx）、SQLite/MySQL、正则清洗、终端表格（ptable）报表。
- **自动化运维**：`@sh` 执行命令、`@sys` 读取环境/参数、`@fsnotify` 监听文件、`@psutil` 采集系统指标。
- **嵌入式脚本**：把 ZGG 当作 Go 程序的规则/配置/扩展脚本引擎。

## 文档结构

| 部分 | 内容 |
|---|---|
| [一、语言特性概述](overview/README.md) | 设计定位、安装运行、快速上手、特性清单 |
| [二、基本语法](syntax/README.md) | 词法、变量、类型、运算符、字符串、容器、控制流、函数、类、错误、模块、并发 |
| [三、标准库](stdlib/README.md) | 内置函数、类型方法、json/yaml、file、time、regex、http、db、xlsx、cli、编解码、网络 |
| [附录](appendix/README.md) | 在 Go 中嵌入、实现原理与性能、已知限制 |

## 本地预览与校验

### GitBook

仓库根目录已包含 `README.md`、`SUMMARY.md` 与 `.gitbook.yaml`，可直接在 GitBook.com 中导入该目录。

本地预览（需要 Node.js）：

```bash
npx gitbook-cli install
npx gitbook-cli serve .
```

也可以直接用任意 Markdown 阅读器按 `SUMMARY.md` 的顺序浏览。

### 校验示例

文档中的 ```` ```zgg ```` 代码块都可以直接运行；`scripts/check_examples.py` 会逐个提取执行：

```bash
ZGG_BIN=/path/to/zgg python3 scripts/check_examples.py
```

当前基线：213 个代码块全部通过（zgg-go `1c341d4`）。

> 少数依赖外部服务或会阻塞的示例使用 ```` ```text ```` 标记，不参与自动执行（如 redis / nsq / cron / 文件监听）。

## 版本与兼容性

- 文档对应源码：`zgg-go` 仓库 `1c341d4`（2026-06-24）。
- 语法以 `parser/ZggParser.g4` 为准，标准库以 `builtin_libs/StdLibMap` 为准。
- 语言仍在演进，升级后请以实际解释器行为为准；已知限制见[附录](appendix/internals.md)。
