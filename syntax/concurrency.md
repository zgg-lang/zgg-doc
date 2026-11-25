# 并发编程

ZGG 的并发基于 Go goroutine：`@concurrent` 提供 future、并发映射、通道与互斥量。

## start：启动一个任务

```zgg
job := @concurrent.start(() => {
    @time.sleep('100ms')
    return 'done'
})

println('waiting...')
println(job.await())      // done
```

返回的 future 支持：

| 方法 | 说明 |
|---|---|
| `await()` | 等待并取回结果（可多次调用，返回缓存结果） |
| `join()` | 同上 |
| `cancel()` / `detech()` | 取消 / 分离（不阻塞主流程） |

## all：并发执行多个任务

参数是多个可调用值，按顺序返回结果数组：

```zgg
println(@concurrent.all(
    () => 1,
    () => 2,
    () => 3,
))       // [1, 2, 3]
```

## map：并发映射

参数是一个**可调用值数组**，可选最大并发数：

```zgg
println(@concurrent.map([() => 1, () => 2, () => 3]))        // [1, 2, 3]
println(@concurrent.map([() => 'a', () => 'b'], 2))          // [a, b]
```

如果要并发处理一个数据数组，先 map 成可调用值：

```zgg
urls := ['https://example.com', 'https://example.org']
futures := urls.map(u => @concurrent.start(() => @http.getText(u)))
println(futures.map(f => len(f.await())))
```

## Chan：通道

```zgg
ch := @concurrent.Chan(1)     // 参数是缓冲大小
ch.send('hello')
println(ch.recv())            // hello
```

生产者/消费者：

```zgg
ch := @concurrent.Chan(2)

producer := @concurrent.start(() => {
    for i in 1..3 {
        ch.send(i)
    }
})

consumer := @concurrent.start(() => {
    sum := 0
    for i in 3 {
        sum += ch.recv()
    }
    return sum
})

producer.await()
println(consumer.await())     // 6
```

## Mutex：互斥量

```zgg
m := @concurrent.Mutex()
println(m.run(() => 42))      // 自动加锁/解锁

m.lock()
// 临界区
m.unlock()
```

## Limiter：并发限流

```zgg
limiter := @concurrent.Limiter(2)     // 最多 2 个并发
future := limiter.run(() => 'ok')
println(future.await())               // ok
limiter.wait()                        // 等待全部完成
```

## 共享状态要加锁

ZGG 的并发**没有内存隔离**：多个任务共享同一个对象，`+=` 这类读改写不是原子的。

```zgg
m := @concurrent.Mutex()
shared := {n: 0}

workers := range(4).map(_ => @concurrent.start(() => {
    for i in 100000 {
        m.run(() => {
            shared.n += 1
        })
    }
}))

for w in workers {
    w.await()
}
println(shared.n)     // 400000
```

如果不加锁，同样的代码会得到远小于 400000 的结果（典型的竞态丢更新）。

## 使用建议

- 通过 `Chan` 传递数据、尽量少共享可变对象。
- 必须共享时用 `Mutex.run(...)` 包住整个读改写。
- 任务里抛出的异常不会自动传到主流程，需要在任务内部 `try/catch`。
- `import` 的模块缓存是全局共享的，模块初始化代码要注意幂等。

继续阅读：[标准库总览](../stdlib/README.md) →
