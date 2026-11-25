# http 客户端与服务端

```zgg
http := @http
```

## 客户端

### 快捷方法

| 方法 | 返回 | 说明 |
|---|---|---|
| `get(url[, headers])` | `Bytes` | GET，返回原始字节 |
| `getText(url[, headers])` | `Str` | GET，返回文本 |
| `getLines(url[, headers])` | `Array<Str>` | GET，按行返回 |
| `getJson(url[, headers])` | `Any` | GET 并解析 JSON |
| `postForm(url, form[, headers])` | `Bytes` | 表单 POST |
| `postJson(url, value[, headers])` | `Bytes` | JSON POST |
| `postMultipartForm(url, form[, headers])` | `Bytes` | multipart POST |
| `escape(strOrObject)` / `unescape(str)` | `Str` | URL 编码/解码 |

```zgg
// 起一个本地服务用于演示
srv := @http.createServer()
srv.route('/api', ctx => ctx.writeJson(200, {ok: true}))
@concurrent.start(() => srv.serve('127.0.0.1:18140'))
@time.sleep('300ms')

text := @http.getText('http://127.0.0.1:18140/api')   // Str
lines := @http.getLines('http://127.0.0.1:18140/api') // Array<Str>
conf := @http.getJson('http://127.0.0.1:18140/api')   // 解析后的对象
data := @http.get('http://127.0.0.1:18140/api')!      // Bytes

println(text.trim())
println(len(lines), conf.ok, data.len())

rsp := @http.postJson('http://127.0.0.1:18140/api', {name: 'zgg'})
println(rsp.len() > 0)
```

> 这些方法在失败时直接抛异常（不会返回 `(value, error)`），需要兜底请用 `try/catch` 或 `?? {}`。

### Request / Response

需要自定义 method、header、body、超时、证书时用 `Request`：

```zgg
req := @http.Request('POST', 'https://example.com/api')   // 或省略 method 默认 GET
req.header('Content-Type', 'application/json')
req.header('X-Token', 'abc')
req.data(bytes(@json.encode({a: 1})))
req.timeout('10s')

resp := req.call()
println(resp.text())          // 文本
println(resp.header('Content-Type'))
println(resp.bytes().len())   // 原始字节（若 body 未被读过）
```

| Request 方法 | 说明 |
|---|---|
| `header(k, v)` | 添加请求头 |
| `data(bytes)` | 设置请求体 |
| `form(obj)` | 设置表单并 POST |
| `multipartForm(obj)` | 设置 multipart 表单 |
| `timeout(duration)` | 超时（如 `'10s'`） |
| `followRedirect(bool)` | 是否跟随重定向 |
| `tlsConfig({certFile, keyFile, ...})` | 客户端证书 |
| `certFile(path)` | 证书文件 |
| `call()` | 发起请求，返回 Response |

| Response 方法 | 说明 |
|---|---|
| `text()` | 读取 body 为字符串 |
| `json()` | 读取 body 并解析 JSON |
| `bytes()` | 读取 body 为字节 |
| `header(name)` | 取响应头 |
| `chunk(callback)` / `iterChunk()` | 流式读取 |
| `close()` | 关闭 |

> body 只能被消费一次：先 `text()` 再 `json()` 会得到 EOF 错误。

### WebSocket 客户端

```zgg
srv := @http.createServer()
srv.routeWebsocket('/ws', ws => {
    msg := ws.read()
    ws.write('echo:' + msg)
})
@concurrent.start(() => srv.serve('127.0.0.1:18141'))
@time.sleep('300ms')

c := @http.connectWebsocket('ws://127.0.0.1:18141/ws')
c.write('hello')
println(c.read())      // echo:hello
c.close()
```

| 方法 | 说明 |
|---|---|
| `write(data)` | 发送文本/字节/对象 |
| `read()` | 读取一条消息 |
| `writeJson(obj)` / `readJson()` | JSON 消息 |
| `close()` | 关闭连接 |

