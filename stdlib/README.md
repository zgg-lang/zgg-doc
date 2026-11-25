# 标准库总览

ZGG 的标准库分三层：

1. **内置函数**：无需 import，直接可用（`println`、`len`、`range`、`json` 之外的通用工具）。
2. **内置模块**：用 `import('模块名')` 或短导入 `@模块名` 使用，由 Go 实现。
3. **Go 标准库**：`import('gostd/包路径')` 直接使用任意 Go 标准库。

## 内置函数（免 import）

`println` `printf` `sprintf` `int` `float` `str` `bytes` `typeName` `type` `len` `range` `seq` `sha1` `sha256` `md5` `import` `isUndefined` `isCallable` `isArray` `isObject` `assertError` `rand` `eval` `bind` `max` `min` `input` `lookup` `log`

详见[内置函数与类型方法](builtins.md)。

## 内置模块

| 模块 | 短导入 | 用途 |
|---|---|---|
| `json` | `@json` | JSON 编解码、格式化、JSONPath 查询 |
| `yaml` | `@yaml` | YAML 编解码 |
| `file` | `@file` | 文件读、写、追加、判断 |
| `time` | `@time` | 时间解析/格式化/运算、定时 |
| `regex` / `regex2` | `@regex` | 正则查找、替换、分割（两种结果形态） |
| `http` | `@http` | HTTP 客户端、服务端、静态文件、WebSocket |
| `db` | `@db` | SQLite / MySQL 访问与 ActiveRecord |
| `xlsx` | `@xlsx` | Excel 读写（基于 excelize） |
| `ptable` | `@ptable` | 终端表格 / Markdown / HTML 输出 |
| `sys` | `@sys` | 参数、环境变量、子进程、临时文件 |
| `sh` | `@sh` | 管道式执行 shell 命令 |
| `flag` | `@flag` | 命令行参数解析 |
| `template` | `@template` | Go template 渲染（文本 / HTML） |
| `url` | `@url` | URL 编解码、表单编解码 |
| `base64` | `@base64` | Base64 编解码 |
| `hash` | `@hash` | md5/sha1/sha256/crc/fnv、HMAC |
| `compress` | `@compress` | GZIP / ZLIB / FLATE 压缩 |
| `binary` | `@binary` | 二进制读写（定长/varint） |
| `math` | `@math` | 数学函数、组合数、向量 |
| `path` | `@path` | 路径拼接、glob、目录遍历 |
| `random` | `@random` | 随机数、随机选择、洗牌 |
| `psutil` | `@psutil` | CPU / 进程指标 |
| `fsnotify` | `@fsnotify` | 文件变更监听 |
| `ip2region` | `@ip2region` | IP 归属地查询 |
| `tcp` | `@tcp` | TCP 客户端/服务端 |
| `udp` | `@udp` | UDP 收发 |
| `kv` | `@kv` | KV 抽象（文件 / Redis） |
| `redis` | `@redis` | Redis 客户端与 pipeline |
| `nsq` | `@nsq` | NSQ 生产/消费 |
| `cron` | `@cron` | 定时任务 |
| `concurrent` | `@concurrent` | future、并发映射、Chan、Mutex、Limiter |
| `msgpack` | `@msgpack` | MessagePack 编解码 |
| `dom` | `@dom` | HTML DOM 解析（goquery） |
| `etree` | `@etree` | XML 树操作 |
| `graph` | `@graph` | 图表/绘图辅助 |
| `drawing` | `@drawing` | 2D 绘制（gg） |
| `go` | `@go` | Go 类型/值桥接工具 |

## 使用方式

```zgg
// 完整 import
json := import('json')
println(json.encode({a: 1}))

// 短导入（等价）
println(@json.encode({a: 1}))

// Go 标准库
fmt := import('gostd/fmt')
println(fmt.Sprintf('%v', 42))

// 短导入 Go 标准库
println(@@strings.ToUpper('abc'))
```

模块是单例：第一次 import 时初始化，之后复用同一个对象。个别模块有副作用初始化（如 `http` 的服务端注册），属于例外。

> 源码中的 `image`、`xml`、`hub` 尚未注册进 `StdLibMap`，当前版本无法通过 `import` 使用。

## 阅读顺序建议

- 日常脚本：内置函数 → [file](file.md) → [json/yaml](json-yaml.md) → [time](time.md) → [regex](regex.md)。
- Web / 服务：[http](http.md) → [db](db.md) → [xlsx](xlsx.md)。
- 运维：[cli（sys/sh/flag/ptable）](cli.md) → [math/path/misc](math-path-misc.md) → [network](network.md)。
