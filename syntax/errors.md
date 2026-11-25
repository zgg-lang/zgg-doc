# 错误处理

## 异常模型

ZGG 的运行时错误统一是 `RuntimeError`（Go 侧用 `panic/recover` 实现），错误对象有两个字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `message` | `Str` | 错误描述 |
| `stack` | `Array` | `[文件名, 行号, 函数名]` 的数组 |

## try / catch / finally

```zgg
try {
    println(1 / 0)
} catch (e) {
    println('caught:', e.message)     // caught: division by zero
} finally {
    println('finally')
}
```

- `catch (e)` 捕获运行时错误；不写 catch 时 `finally` 仍会执行。
- `finally` 不会改变 `try` 中的返回值。

```zgg
func f() {
    try {
        return 'try'
    } finally {
        println('cleanup')
    }
}
println(f())      // 先打印 cleanup，再输出 try
```

## assert

```zgg
try {
    assert 1 == 1
    assert 1 == 2, '必须相等'
} catch (e) {
    println(e.message)      // Assertion fail! 必须相等
}
```

失败时抛出 `Assertion fail! <消息>`：

```text
Exception! Assertion fail! 必须相等
```

`assert` 常用于脚本前置条件、单元测试式检查。

## 解包 Go error：`!`

Go 风格返回值 `(value, error)` 可以用 `!` 解包：

```zgg
@file.rewrite('/tmp/data.txt', 'hello')

// gostd 函数返回 (value, error)
f := import('gostd/os')
content := f.ReadFile('/tmp/data.txt')!
println(len(content))
```

- 成功：返回去掉最后一个（error）元素后的值。
- 失败：抛出 `assert error fail! ...` 异常。

## 默认值与兜底

### `??`：空值默认

```zgg
name := nil
println(name ?? 'anonymous')

port := 0
println(port ?? 8080)      // 0（只有 nil/undefined 才触发）
```

### `?? {}`：调用失败兜底

只能跟在一个**调用语句**后面；成功则继续，失败则执行代码块：

```zgg
@file.readBytes('/tmp/not-exists') ?? {
    println('读取失败，使用默认配置')
}
println('继续执行')
```

> `?? {}` 是语句级结构，不能作为表达式赋值（`x := call() ?? {}` 不支持）。

## 主动抛错

ZGG 目前没有 `throw` 语句（`throw` 是保留字但没有语法规则），需要中断执行时：

```zgg
try {
    assert false, '业务校验失败'
} catch (e) {
    println(e.message)
}
```

或在函数里触发一个运行时错误（例如除零、类型错误），再用 `try/catch` 捕获。生产代码建议用 `assert` 表达"不可能发生"的约束。

## 常见异常清单

| 消息 | 原因 |
|---|---|
| `variable x not exists` | 给未声明变量赋值 |
| `variable x redefined` | 同作用域重复 `:=` |
| `X is not callable` | 调用了非函数值 / 拼错方法名 |
| `division by zero` | 整数除零 |
| `Cannot plus between X and Y` | 不支持的类型运算 |
| `str requires ..., got ...` | 参数类型不符 |
| `Assertion fail! ...` | `assert` 失败 |

继续阅读：[模块与导入](modules.md) →
