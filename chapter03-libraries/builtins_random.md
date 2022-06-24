# ZGG内置标准库 - random

random提供了常用的随机数相关函数

## 函数目录

### 生成随机数

* [func random()](#random0)
* [func random(end)](#random1)
* [func random(begin, end)](#random2)

### 数组操作
* [func choice(array)](#choice)
* [func shuffle(array)](#shuffle)

## 函数详解

### <div id="random0">func random()</div>
返回一个取值范围在[0, 1)之前的浮点数

### <div id="random1">func random(end)</div>
返回一个取值范围在[0, end)之前的整数

### <div id="random2">func random(begin, end)</div>
返回一个取值范围在[begin, end)之间的整数，如果begin >= end，抛出异常

### <div id="choice">func choice(array)</div>
从array中等概率随机挑选一个元素

### <div id="shuffle">func shuffle(array)</div>
原地将array内元素次序打乱