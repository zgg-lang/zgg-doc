# 在 Go 中嵌入 ZGG

ZGG 可以作为库嵌入 Go 程序：执行脚本、求值表达式、注入变量、获取导出结果。

模块路径：`github.com/zgg-lang/zgg-go`

## 基本用法

```go
package main

import (
	"context"
	"fmt"

	"github.com/zgg-lang/zgg-go"
)

const code = `
    export func greet(name) {
        return 'hello, ' + name
    }
    export result := greet('world')
`

func main() {
	exports, err := zgg.RunCode(code)
	if err != nil {
		panic(err)
	}
	fmt.Println(exports["result"]) // hello, world
}
```

## 注入变量

`zgg.Var{Name, Value}` 用于注入变量：

- `Value` 直接传 Go 值：脚本里拿到的是 `GoValue`（可调用其方法/字段）。
- 用 `zgg.Val{v}` 包装：会转换成 ZGG 原生值（数字、字符串、map、slice 等）。

```go
type User struct{ Coins int }

func (u *User) AddCoins(n int) { u.Coins += n }

func main() {
	user := &User{Coins: 10}

	_, err := zgg.RunCode(`
		user.AddCoins(n)
	`, zgg.Var{Name: "user", Value: user}, zgg.Var{Name: "n", Value: zgg.Val{5}})
	if err != nil {
		panic(err)
	}
	fmt.Println(user.Coins) // 15
}
```

## Runner：可复用的执行环境

```go
runner := zgg.NewRunner(context.Background()).
	Filename("inline.zgg").
	Workdir(".").
	Args("a", "b").
	Stdout(os.Stdout).
	Stderr(os.Stderr)

if _, err := runner.Run(`println(@sys.args)`); err != nil {
	panic(err)
}
```

| 方法 | 说明 |
|---|---|
| `NewRunner(ctx)` | 创建执行器 |
| `Filename(name)` | 设置脚本名（影响 `__file__` 与错误信息） |
| `Workdir(dir)` | 设置相对导入的基准目录 |
| `Args(...)` | 设置 `@sys.args` |
| `Var(name, value)` | 注入变量 |
| `Stdout(w)` / `Stderr(w)` | 重定向输出 |
| `IsDebug(bool)` / `CanEval(bool)` | 调试 / 允许 `eval` |
| `Run(code)` | 执行模块，返回导出结果的 `map[string]interface{}` |
| `Eval(expr)` | 求值表达式 |
| `CompileCode(code)` / `CompileExpr(expr)` | 预编译为 AST，可重复执行 |
| `Reset()` | 重置执行环境 |

## 预编译

`CompileCode` / `CompileExpr` 返回 `ast.Node`，可以缓存后重复执行，跳过解析开销：

```go
node, err := zgg.CompileCode(code)
if err != nil {
	panic(err)
}
for i := 0; i < 3; i++ {
	out, err := zgg.RunCode(node)
	if err != nil {
		panic(err)
	}
	fmt.Println(out)
}
```

## 包级便捷函数

| 函数 | 说明 |
|---|---|
| `zgg.RunCode(code, opts...)` | 执行模块，返回导出 map |
| `zgg.Eval(expr, opts...)` | 求值表达式，返回 `interface{}` |
| `zgg.CompileCode(code)` | 编译模块 |
| `zgg.CompileExpr(expr)` | 编译表达式 |

## 自定义导入

`zgg.ImportFunc` 是一个可传给 `RunCode` / `Eval` 的选项，用来接管 `import()` 的模块加载（例如从数据库、对象存储读取脚本）：

```go
custom := zgg.ImportFunc(func(
	c *runtime.Context,
	name, code, importType string,
	reloadIfNewer bool,
) (runtime.Value, int64, bool) {
	// 返回 (模块值, 修改时间, 是否成功)
	return runtime.Undefined(), 0, false
})

exports, err := zgg.RunCode(code, custom)
```

## 注意

- 宿主与脚本共享 goroutine：脚本里的长任务会阻塞调用方，需要异步时自行放到 goroutine。
- 脚本错误以 `error` 返回；`try/catch` 只捕获脚本运行时异常。
- 并发调用同一个 `Runner` 不安全，请每个 goroutine 使用独立 Runner（或使用包级函数，其内部有池化）。
