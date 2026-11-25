# 安装、运行与 CLI

## 安装

### 方式一：一键脚本（官方）

```bash
curl -k https://www.zgg-lang.org/install/install.sh | bash
```

脚本会下载对应平台的二进制并安装到 `PATH`。更新解释器：

```bash
zgg --update
```

### 方式二：直接下载二进制

官网文档提供各平台产物：Linux / macOS / Windows（amd64、arm64）。

### 方式三：从源码构建

需要 Go 1.24+：

```bash
git clone https://github.com/zgg-lang/zgg-go.git
cd zgg-go
make cmd                 # 产物：bin/zgg
# 或手动：
CGO_ENABLED=0 go build -o bin/zgg cmd/*.go
```

验证：

```bash
zgg --info
# BUILD_TIME : 2026-06-24T14:24:14+0800
# BUILD_HASH : 1c341d4...
```

## 运行方式

```bash
zgg script.zgg                 # 运行脚本，后续参数进入 @sys.args
zgg -c "println(1 + 2)"        # 执行一段代码
echo "println('hi')" | zgg stdin   # 从标准输入读代码
zgg -m http                    # 以模块方式启动内置库（执行其 __main__，如文件服务器）
zgg                            # 进入 REPL
```

脚本可以带 shebang（`#!` 开头的第一行会被忽略）：

```zgg
#!/usr/bin/env zgg
println('runnable as executable')
```

## REPL

```text
$ zgg
zgg> a := 1
1
zgg> a + 1
2
zgg> func f(x) { return x * 2 }
<func f>
zgg> f(3)
6
```

REPL 支持多行输入（未闭合的 `{` 会继续等待），提示符与历史记录位于 `/tmp/zgg_history`。

## 命令行子命令

| 命令 | 作用 |
|---|---|
| `zgg hub` | 启动模块仓库服务（内部包管理服务端） |
| `zgg deps` | 按 `zggdeps.txt` 下载/更新依赖模块 |
| `zgg add <module...>` | 追加依赖到 `zggdeps.txt` 并立即拉取 |
| `zgg ws [addr]` | 启动 WebSocket 版 REPL 服务 |
| `zgg showast <file>` | 打印源码的 AST（调试解析器用） |
| `zgg expr-ast <expr>` | 打印表达式的 AST |

## 环境变量

| 变量 | 作用 |
|---|---|
| `ZGGPATH` | 模块搜索根目录，多个用 `:` 分隔；同时用于查找 `_autoimport.zgg` |
| `CAN_EVAL` | 非空时允许脚本调用 `eval()`（默认禁止） |
| `DEBUG` | 非空时开启调试日志 / pprof（`/tmp/pprof_result.pprof`） |
| `DISABLE_PRECALC` | 设为 `1` 关闭解析期常量折叠（对比性能时用） |
| `INSTALL_SH_URL` | 覆盖 `zgg --update` 使用的安装脚本地址 |

## 模块依赖

项目根目录的 `zggdeps.txt` 每行一个模块名：

```text
webhost
feishu
```

```bash
zgg add webhost feishu   # 写入 zggdeps.txt 并下载
zgg deps                 # 按文件重新同步
```

下载后的模块放在 `zgg_modules/` 下，脚本中直接 `import('webhost')` 即可。

## 目录约定

一个典型的 ZGG 项目：

```text
my-project/
├── main.zgg
├── lib/
│   └── util.zgg
├── zggdeps.txt
└── zgg_modules/
    └── webhost/
        └── index.zgg
```

- 相对导入以**当前脚本所在目录**为基准：`import('./lib/util')`。
- 目录导入会找该目录下的 `index.zgg`。
- 绝对路径与 `ZGGPATH` 中的模块也可直接 `import('name')`。

继续阅读：[快速上手](quickstart.md) →
