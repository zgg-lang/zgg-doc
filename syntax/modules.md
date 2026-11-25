# 模块与导入

## 基本用法

一个 `.zgg` 文件就是一个模块。用 `export` 决定导出内容，用 `import()` 引入：

```zgg
// mathx.zgg
export pi := 3.14159

export func square(x) {
    return x * x
}

func internalHelper() {   // 没有 export，外部不可见
    return 1
}
```

```zgg
// 先准备模块文件（实际项目中是手写的 lib/mathx.zgg）
@file.rewrite('./mathx.zgg', 'export pi := 3.14159\nexport func square(x) { return x * x }')

m := import('./mathx.zgg')
println(m.pi, m.square(3))     // 3.14159 9
```

- `import` 返回一个对象，包含所有 `export` 的名字。
- 模块在**首次导入时执行一次**，之后命中缓存。
- `export` 只能出现在模块顶层。

## 导入路径

| 写法 | 含义 |
|---|---|
| `import('./lib/util')` | 相对**当前脚本所在目录** |
| `import('../shared/util')` | 上一级目录 |
| `import('/abs/path/util')` | 绝对路径 |
| `import('webhost')` | 在 `ZGGPATH` / 工作目录中查找 |
| `import('webhost/index')` | 目录会默认找 `index.zgg` |

支持的后缀：`.zgg`（脚本）、`.so`（Go 插件）。

## 短导入：`@` 与 `@@`

```zgg
println(@time.now().year)          // 等价于 import('time').now()
println(@json.encode({a: 1}))

// @@ 前缀表示 Go 标准库
fmt := import('gostd/fmt')
println(@@fmt.Sprintf('%v', 42))
```

- `@name` → `import('name')`
- `@@name` → `import('gostd/name')`
- 名字中的 `__` 会转成路径分隔符：`@@net__http` → `gostd/net/http`。

也就是说短导入是**语法**，不是字符串：写 `@time.now()`，不要写 `import('@time')`。

## 导入类型

`import(name, reload?, type?)` 的第三个参数：

| type | 结果 |
|---|---|
| `'script'`（默认） | 执行脚本，返回导出对象 |
| `'text'` | 文件内容字符串 |
| `'bytes'` | 文件内容 `Bytes` |
| `'json'` | 解析 JSON 为对象/数组 |
| `'csv'` | 解析 CSV 为二维数组（全部是字符串） |

```zgg
@file.rewrite('./data.csv', 'a,b\n1,2\n')
@file.rewrite('./conf.json', '{"x": 1}')
@file.rewrite('./note.txt', 'hello')

rows := import('./data.csv', false, 'csv')
println(rows)          // [[a, b], [1, 2]]

conf := import('./conf.json', false, 'json')
println(conf.x)

text := import('./note.txt', false, 'text')
println(text)
```

## 缓存与热重载

- 模块按路径缓存，并记录文件修改时间。
- `import(path, true)`：文件有更新时重新加载。
- 这对 REPL、长驻服务的热更新很有用。

```zgg
@file.rewrite('./lib.zgg', 'export v := 1')
m1 := import('./lib.zgg')
println(m1.v)

@file.rewrite('./lib.zgg', 'export v := 2')
m2 := import('./lib.zgg', true)     // reloadIfNewer
println(m2.v)
```

## isMain

同一个文件既可作为主脚本运行，也可被导入：

```zgg
export func helper() { return 1 }

if isMain {
    println('作为主程序运行')
}
```

## 模块搜索路径

- 当前脚本目录（相对导入）。
- 当前工作目录。
- `ZGGPATH` 环境变量中的目录（`:` 分隔）。

`ZGGPATH` 目录下的 `_autoimport.zgg` 会在启动时自动导入，其中的导出名会注入全局作用域。

## 依赖管理

```bash
zgg add webhost feishu    # 写入 zggdeps.txt 并下载
zgg deps                  # 按 zggdeps.txt 同步
```

依赖下载到项目的 `zgg_modules/` 目录，之后 `import('webhost')` 即可。

## Go 标准库

```zgg
@file.rewrite('/tmp/a.txt', 'hello')

http := import('gostd/net/http')
os := import('gostd/os')

f := os.Open('/tmp/a.txt')!
defer f.Close()
println('opened')
```

几点注意：

- 调用 Go 函数时，参数会按目标参数类型转换；传给 `...interface{}` 的数字会以 `float64` 出现，格式化建议用 `%v`。
- Go 的 `(value, error)` 返回值可以用 `!` 解包。
- Go 结构体字段/方法直接以成员方式访问。

## .so 插件

`.so` 文件按 Go plugin 规则加载，需导出 `New` 符号：

```text
plugin := import('./bin/mylib.so')
```

插件适合把性能敏感或需要 CGO 的能力做成原生扩展。

继续阅读：[并发编程](concurrency.md) →
