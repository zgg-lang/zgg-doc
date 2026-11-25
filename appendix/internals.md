# 实现原理、性能与已知限制

## 实现架构

```text
源码
  │  ANTLR4 词法/语法（parser/Zgg*.g4）
  ▼
AST（ast/，每个节点实现 Eval）
  │  树遍历求值（runtime/Context）
  ▼
结果 / 异常
```

- **解析**：ANTLR 生成 Go parser，`ParseVisitor` 直接把语法树转成 AST；支持解析期常量折叠（`DISABLE_PRECALC=1` 可关闭）。
- **执行**：纯 AST 解释，无字节码、无 JIT。
- **作用域**：每个代码块 `PushStack` 一个 `contextFrame`；变量存放在 frame 内的 `sync.Map`，沿 parent 链查找。
- **闭包**：函数值捕获定义处的 frame 链；调用时切换当前 frame。
- **异常**：`panic/recover` + `RuntimeError`（含 `message` / `stack`）。
- **模块**：按路径 + mtime 缓存，可热重载。
- **Go 互操作**：`reflect` 桥接；`stdgolibs` 由脚本生成，覆盖 Go 标准库；支持 `.so` 插件。

## 性能参考

在同一台 Apple M5 / macOS 上实测（2026-06 源码构建）：

| 场景 | ZGG | CPython 3.9 | Node 24 |
|---|---|---|---|
| `fib(26)` 递归 | 0.37 s | 0.016 s | 0.003–0.008 s |
| 1000 万次累加循环 | 3.2 s | 0.36 s | — |
| 1000 万次空循环 | 1.2 s | — | — |
| 启动（hello） | ~20 ms | — | — |
| 峰值内存（hello） | ~17 MB | — | — |

结论：

- 启动快、内存小，适合**胶水逻辑、脚本、服务端编排**。
- 计算密集场景比 CPython 慢约一个数量级（递归约 20 倍），不适合替代通用计算语言。
- 主要开销来自每次块进入/循环迭代新建 `contextFrame + sync.Map`，以及值装箱与成员绑定。

## 已知限制

以下是当前版本（`1c341d4`）确认存在的问题，写生产脚本时需要注意。

### 1. 失败时退出码为 0

断言失败、未捕获异常、语法错误都会打印错误，但进程返回码是 **0**；也没有 `sys.exit` 可以手动设置。

```bash
zgg bad.zgg; echo $?     # 0
```

**建议**：外层用 `try/catch` + 显式写文件/标记来判断成败；CI 中不要只依赖退出码。

### 2. 对象遍历顺序不稳定

对象底层是哈希表，`keys()` / `values()` / `pairs()` / `each()` / `println(obj)` 的顺序不保证。需要稳定输出时显式排序：

```zgg
obj := {b: 2, a: 1}
keys := obj.keys().sort(k => k)
println(keys)
```

`json.encode` 的键序是稳定的（按字典序）。

### 3. 调用栈信息不完整

异常只显示最内层一帧，根帧文件名可能丢失（`:0 (<root>)`）。定位问题时建议在关键函数里打印上下文。

### 4. 循环 import 不会报错

`a` 导入 `b`、`b` 又导入 `a` 会无限递归/卡住，没有环检测。请保持模块依赖为有向无环图。

### 5. 没有 `throw`

`throw` 是保留字但没有语法规则；某些位置写 `throw ...` 甚至会被静默忽略。主动报错请用：

```zgg
try {
    assert false, '错误信息'
} catch (e) {
    println(e.message)
}
```

### 6. 调试模式下的解析崩溃

`DEBUG=1` 时如果源码有特定语法错误，解析器可能触发空指针 panic（Go 栈），而不是打印语法错误。排查语法问题时先不要开 `DEBUG`。

### 7. 并发共享状态不安全

`+=` 等读改写不是原子的；多任务共享对象必须加 `@concurrent.Mutex`，或改用 `Chan` 传递数据。

### 8. 部分 API 有缺陷

| API | 现象 | 替代 |
|---|---|---|
| `@file.append` | `bad file descriptor` | 读 + `rewrite` |
| `db.m(t).count()` | 默认返回 1 | `count('count(1)')` 或 `len(all())` |
| `db.tables()` | SQLite 下语法错误 | 手动 `query` |
| `@udp.Conn` | 初始化时打印 `ListenUDP ...` | 忽略输出 |
| `@sys.Command(...).input()` | 无法关闭 stdin，`wait()` 可能挂起 | 用 `@sh` / `shellResult` |

### 9. 语法层面的小坑

- 只支持单引号字符串；双引号是词法错误。
- 字符串里的 `$` 会触发插值；`'$100'` 直接报错，用 `r'$100'`。
- 对象解构 `{a} := obj` 不可用（数组解构可用）。
- `if` / `switch` 是语句，不能当表达式；用 `when`。
- `?.` 只能用于调用，不能取字段。
- `use` / `use@` 需要出现在表达式位置（`x := use ...`）。
- 三段 `for` 不能省略任何一段。
- 序列化/时间格式化是两套规则：`json` 用 JSON，`time.parse` 用 Go layout，`time.format` 同时支持 Go layout 与 `%Y-%m-%d`。

### 10. 工程化现状

- 测试：仓库中的 `zgg_test.go`、`ast/expr_test.go` 因 API 变更已无法编译；只有 `runtime` 包测试可运行。
- 无 CI 配置；`testcases/` 仅有一个示例。
- 官方 GitBook 文档未覆盖切片、`is`/`in`、推导式、`use@`、`bind`、`concurrent.map` 等新特性（本文档即为补齐）。

## 给维护者的建议

如果要把 ZGG 推向"可被他人依赖"：

1. **退出码**：三类失败分别返回非 0，并补 `sys.exit(code)`。
2. **对象有序**：`ValueObject` 增加插入序，遍历/打印按序输出。
3. **调用栈**：frame 记录 caller，恢复真实调用链；修根帧文件名。
4. **诊断**：包装 ANTLR 错误为"行号 + 期望 + 实际 + 源码行"，修掉解析 panic 与静默 no-op。
5. **测试与 CI**：修复失效测试，把本文档中的示例作为 golden 用例跑起来。
6. **性能**：循环/块不新建 frame（或做 frame 复用），变量解析改为 `(深度, 槽位)`，预计可提升一个数量级。

在此之前，把 ZGG 定位为**团队内部的胶水语言**是合适的：它的语法与标准库已经足够好用，但确定性与工程化仍需谨慎对待。
