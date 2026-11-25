# sys / sh / flag / ptable

这一组模块是写命令行工具与报表的主力。

## sys：进程与系统

```zgg
sys := @sys
```

| 成员 | 说明 |
|---|---|
| `args` | 脚本参数数组（`zgg script.zgg a b` → `[a, b]`） |
| `env(name)` | 读取环境变量 |
| `loadEnv(file)` | 从文件加载环境变量 |
| `shellResult(cmds[, env])` | 用 shell 执行字符串命令，返回输出 |
| `Command(name)` | 构造外部命令对象 |
| `createTempFile()` | 创建临时文件，返回 `{name, drop()}` |
| `getResult(...)` | 执行并获取结构化结果 |

```zgg
println(@sys.args)                 // 例如 [a, b]
println(@sys.env('HOME'))

out := @sys.shellResult('echo hello')
println(out)

tmp := @sys.createTempFile()
println(tmp.name)
tmp.drop()
```

### Command

```zgg
println(@sys.Command('date').waitOutput())   // 返回命令输出（Bytes）
```

| 方法 | 说明 |
|---|---|
| `waitOutput()` | 运行并返回合并输出（`Bytes`），适合一次性命令 |
| `start()` | 启动进程 |
| `onStdout(cb)` / `onStderr(cb)` | 注册输出回调（需在 `start` 前） |
| `wait()` | 等待结束，返回退出码 |
| `kill()` | 结束进程 |

> 简单的命令执行优先用 `@sh` 或 `@sys.shellResult`；`Command` 适合需要进程控制/流式输出的场景。
> 注意：`Command` 目前没有暴露关闭 stdin 的方法，`input()` 后 `wait()` 可能一直等待。

## sh：管道式命令

```zgg
println(@sh.echo('hello').text().trim())      // hello
println(@sh.ls('-1', '/tmp').lines())          // 每行一个元素
println(@sh.echo('{"a":1}').json())            // 解析为对象
```

`@sh.命令名(参数...)` 返回 Command 对象，支持：

| 方法 | 说明 |
|---|---|
| `text()` | 输出为字符串 |
| `lines()` | 输出按行拆分 |
| `json()` | 输出解析为 JSON |
| `__str__()` | 同 `text()` |

命令失败会抛异常；需要忽略失败时用 `try/catch`。

## flag：命令行参数

```zgg
p := @flag.Parser('mycli')
p.str('host', '监听地址')
p.int('port', '端口')
p.bool('verbose', '详细日志')
p.float('ratio', '比例')
p.duration('timeout', '超时')

[help, opts, rest] := p.parse(...@sys.args)
println(help, opts.host, opts.port, opts.verbose, rest)
```

- 声明方法：`str` / `int` / `bool` / `float` / `duration`，第一个参数是名字，第二个是用法说明。
- `parse(...)` 接收**展开后的参数**（`...@sys.args`），返回 `[是否帮助, 选项对象, 剩余参数]`。
- 选项访问：`opts.host`、`opts.port`。

运行：

```bash
zgg cli.zgg -host 0.0.0.0 -port 8080 -verbose
```

## ptable：终端表格

```zgg
t := @ptable('name', 'age')
t.add('alice', 30)
t.addArray([['bob', 20], ['carol', 40]])
t.addObject({name: 'dave', age: 50})

println(t.txt())        // ASCII 表格（默认）
println(t.markdown())   // Markdown 表格
println(t.html())       // HTML 表格
println(t.csv())        // CSV
```

| 方法 | 说明 |
|---|---|
| `add(...)` | 追加一行（按列顺序） |
| `addArray(rows)` | 批量追加（二维数组） |
| `addObject(obj)` / `addObjects(arr)` | 按列名从对象取值追加 |
| `columns()` | 列名数组 |
| `toArray(includHeaders?)` | 转二维数组 |
| `slice(begin, end)` | 截取行 |
| `txt()` / `ascii()` / `unicode()` | 文本表格 |
| `markdown()` / `md()` | Markdown |
| `html()` | HTML |
| `csv()` | CSV |
| `colFormat(col, format)` | 设置某列格式 |
| `addCol(name[, fill])` | 追加列，可用函数填充 |

### 结尾对齐示例

```zgg
t := @ptable('word', 'count')
t.add('beta', 2)
t.add('alpha', 1)
println(t.txt())
```

```text
+-------+-------+
| word  | count |
+-------+-------+
| beta  |     2 |
| alpha |     1 |
+-------+-------+
```

## 组合示例：统计命令输出

```zgg
lines := @sh.ls('-1', '/tmp').lines()

t := @ptable('index', 'name')
for i, name in lines {
    t.add(i, name)
}
println(t.txt())
```
