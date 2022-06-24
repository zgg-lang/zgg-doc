# ZGG的数组

ZGG语言提供了强大的数组功能。数组，可以定义为**有限个值的有序集合**

## 数组的声明与访问

数组声明方法：
```
[item0, item1, ...]
```
每个item是一个表达式，数组保存的是表达式计算后得到的值。下标从0开始

访问数组指定下标的元素的语法为：
```
arr[index]
```

## 数组的运算

### 加法

若干个数组相加，将返回一个新的数组，其内容为各个参与相加的数组的依次拼接
```
zgg> [1, 2, 3] + [4, 5, 6] + [7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```
### 乘法

数组支持乘以一个大于等于0的整数，其作用为将其重复若干遍。如：
```
zgg> [1, 2, 3] * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
zgg> [1, 2, 3] * 0
[]
```

***注：乘以0的时候，即重复0遍，必然返回空数组***

### 数组推导式

ZGG支持通过类似Python的数组推导式生成新的数组。

以下是一些常见的数组推导式用法：
```
zgg> a := [1, 2, 3, 4, 5, 6]
[1, 2, 3, 4, 5, 6]

zgg> [item * item for item in a]
[1, 4, 9, 16, 25, 36]

zgg> [item * 2 for item in a if item % 2 == 0]
[4, 8, 12]

zgg> [v * 2 for v in 2..10] // 2..10在for..in里面相当于[2, 3, 4, 5, 6, 7, 8, 9, 10]，但不需要创建一个临时数组，效率更高
[4, 6, 8, 10, 12, 14, 16, 18, 20]

zgg> [v * 2 for v in 2..<10] // 2..<10在for..in里面相当于[2, 3, 4, 5, 6, 7, 8, 9]，但不需要创建一个临时数组，效率更高
[4, 6, 8, 10, 12, 14, 16, 18]

zgg> [v * 2 for v in 10]  // for .. in 10是for .. in 0..<10的简化写法
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

## 数组的内置方法

为了提高工作效率，ZGG内置了大量实用的数组方法

| 方法名 | 作用 |
|-------|------|
| [map](#map ) | |
| [filter](#filter ) | |
| [reduce](#reduce ) | |
| [each](#each ) | |
| [push](#push ) | 往数组末尾添加元素 |
| [slice](#slice ) | 获取数组切片 |
| [sort](#sort ) | 原地排序 |
| [join](#join ) | 将数组各元素依次拼接为一个字符串 |
| [toMap](#toMap ) | 将数组元素转为一个Map |
| [toGroup](#toGroup ) | 将数组元素按自定义key分组 |
| [chunk](#chunk ) | 将数组元素按顺序分组 |
| [find](#find  )  | 查找数组中出现的第一个符合预期的元素,找不到则返回undefined |
| [findIndex](#findIndex  )  | 查找数组中出现的第一个符合预期的元素的下标,找不到则返回-1 |
| [times](#times  )  | // |

## 生成数组的内建函数
| 函数名 | 作用 |
|-------|------|
| [seq(a, b)](#seq) | 返回从a到b的数组。如：seq(1, 5)返回[1, 2, 3, 4, 5]。更多用法请看下面的详解 |
| [range(end)](#range1) | 具体用法见详解|
| [range(begin, end)](#range2) | 具体用法见详解|
| [range(begin, end, step)](#range3) | 具体用法见详解|

## 函数详解

### <div id="map">Array.map(mapper)</div>
将数组每个元素根据mapper映射到指定形式，存放到新的数组中并返回。原数组内容不变

mapper支持多种不同类型：

| mapper类型 | 映射结果 |
|-----------|----|
| 任意可执行对象 | mapper(item, index) |
| Int或Str | item[mapper] |

#### Examples:
```
zgg> [1, 2, 3].map(v => v * v)
[1, 4, 9]
zgg> [{x: 1}, {x: 2}, {x: 3}].map('x')
[1, 2, 3]
zgg> [{x: 1}, {x: 2}, {x: 3}].map('y')
[undefined, undefined, undefined]
zgg> [[1, 2, 3], [2, 3, 4], [3, 4, 5]].map(1)
[2, 3, 4]
```

### <div id="filter">Array.filter(filterFunc)</div>
将原数组将符合条件的元素，依次放在新数组并返回。

符合条件的定义是：filterFunc(item, index)返回一个真值。真值的定义请看条件判断章节

#### Examples:
```
zgg> seq(1, 10).filter(v => v % 2 == 0)
[2, 4, 6, 8, 10]
```

### <div id="reduce">Array.reduce(reducer, initialValue?)</div>

reduce() 方法接收一个函数reducer作为累加器，数组中的每个值（从左到右）开始缩减，最终计算为一个值。

参数说明：
* reducer: 格式为：func(total, currenetValue, currentIndex, thisArray)。如果不设reduce，默认会把各个元素相加返回（即为数组求和）
* initialValue: 可选。传递给函数的初始total值

更多细节请看下面例子或参考Javascript里的表现。

#### Examples:
```
zgg> seq(1, 10).reduce() // 不传reducer，默认为求和
55

zgg> seq('a', 'g').reduce() // 字符串的求和，即依次拼接
abcdefg

