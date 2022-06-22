# ZGG内置标准库 - json

json提供了JSON操作相关的函数

## 函数目录

* [func encode()](#random0)
* [func decode()](#random1)
* [func format()](#random2)
* [func find()](#random2)

## 函数详解

### <div id="encode">func encode(value, indent?)</div>
将***value***序列化为json字符串，返回Str

***indent***如果不缺省，序列化结果会带上换行和缩进，以更可读的形式生成。其中：
* 当indent为Int时：每一个层级前面加上层级数乘以indent个空格作为缩进
* 当indent为Str时：每一个层架前面加上层级数乘以indent字符串作为缩进

### <div id="decode">func decode(strOrBytes)</div>
解析json字符串，返回解析出来的zgg value，是encode的逆操作

### <div id="format">func format(strOrBytes, indent?)</div>
将json字符串以指定形式重新格式化（以提高可读性）。format(a, b)实际上是```encode(decode(a), b)```的简化形式

### <div id="find">func find(jsonpath, value)</div>
通过jsonpath，获取value的指定字段内容

***注：当传入value类型为Str或者Bytes时，find函数会先对value进行json.decode操作，即
```
s := '{"a":1}'
//以下两行是等价的
@json.find('$.a', s)
@json.find('$.a', @json.decode(s))
```
***

具体jsonpath的语法，请参考[github.com/oliveagle/jsonpath](https://pkg.go.dev/github.com/oliveagle/jsonpath@v0.0.0-20180606110733-2e52cf6e6852)
