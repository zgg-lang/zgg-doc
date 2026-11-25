# time 时间处理

```zgg
t := @time
```

## 获取当前时间

| 写法 | 说明 |
|---|---|
| `@time.now()` | 当前时间 |
| `@time.now('day')` / `'hour'` / `'minute'` / `'second'` | 截断到对应精度 |
| `@time.today()` / `yesterday()` / `tomorrow()` | 今天/昨天/明天 00:00 |
| `@time.as('day')` / `'day'` 可带 offset | 当前时间按精度对齐，`offset` 为步数 |
| `@time.time()` | 当前 Unix 秒 |

```zgg
println(@time.now().format('%Y-%m-%d %H:%M:%S'))
println(@time.now('second').format('%H:%M:%S'))
println(@time.today().format('%Y-%m-%d'))
println(@time.time())
```

## 解析与转换

| 方法 | 说明 |
|---|---|
| `parse(str[, layout])` | 解析时间；不传 layout 时自动识别常见格式 |
| `parseIn(tz, str[, layout])` | 指定时区解析（`tz` 可为时区名或小时偏移） |
| `fromUnix(sec)` | 从 Unix 秒构造 |
| `fromUnixMs(ms)` | 从 Unix 毫秒构造 |
| `fromGoTime(goTime)` | 从 Go `time.Time` 构造 |

```zgg
t := @time.parse('2026-11-25 10:30:45')          // 自动识别
t2 := @time.parse('2026/11/25', '2006/01/02')    // Go layout
println(t.year, t.month, t.day, t.hour, t.minute, t.second)
println(@time.fromUnix(t.unix).format('%Y-%m-%d'))
println(@time.fromUnixMs(1795573845000).format('%Y-%m-%d %H:%M:%S'))
```

> `parse` 的 layout 是 **Go 风格**（`2006-01-02 15:04:05`），不是 `%Y`。
> 但 `format()` 同时支持 Go layout 和 `%Y-%m-%d %H:%M:%S` 这类写法。

## Time 对象

| 方法 / 字段 | 说明 |
|---|---|
| `format([layout][, timezone])` | 格式化，默认 `2006-01-02 15:04:05` |
| `add(duration)` | 加一个 `Duration` |
| `addDays(n)` / `addHours(n)` | 加减天 / 小时 |
| `as(kind)` | 截断到 `day`/`hour`/`minute`/`second` |
| `loc(tz)` | 转换时区（时区名或小时偏移） |
| `dayBegin(offset?)` / `weekBegin(offset?)` / `monthBegin(offset?)` / `yearBegin(offset?)` | 周期起点 |
| `timetuple()` | `[年, 月, 日, 时, 分, 秒, 时区]` |
| `unix` / `unixNano` | Unix 秒 / 纳秒 |
| `year` `month` `day` `hour` `minute` `second` `weekday` | 字段 |
| `toGoTime()` | 转 Go `time.Time` |
| 比较运算 | `< <= > >= == !=` |
| `Time` 之间可相减得到 `Duration` | |

```zgg
t := @time.parse('2026-11-25 10:30:45')
println(t.format('%Y-%m-%d'))
println(t.addDays(1).format('%Y-%m-%d'))
println(t.dayBegin().format('%H:%M:%S'))
println(t.monthBegin().format('%Y-%m-%d'))
println(t.weekBegin().format('%Y-%m-%d'))
println(t.timetuple())
println(t.loc('UTC').format('%H:%M'))
```

## Duration

```zgg
d := @time.Duration('1h30m')
println(d)                       // 1h30m0s
println(d + @time.Duration('30m'))   // 2h0m0s
println(d * 2)                   // 3h0m0s
println(d > @time.Duration('1h'))
```

支持单位：`ns` `us` `ms` `s` `m` `h`。

## 睡眠与计时

```zgg
@time.sleep('200ms')             // 接受 Duration 字符串

d := @time.timeit(() => {
    s := 0
    for i in 100000 {
        s += i
    }
})
println(d)                       // 例如 2.5ms
```

## 遍历时间区间

```zgg
begin := @time.parse('2026-11-01')
for d in @time.iter(begin, begin.addDays(3)) {
    println(d.format('%m-%d'))
}

list := @time.list(begin, begin.addDays(2))
println(list.map(d => d.format('%d')))
```

`iter(begin, end, step?)` 默认步长 1 天；`list` 直接返回数组。

## 时区

```zgg
@time.setDefaultTimezone('Asia/Shanghai')
println(@time.now().format('%Y-%m-%d %H:%M:%S'))
println(@time.now().loc(8).format('%H:%M'))    // 固定 +8
```

`setDefaultTimezone` 影响后续的 `now` / `today` / `parse` 的默认时区。

## 常见场景

```zgg
// 计算两个时间相差几天
a := @time.parse('2026-11-01')
b := @time.parse('2026-11-25')
days := int(b.unix - a.unix) / 86400
println(days)

// 生成最近 7 天的日期
for d in @time.iter(@time.today().addDays(-6), @time.today().addDays(1)) {
    println(d.format('%Y-%m-%d'))
}
```
