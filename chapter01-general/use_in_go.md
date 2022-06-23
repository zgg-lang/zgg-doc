# 在Go程序中嵌入ZGG脚本

ZGG语言从开发之初就支持在Go语言中使用（毕竟ZGG的开发团队所在公司的主力开发语言是Go）。以下是如何在一个Go的项目中集成ZGG引擎

## 如何集成ZGG？

### 第一步：安装依赖库

```
go get github.com/zgg-lang/zgg-go
```

### 第二步：参考下面例子完成代码集成

#### 1.简单使用Demo（展示一下核心接口的用法）

```go
package main

import (
	"fmt"

	"github.com/zgg-lang/zgg-go"
)

const demoModule = `
	fib := n => when n {
		1, 2 -> 1
		else -> fib(n - 1) + fib(n - 2)
	}
	export result := fib(n)
`

const demoExpr = `n ** 2`

func main() {
	// 使用源码运行模块
	if exported, err := zgg.RunCode(demoModule, zgg.Var{"n", zgg.Val{10}}); err != nil {
		panic(err)
	} else {
		fmt.Println("module exported result:", exported["result"].(int64))
	}
	// 使用预编译结果运行模块
	if compiled, err := zgg.CompileCode(demoModule); err != nil {
		panic(err)
	} else if exported, err := zgg.RunCode(compiled, zgg.Var{"n", zgg.Val{10}}); err != nil {
		panic(err)
	} else {
		fmt.Println("module exported result:", exported["result"].(int64))
	}
	// 使用源码进行表达式求值
	if result, err := zgg.Eval(demoExpr, zgg.Var{"n", zgg.Val{10}}); err != nil {
		panic(err)
	} else {
		fmt.Println("expr result:", result.(int64))
	}
	// 使用预编译结果进行表达式求值
	if compiled, err := zgg.CompileExpr(demoModule); err != nil {
		panic(err)
	} else if result, err := zgg.Eval(compiled, zgg.Var{"n", zgg.Val{10}}); err != nil {
		panic(err)
	} else {
		fmt.Println("expr result:", result.(int64))
	}
}
```

#### 2. 调用Go方法和对象
```go
package main

import (
	"fmt"

	"github.com/zgg-lang/zgg-go"
)

type User struct {
	Coins int
}

func (user *User) AddCoins(c int) {
	user.Coins += c
}

const code = `
	user.AddCoins(n) // 在ZGG代码里面调用go值的方法
`

func main() {
	user := User{Coins: 10}
	_, err := zgg.RunCode(code,
		zgg.Var{"user", &user},   // 注入Go值，可直接注入
		zgg.Var{"n", zgg.Val{5}}, // 如果希望注入的值自动转成ZGG基本类型，需要把Go的值用zgg.Val包装一下
	)
	if err != nil {
		fmt.Println("run error:", err)
	} else {
		fmt.Println("after RunCode, user.Coins", user.Coins)
	}
}
```

## 核心接口说明：

----------

### func RunCode(script interface{}, opts ...ExecOption) (exported map[string]interface{}, err error)

* 功能：运行代码模块
* 参数：
  * script: 待运行的代码，可为源码(string）或者预先编译好的代码对象(ast.Node)
  * opts: 需要注入到运行环境的内容。目前仅支持注入变量
* 返回值：
  * exported: 运行成功后，返回这个代码模块导出的内容。err为nil时，exported一定不为nil
  * err: 当且仅当运行失败时不为空

-----------

### func Eval(expr interface{}, opts ...ExecOption) (interface{}, error)
* 功能： 运行表达式求值
* 参数：
  * script: 待运行的表达式代码，可为源码(string）或者预先编译好的代码对象(ast.Node)
  * opts: 需要注入到运行环境的内容。目前仅支持注入变量
* 返回值：
  * exported: 运行成功后，返回这个表达式的返回值
  * err: 当且仅当运行失败时不为空

-----------

### func CompileCode(code interface{}) (compiled ast.Node, err error)
* 功能：编译代码模块
* 参数：
  * code: 待运行的表达式代码，可为源码(string）或者预先编译好的代码对象(ast.Node)
* 返回值：
  * compiled: 编译结果。如果入参code是预先编译好的，则直接返回code
  * err: 当且仅当运行失败时不为空

-----------

### func CompileExpr(code interface{}) (ast.Node, error)
* 功能：编译表达式
* 参数：
  * code: 待运行的表达式代码，可为源码(string）或者预先编译好的代码对象(ast.Node)
* 返回值：
  * compiled: 编译结果。如果入参code是预先编译好的，则直接返回code
  * err: 当且仅当运行失败时不为空