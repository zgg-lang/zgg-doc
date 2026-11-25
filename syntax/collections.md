# 数组与对象

## 数组

### 字面量与基本操作

```zgg
arr := [1, 2, 3]
println(arr[0], arr[-1])      // 1 3
println(arr[1:3])             // [2, 3]
println(len(arr))             // 3

arr[1] = 20
arr.push(4)
println(arr)                  // [1, 20, 3, 4]
```

- 下标支持负数（从尾部计数）；越界返回 `undefined`，不报错。
- `push(...)` 原地追加，返回追加的元素个数。
- `[1] + [2]` 拼接，`[1, 2] * 2` 重复。

### 展开与推导式

```zgg
base := [1, 2]
println([0, ...base, 3])                  // [0, 1, 2, 3]
println([x * 2 for x in 1..5 if x % 2 == 1])   // [2, 6, 10]
```

### 方法一览

| 方法 | 说明 |
|---|---|
| `map(fn)` | `fn(value, index)` → 新数组；也可传字段名 `map('name')` 或下标 `map(0)` |
| `filter(fn)` | `fn(value, index)` 返回真则保留 |
| `flatMap(fn)` | 映射后展平一层 |
| `filterMap(fn)` | `fn` 返回 `[value, accepted]`，accepted 为真才收集 |
| `reduce(fn, init?)` | `fn(acc, value)`；无 `init` 时用首元素作初值 |
| `sum(fn?)` | 求和，可先映射 |
| `each(fn)` | 遍历并执行副作用 |
| `push(v...)` | 追加，返回追加数量 |
| `slice(begin?, end?)` | 子数组，支持负数 |
| `sort(keyFn?, reverse?)` | 按 `keyFn(value)` 排序（原地），`reverse=true` 降序 |
| `join(sep?)` | 拼接为字符串，默认空格 |
| `toMap(keyFn?, valFn?)` | 转对象，默认用下标作 key |
| `count(keyFn?)` | 无参按值计数；有参按键计数 |
| `countIf(fn)` | 满足条件的元素个数 |
| `toGroup(keyFn)` | 按键分组为 `{key: [values]}` |
| `uniq(keyFn?)` | 去重 |
| `chunk(n)` | 每 n 个切一块 |
| `find(fn, start?)` / `findIndex(fn, start?)` | 查找值 / 下标 |
| `groupBy(keyFn...)` | 分组，返回分组后的数组 |
| `reverse()` | 原地反转 |

```zgg
nums := [3, 1, 2]
println(nums.map(v => v * 2))               // [6, 2, 4]
println(nums.filter(v => v > 1))            // [3, 2]
println(nums.reduce((acc, v) => acc + v, 10))  // 16
println(nums.sort(v => v))                  // [1, 2, 3]
println(nums.sort(v => v, true))            // [3, 2, 1]
println([1, 2, 3].join('-'))                // 1-2-3
println([1, 2, 2, 3].uniq())                // [1, 2, 3]
println([1, 2, 3, 4, 5].chunk(2))           // [[1, 2], [3, 4], [5]]
println([1, 2, 3].count())                  // {1: 1, 2: 1, 3: 1}
```

> `sort` 的第一个参数是**取键函数**（单参数），不是比较器。排序对象时写 `rows.sort(r => r.count, true)`。

## 对象

### 字面量

```zgg
name := 'zgg'
user := {
    name,                       // 简写：等价于 name: name
    age: 5,
    ['k' + 1]: 'computed',      // 计算键
    greet() {                   // 方法简写
        return 'hi, ' + this.name
    },
}
println(user.name, user.k1, user.greet())
```

- 键可以是标识符、字符串字面量或 `[表达式]`。
- 支持展开：`{...base, b: 2}`（后者覆盖同名键）。
- 对象方法内的 `this` 指向对象本身。

### 访问与遍历

```zgg
u := {a: 1, b: 2}
println(u.a, u['a'])        // 1 1
println(len(u))             // 2
println('a' in u)           // true
println(u.keys())           // [a, b]（顺序不保证）
println(u.values())         // [1, 2]
println(u.pairs())          // [{key: a, value: 1}, ...]
u.each((k, v) => println(k, v))
```

> ⚠️ 对象底层是哈希表，`keys()` / `values()` / `pairs()` / `each()` 的遍历顺序**不稳定**。需要固定顺序时请显式排序，例如 `u.keys().sort(k => k)`。

### 对象与类

对象是类的实例。普通字面量对象的类型是 `Object`，也可以通过类构造：

```zgg
class Point {
    __init__(x, y) {
        this.x = x
        this.y = y
    }
    __getItem__(i) {
        return i == 0 ? this.x : this.y
    }
    __str__() {
        return 'Point(${this.x}, ${this.y})'
    }
}
p := Point(3, 4)
println(p[0], p[1])     // 3 4
println(p)              // Point(3, 4)
```

### 结构相等

```zgg
println({a: 1} == {a: 1})     // true
println([1, [2]] == [1, [2]]) // true
```

继续阅读：[控制流](control-flow.md) →
