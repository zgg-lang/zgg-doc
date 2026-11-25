# xlsx 表格

基于 [excelize](https://github.com/xuri/excelize) 的 Excel 读写。

```zgg
x := @xlsx
```

## 打开已有文件

```zgg
f := @xlsx.open('/tmp/report.xlsx')

println(f.sheetCount())        // 工作表数量
println(f.sheetNames())        // ['Sheet1', ...]

// 全部按字符串读取
rows := f.sheetStrs(0)         // 也可传工作表名
println(rows)

// 读取并尽量保留类型（布尔会还原为 Bool）
values := f.sheetValues('Sheet1')
println(values)
```

| 方法 | 说明 |
|---|---|
| `open(path)` | 打开 Excel 文件 |
| `sheetCount()` | 工作表数量 |
| `sheetNames()` | 工作表名数组 |
| `sheetStrs(sheet)` | 按字符串读取，`sheet` 可为名字或下标 |
| `sheetValues(sheet)` | 按类型读取（数字可能仍是字符串，需要时用 `int()` / `float()`） |
| `save(path)` | 另存为 |

## 从 PTable 生成

最常用的写法：先组织数据为 `PTable`，再一次性导出。

```zgg
t := @ptable('name', 'age', 'ok')
t.add('alice', 30, true)
t.add('bob', 20, false)

f := @xlsx.File(t)          // 以 PTable 初始化新工作簿
println(f.sheetNames())     // [Sheet1]
f.save('/tmp/report.xlsx')
```

## 从数据库导出

```zgg
db := @db.open('sqlite', 'file:/tmp/xlsx_demo.db')
db.execute('drop table if exists user')
db.execute('create table user(id integer primary key, name text)')
db.execute('insert into user(id, name) values(1, ?)', 'alice')

table := db.m('user').toTable()        // ActiveRecord → PTable
@xlsx.File(table).save('/tmp/users.xlsx')
println(@xlsx.open('/tmp/users.xlsx').sheetStrs(0))
```

## 读取后转表格展示

```zgg
f := @xlsx.open('/tmp/report.xlsx')
rows := f.sheetStrs(0)

t := @ptable()
for row in rows {
    t.addArray([row])
}
println(t.txt())
```

## 注意

- 新工作簿默认只有 `Sheet1`，写入数据时从第 0 行第 0 列开始。
- 读取数字单元格时，excelize 可能返回字符串（取决于单元格类型），计算前请显式 `int()` / `float()`。
- 大文件（几十万行）建议分页处理，避免一次性读入内存。