zgg> seq(1, 10).reduce((total, cur) => total + cur)
55

zgg> seq(1, 10).reduce((total, cur) => total + cur ** 2)
385

zgg> seq(1, 10).reduce((total, cur) => total + cur ** 2, 0)
385

zgg> seq(1, 10).reduce((total, cur) => total + cur ** 2, 100)
485

zgg> // 当没有传入initialValue时，第一次执行的total为array[0]，cur为array[1]
zgg> seq(1, 5).reduce((total, cur) => {
....   println('total is $total, cur is $cur')
....   return total + cur
.... })
total is 1, cur is 2
total is 3, cur is 3
total is 6, cur is 4
total is 10, cur is 5
15

zgg> // 当有传入initialValue时，第一次执行的total为initialValue，cur为array[0]
zgg> seq(1, 5).reduce((total, cur) => {
....   println('total is $total, cur is $cur')
....   return total + cur
.... }, 0)
total is 0, cur is 1
total is 1, cur is 2
total is 3, cur is 3
total is 6, cur is 4
total is 10, cur is 5
15
```
### <div id="each">Array.each(callback)</div>
依次取数组元素，调用callback函数。以下两段代码时等价的：
```
arr.each(callback)
```
与
```
for index, value in arr {
    callback(value, index)
}
```

### <div id="toMap">Array.toMap(keyMapper?, valueMapper?)</div>

根据数组内的元素，生成一个Object对象，其键名为数组元素被keyMapper映射后的结果，键值为元素被valueMapper映射后的结果。

注：
* mapper的映射规则，请参考数组的map方法
* keyMapper和valueMapper都可以缺省，缺省时映射结果为元素本身
* 如果多个元素映射的键名相同，将保留最后一个元素映射的键值

#### Examples:
```
zgg> items := [{value} for value in 1..10]
[{value: 1}, {value: 2}, {value: 3}, {value: 4}, {value: 5}, {value: 6}, {value: 7}, {value: 8}, {value: 9}, {value: 10}]

zgg> items.toMap(item => item.value % 3)
{
    1: {value: 10},
    2: {value: 8},
    0: {value: 9}
}

zgg> items.toMap(item => item.value % 3, 'value')
{1: 10, 2: 8, 0: 9}

zgg> items.toMap('value')
{
    7: {value: 7},
    9: {value: 9},
    10: {value: 10},
    1: {value: 1},
    3: {value: 3},
    6: {value: 6},
    8: {value: 8},
    2: {value: 2},
    4: {value: 4},
    5: {value: 5}
}
```

### <div id="toGroup">Array.toGroup(keyMapper?, valueMapper?)</div>

根据key分组。根据数组内的元素，生成一个Object对象，其键名为数组元素被keyMapper映射后的结果，键值为“所有映射到该键名的元素被valueMapper映射后的结果”的数组。

注：
* mapper的映射规则，请参考数组的map方法
* keyMapper和valueMapper都可以缺省，缺省时映射结果为元素本身
* 同一分组元素顺序，为这些元素在原数组的顺序

#### Examples:
````
zgg> items := [{value} for value in 1..10]
[{value: 1}, {value: 2}, {value: 3}, {value: 4}, {value: 5}, {value: 6}, {value: 7}, {value: 8}, {value: 9}, {value: 10}]

zgg> items.toGroup(item => item.value % 3)
{
    0: [{value: 3}, {value: 6}, {value: 9}],
    1: [{value: 1}, {value: 4}, {value: 7}, {value: 10}],
    2: [{value: 2}, {value: 5}, {value: 8}]
}
zgg> items.toGroup(item => item.value % 3, 'value')
{
    0: [3, 6, 9],
    1: [1, 4, 7, 10],
    2: [2, 5, 8]
}
````

### <div id="chunk">Array.chunk(chunkSize)</div>
将数据元素按固定大小分段

#### Examples:
```
zgg> seq(1, 10).chunk(4)
[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

### <div id="find">Array.find(predict)</div>
找到第一个符合predict的元素并返回。当找不到符合元素时返回undefined

符合条件的定义是：
* predict若为可执行对象：predict(item)返回真值
* 否则: item == predict

#### Examples:
```
zgg> seq(1, 10).find(4)
4
zgg> seq(1, 10).find(20)
undefined
```

### <div id="findIndex">Array.findIndex(predict)</div>
与find相似，区别在于findIndex返回的是元素的下标，找不到的时候返回-1

#### Examples:
```
zgg> seq(1, 10).findIndex(4)
3
zgg> seq(1, 10).findIndex(20)
-1
```

### <div id="seq">func seq(a, b)</div>
生成从a到b的数组。这里的a和b的类型不仅局限于Int，还支持所有实现了__next__协议和__eq__协议的对象。

### <div id="range1">func range(end)</div>
#### Example:
```
zgg> range(5)
[0, 1, 2, 3, 4]
```

### <div id="range2">func range(begin, end)</div>
#### Example:
```
zgg> range(2, 5)
[2, 3, 4]
```
### <div id="range3">func range(begin, end, step)</div>
#### Example:
```
zgg> range(2, 10, 3)
[2, 5, 8]
```