## 服务端

### 创建与路由

```zgg
srv := @http.createServer()            // 可传 {serverName: 'my-server'}

srv.route('/api/hello', ctx => {
    name := ctx.query('name') ?? 'world'
    ctx.writeJson(200, {msg: 'hello ' + name})
})

srv.route('/api/user', ctx => {
    // ctx.method / ctx.path / ctx.querystr 是字段
    if ctx.method != 'POST' {
        ctx.write(405, 'method not allowed')
        return
    }
    body := @json.decode(ctx.getBodyStr())
    ctx.writeJson(200, {id: 1, name: body.name})
})

// 阻塞式启动；演示时放到后台任务
@concurrent.start(() => srv.serve('127.0.0.1:18142'))
@time.sleep('300ms')

println(@http.getText('http://127.0.0.1:18142/api/hello?name=zgg'))
println(@http.postJson('http://127.0.0.1:18142/api/user', {name: 'alice'}).len() > 0)
```

| 服务端方法 | 说明 |
|---|---|
| `route(path, handler)` | 注册 HTTP 路由 |
| `routeWebsocket(path, handler)` | 注册 WebSocket 路由 |
| `serve(addr[, options])` | 启动服务（阻塞）；`options` 支持 `certFile` / `keyFile` |
| `serveFS(addr[, dir[, urlPrefix]])` | 启动静态文件服务（带 gzip） |

### RequestContext

| 成员 | 类型 | 说明 |
|---|---|---|
| `method` | `Str` | 请求方法 |
| `path` | `Str` | 路径 |
| `querystr` | `Str` | 原始查询串 |
| `query(name)` | `Str` | 查询参数 |
| `queryAll(name)` | `Array` | 同名多值参数 |
| `form(name)` / `formAll(name)` | | 表单字段 |
| `file(name)` / `files()` | | 上传文件 |
| `parseMultipartForm(maxBytes)` | | 解析 multipart |
| `getBody()` | `Bytes` | 请求体 |
| `getBodyStr()` | `Str` | 请求体文本 |
| `getHeader(name)` / `getHeaders()` | | 请求头 |
| `cookie(name)` / `cookies()` | | Cookie |
| `setHeader(k, v)` / `addHeader(k, v)` | | 响应头 |
| `setCookie(k, v[, opts])` / `delCookie(k)` | | 响应 Cookie |
| `write(status[, body...])` | | 写响应 |
| `writeJson([status,] value)` | | 写 JSON 响应 |
| `sendFile(path)` | | 发送文件 |
| `redirect(url[, code])` | | 重定向 |
| `forward(target[, options])` | | 反向代理转发 |

### WebSocket 路由

```zgg
srv.routeWebsocket('/ws', ws => {
    for {
        msg := ws.read()
        if isUndefined(msg) {
            break
        }
        ws.write('echo:' + msg)
    }
})
```

WebSocket 上下文方法：`read` / `write` / `readJson` / `writeJson` / `close` / `header`。

## 完整示例：本地起服务并调用

```zgg
srv := @http.createServer()
srv.route('/hello', ctx => {
    ctx.writeJson(200, {msg: 'hello', path: ctx.path})
})

// serve 是阻塞的，放到后台任务
job := @concurrent.start(() => srv.serve('127.0.0.1:18080'))
@time.sleep('300ms')

println(@http.getText('http://127.0.0.1:18080/hello'))
```

## 静态文件服务

```text
// 一行启动：目录 . 映射到 /，带 gzip（会阻塞）
@http.serveFS('0.0.0.0:8080', './public', '/')
```

## 注意事项

- `serve` / `serveFS` 会阻塞当前流程；脚本里演示时放到 `@concurrent.start` 中。
- handler 中抛出的异常由框架捕获并记录，不会导致进程退出。
- `ctx.write` 的第一个参数是状态码；多次写会按顺序输出。
- 生产环境建议在前面加一层反向代理处理 TLS、限流与访问日志。
