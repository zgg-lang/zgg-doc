# 网络与存储

本页覆盖 tcp / udp / kv / redis / nsq / cron / dom / etree / drawing / graph / go 等模块。需要外部服务的模块只列 API 形态，示例以本地可运行的为主。

## tcp

```zgg
// 服务端
srv := @tcp.listen('127.0.0.1:19001')
@concurrent.start(() => srv.acceptLoop(conn => {
    msg := conn.recv(1024)
    conn.send('echo:' + str(msg))
    conn.close()
}))

@time.sleep('200ms')

// 客户端
c := @tcp.connect('127.0.0.1:19001')
c.send('hi')
println(str(c.recv(1024)))     // echo:hi
c.close()
```

| API | 说明 |
|---|---|
| `listen(addr)` | 监听，返回 `TcpListener` |
| `connect(addr[, timeout])` | 建立连接 |
| `listener.accept()` | 接受一个连接 |
| `listener.acceptLoop(handler)` | 循环接受（阻塞） |
| `conn.send(data[, timeout])` | 发送，返回字节数 |
| `conn.recv(max[, timeout])` | 接收，返回 `Bytes`；对端关闭返回 `nil` |
| `conn.addr()` | `{remote, local}` |
| `conn.close()` | 关闭 |

`timeout` 用 Duration 字符串，如 `'5s'`。

## udp

```zgg
srv := @udp.Conn('127.0.0.1:19010')
@concurrent.start(() => {
    [data, addr] := srv.recvFrom(1024)
    srv.sendTo('echo:' + str(data), addr)
})

@time.sleep('200ms')

c := @udp.Conn('127.0.0.1:19011')
c.sendTo('hi', '127.0.0.1:19010')
[d, a] := c.recvFrom(1024)
println(str(d))       // echo:hi
```

| API | 说明 |
|---|---|
| `Conn(addr)` | 绑定本地地址（也可当函数直接调） |
| `sendTo(data, addr)` | 发送 |
| `recvFrom(maxRecv[, timeout])` | 接收，返回 `[data, addr]` |
| `addr()` / `close()` | 地址 / 关闭 |

> 当前实现会在 `Conn` 初始化时向 stdout 打印 `ListenUDP ...` 调试信息。

## kv：KV 抽象

适配器通过 URL scheme 选择：

| scheme | 说明 |
|---|---|
| `fs:///dir?prefix=p` | 本地文件目录 |
| `redis://host:port?prefix=p` | Redis 字符串 |
| `redishash://host:port?hashkey=h&prefix=p` | Redis Hash |

```zgg
// 目录需要已存在
m := @kv.Manager('fs:///tmp/kvstore?prefix=demo')
m.set('k', 'hello')
println(m.get('k'))     // hello
m.close()
```

接口：`get(key)` / `set(key, value[, ttl])` / `close()`。

## redis

```text
r := @redis.open('127.0.0.1:6379')                       // 默认即本地
// r := @redis.open('127.0.0.1:6379', {password: 'x', database: 1})
r.set('name', 'zgg')
println(r.get('name'))
r.close()
```

- `@redis.open([addr][, opts...])`：`opts` 可传整数数据库编号，或 `{username, password, database, readTimeout, connTimeout, writeTimeout}`。
- `RedisClient` 通过 `__getAttr__` 把任意方法名映射为 Redis 命令：`r.hget(...)`、`r.lpush(...)`。
- `r.pipe()` 返回 pipeline 会话，最后 `exec()` 批量提交。

## nsq

```text
// 一次性发布
@nsq.publish('127.0.0.1:4150', 'topic', 'message')

// 复用生产者
p := @nsq.Producer('127.0.0.1:4150')
p.publish('topic', {a: 1})
p.close()

// 消费：dType 为 'nsqd' 或 'nsqlookupd'
c := @nsq.Consumer('nsqd', '127.0.0.1:4150')
c.on('topic', 'channel', (body, msg) => {
    println(str(body))
    msg.Finish()
})
```

## cron：定时任务

```text
app := @cron.App()
app.add('*/5 * * * *', () => println('每 5 分钟'))
app.start()
```

支持秒级 cron 表达式；`app.stop()` 停止，`app.remove(id)` 移除任务。

## dom / etree：HTML 与 XML

```text
// HTML：@dom.fromUrl 返回 Go 的 goquery.Document，方法按 Go 命名
doc := @dom.fromUrl('https://example.com')
println(doc.Find('title').Text())

// XML
x := @etree.fromString('<root><a k="1">v</a></root>')
println(x.find('a').text())
```

`@dom` 目前只提供 `fromUrl`（以及等价的 `@dom(url)` 调用）；本地 HTML 可以先起一个 http 服务再用 URL 访问。

## drawing / graph：绘图

```zgg
c := @drawing.Canvas(400, 300)
c.rect(10.0, 10.0, 100.0, 50.0)
c.text('hello', 20.0, 40.0)
c.save('/tmp/out.png')
println(@file.exists('/tmp/out.png'))
```

`Canvas(width, height)` 支持 `rect` / `circle` / `line` / `arc` / `text` / `fill` / `stroke` / `save`（PNG/JPEG）等；`Font` 类用于字体与文本测量。

`@graph` 目前只有 `readFile`（读取图形数据文件）。

## go：Go 桥接工具

```text
println(@go.type(goValue))
v := @go.convert(123)
println(typeName(v))
```

| 函数 | 说明 |
|---|---|
| `type(v)` / `getType(v)` | 反射类型 |
| `convert(v)` | 转 Go 值 |
| `makeSlice` / `makeMap` / `makeChan` | 构造 Go 容器 |
| `append` | 追加 |
| `int` / `float` / `string` / `bool` / `byte` / `rune` | Go 类型转换 |

## 其他

- `@msgpack`：见[编解码](text-codec.md)。
- `@ip2region`、`@psutil`、`@fsnotify`：见[系统与杂项](math-path-misc.md)。
