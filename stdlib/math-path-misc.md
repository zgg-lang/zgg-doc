# math / path / random / psutil / fsnotify / ip2region

## math：数学

```zgg
m := @math
println(m.PI, m.E)
println(m.abs(-3), m.sqrt(9), m.floor(1.7), m.ceil(1.2), m.round(1.5))
println(m.sin(0), m.cos(0), m.tan(0))
println(m.log(m.E), m.log10(100), m.exp(0), m.pow(2, 10))
println(m.gcd(12, 18), m.lcm(4, 6))          // 6 12
println(m.P(5, 2), m.C(5, 2))                // 排列 20 / 组合 10
println(m.reduction(2, 3))                   // 约分 → [2, 3]
```

| 类别 | 函数 |
|---|---|
| 常量 | `PI` `E` |
| 基础 | `abs` `floor` `ceil` `round` `trunc` `sqrt` `pow` `hypot` |
| 三角 | `sin` `cos` `tan` `asin` `acos` `atan` `atan2` |
| 指数对数 | `exp` `log` `log10` |
| 整数 | `gcd` `lcm` `P` `C` `reduction` |
| 向量 | `Vec` 类（`__add__` / `__sub__` 等） |

## path：路径与遍历

```zgg
println(@path.join('/tmp', 'a', 'b.txt'))     // /tmp/a/b.txt
println(len(@path.glob('/tmp/*.txt')))         // 匹配数量

for item in @path.walk('/tmp/data') {
    println(item.path, item.isDir)
}

@path.walk('/tmp/data', item => {
    println('visit', item.name)
})
```

| 方法 | 说明 |
|---|---|
| `join(parts...)` | 拼接路径 |
| `glob(pattern)` | 通配符匹配，返回数组 |
| `walk(root)` | 惰性迭代（可 `for-in`），元素 `{path, name, isDir}` |
| `walk(root, callback)` | 遍历并回调 |

## random：随机

```zgg
println(@random.random())               // [0, 1) 浮点
println(@random.choice([1, 2, 3]))      // 随机取一个
arr := [1, 2, 3, 4, 5]
println(@random.shuffle(arr))           // 原地洗牌并返回
```

## psutil：系统指标

```zgg
println(@psutil.cpu.logicalCount, @psutil.cpu.physicalCount)
// cpu.percent 在部分平台/版本上可能返回 not implemented
```

## fsnotify：文件监听

```text
watcher := @fsnotify.watch('/tmp/data')
for ev in watcher {
    println(ev.name, ev.op)
}
```

（监听对象可迭代，事件含 `name` 与 `op`。）

## ip2region：IP 归属地

```text
searcher := @ip2region.Searcher('/path/to/ip2region.xdb')
info := searcher.search('8.8.8.8')
println(info.country, info.province, info.city, info.carrier)
```

需要自备 ip2region 数据文件。
