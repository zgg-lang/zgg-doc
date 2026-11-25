# 快速上手

## 第一个程序

```zgg
println('Hello, ZGG!')
```

```bash
zgg hello.zgg
```

输出：

```text
Hello, ZGG!
```

## 基本构成

### 变量与类型

```zgg
name := 'ZGG'        // 声明（:=）
age := 5             // Int
version := 1.5       // Float
tags := ['lang', 'go']
info := {name: name, age: age}

age = age + 1        // 修改（=）
println('$name $age $version')   // ZGG 6 1.5
println(info)
```

### 函数

```zgg
func add(a, b) {
    return a + b
}

double := x => x * 2                 // 表达式箭头函数
show := (x) => { println(x) }        // 代码块箭头函数

println(add(1, 2), double(3))
show('hi')
```

### 控制流

```zgg
score := 85

if score >= 90 {
    println('A')
} else if score >= 60 {
    println('B')
} else {
    println('C')
}

println(when score {
    90..100 -> 'A'
    60..<90 -> 'B'
    else -> 'C'
})
```

### 容器操作

```zgg
nums := [1, 2, 3, 4, 5]

println(nums.map(v => v * v))                 // [1, 4, 9, 16, 25]
println(nums.filter(v => v % 2 == 1))         // [1, 3, 5]
println(nums.reduce((acc, v) => acc + v, 0))  // 15
println(nums[1:3])                            // [2, 3]
println([x * 2 for x in nums if x > 3])       // [8, 10]
```

### 对象与方法

```zgg
user := {
    name: 'alice',
    age: 30,
    greet() {
        return 'hi, ' + this.name
    },
}

println(user.greet())
println(user.keys())
```

### 类

```zgg
class Animal {
    __init__(name) {
        this.name = name
    }
    speak() {
        return this.name + ' makes a sound'
    }
}

class Dog(Animal) {
    speak() {
        return super.speak() + ': woof'
    }
}

println(Dog('wang').speak())
```

## 一段完整脚本：统计词频

把上面的能力组合起来：读文件 → 统计 → 终端表格 → 写 JSON。

```zgg
// 1. 准备输入
@file.rewrite('/tmp/zgg_demo.txt', 'alpha beta\nbeta gamma\ngamma gamma\n')

// 2. 统计词频
counter := {}
for line in @file.readLines('/tmp/zgg_demo.txt') {
    for w in line.split(' ') {
        word := w.trim()
        if word == '' {
            continue
        }
        counter[word] = (counter[word] ?? 0) + 1
    }
}

// 3. 排序（less 函数返回 true 表示排在前面）
rows := counter.pairs().map(p => ({word: p.key, count: p.value}))
rows.sort(r => r.count, true)

// 4. 输出表格
table := @ptable('word', 'count')
for r in rows {
    table.add(r.word, r.count)
}
println(table.txt())

// 5. 落盘为 JSON
@file.rewrite('/tmp/zgg_demo.json', @json.encode(rows))
println(@json.decode(@file.readString('/tmp/zgg_demo.json'))[0])
```

输出：

```text
+-------+-------+
| word  | count |
+-------+-------+
| gamma |     3 |
| beta  |     2 |
| alpha |     1 |
+-------+-------+
{word: gamma, count: 3}
```

> 对象的字段打印顺序不固定，上面只是其中一种输出。

## 调试建议

- 用 `println` / `printf` 打印中间值；`printf` 采用 Go 的格式化占位符（`%v`、`%d`、`%s`）。
- 出错时会打印 `Exception!` 与文件行号；`try/catch` 可以拿到 `e.message`。
- 想看某个值的类型：`typeName(v)`；判断类型：`v is Int`。
- 排查模块问题：先确认 `import` 路径（相对当前脚本目录），再用 `zgg showast` 看解析结果。

继续阅读：[语法总览](../syntax/README.md) →
