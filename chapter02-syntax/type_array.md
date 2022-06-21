# ZGG的数组

ZGG语言提供了强大的数组功能。数组，可以定义为**有限个值的有序集合**

数组声明方法：
```
[item0, item1, ...]
```
每个item是一个表达式，数组保存的是表达式计算后得到的值

## 数组的运算

### 加法
### 乘法

数组支持乘以一个大于等于0的整数，其作用为将其重复若干遍。如：
```
zgg> [1, 2, 3] * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
zgg> [1, 2, 3] * 0
[]
```

***注：乘以0的时候，即重复0遍，必然返回空数组***

## 数组的内置方法

为了提高工作效率，ZGG内置了大量实用的数组方法

| 方法名 | 作用 |
|-------|------|
| map | |
| filter | |
| reduce | |
| each | |
| push | 往数组末尾添加元素 |
| slice | 获取数组切片 |
| sort | 原地排序 |
| join | 将数组各元素依次拼接为一个字符串 |
| toMap | 将数组元素转为一个Map |
| toGroup | 将数组元素分组 |
| find  | 查找数组中出现的第一个符合预期的元素 |
| findIndex  | 查找数组中出现的第一个符合预期的元素的下标 |
| times  | // |

### map(mapper)
### filter(filterFunc)
### reduce(reducer, initialValue?)
### each(callback)
### find(predict)
### findIndex(predict)