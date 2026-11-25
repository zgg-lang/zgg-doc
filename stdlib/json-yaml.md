# json 与 yaml

## json

```zgg
j := @json
```

| 方法 | 说明 |
|---|---|
| `encode(value[, indent])` | 序列化为 JSON 字符串；`indent` 可为整数空格数或字符串 |
| `decode(strOrBytes)` | 解析 JSON；数字按整数/浮点还原，`null` → `nil` |
| `format(jsonStr[, indent])` | 重新格式化（美化）JSON 文本 |
| `find(jsonpath, value)` | 按 JSONPath 取值（注意 **path 在前**） |

### 编码

```zgg
println(@json.encode({b: 1, a: [1, 2]}))
// {"a":[1,2],"b":1}

println(@json.encode({b: 1, a: [1, 2]}, 2))
// {
//   "a": [
//     1,
//     2
//   ],
//   "b": 1
// }
```

- 对象的键按字典序输出，结果稳定。
- 输出末尾带一个换行（来自 Go 的 `json.Encoder`），拼接时可用 `.trim()`。

### 解码

```zgg
v := @json.decode('{"i": 1, "f": 1.5, "ok": true, "n": null, "a": [1, 2]}')
println(v.i, typeName(v.i))      // 1 <type Int>
println(v.f, typeName(v.f))      // 1.5 <type Float>
println(v.ok, v.n)               // true nil
```

也接受 `Bytes`（例如 `@http.get` 的返回值）：

```text
// 读取远程 JSON
data := @http.get('https://example.com/api')!
obj := @json.decode(data)
```

### JSONPath 查询

```zgg
data := {a: {b: [10, 20]}}
println(@json.find(r'$.a.b[1]', data))     // 20
```

> `find(path, value)` 的参数顺序是"路径在前"；内置函数 `lookup(value, path)` 则相反（值在前）。路径里含 `$`，记得用 `r'...'`。

## yaml

```zgg
y := @yaml.encode({name: 'zgg', list: [1, 2]})
println(y)

obj := @yaml.decode(y)
println(obj.name, obj.list)
```

| 方法 | 说明 |
|---|---|
| `encode(value)` | 序列化为 YAML |
| `decode(str)` | 解析 YAML |

适用场景：配置文件、K8s 清单、CI 配置读写。

## 与 HTTP 配合

```text
// 读取远程 JSON
conf := @json.decode(@http.getText('https://example.com/conf.json'))
```
