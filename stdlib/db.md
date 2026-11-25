# db 数据库

支持 SQLite 与 MySQL（驱动在启动时注册）。

## 连接

```zgg
// 方式一：DSN
db := @db.open('sqlite', 'file:/tmp/app.db')
// MySQL:
// db := @db.open('mysql', 'user:pass@tcp(127.0.0.1:3306)/test')

// 方式二：URL 形式
// db := @db.open('mysql://user:pass@127.0.0.1:3306/test')
```

> SQLite 驱动名是 `sqlite`（`github.com/glebarez/go-sqlite`，纯 Go，无需 CGO）。

## 直接执行 SQL

```zgg
db := @db.open('sqlite', 'file:/tmp/db_demo.db')
db.execute('create table if not exists user(id integer primary key autoincrement, name text, age int)')

res := db.execute('insert into user(name, age) values(?, ?)', 'alice', 30)
println(res)      // {affected: 1, lastInsertID: 1}

r := db.query('select id, name, age from user where age > ?', 18)
println(r.all())  // [{id: 1, name: alice, age: 30}, ...]
```

| Database 方法 | 说明 |
|---|---|
| `query(sql, args...)` | 查询，返回 `QueryResult` |
| `execute(sql, args...)` | 执行，返回 `{affected, lastInsertID}` |
| `m(table)` | 获取表的 ActiveRecord |
| `atom(fn)` | 事务内执行（异常回滚） |
| `newSession()` | 新事务会话，手动 `commit` / `rollback` |
| `tables()` | 列出表（MySQL 方言） |
| `close()` | 关闭连接 |

## QueryResult

| 方法 | 说明 |
|---|---|
| `all()` | 全部行（对象数组） |
| `allArray()` | 全部行（数组的数组） |
| `allOne()` | 首行首列的值 |
| `next()` | 下一行（对象），结束返回 `nil` |
| `nextArray()` | 下一行（数组） |
| `nextOne()` | 下一行首列 |
| `each(fn)` | 逐行回调 |
| `toTable()` | 转成 `PTable` |
| `close()` | 关闭结果集 |

```zgg
db := @db.open('sqlite', 'file:/tmp/db_demo.db')
r := db.query('select 1 as a, 2 as b')
println(r.next())     // {a: 1, b: 2}
println(r.next())     // nil
```

> 结果集是**一次性**的：`all()` 之后不能再 `allOne()` / `next()`（会报 `Rows are closed`）。

## ActiveRecord

```zgg
db := @db.open('sqlite', 'file:/tmp/db_demo2.db')
db.execute('drop table if exists user')
db.execute('create table user(id integer primary key autoincrement, name text, age int)')
users := db.m('user')

users.add({name: 'alice', age: 30}, {name: 'bob', age: 20})   // 支持多行
println(len(users.all()))

// 注意：查询过的 ActiveRecord 不要再复用，重新 db.m() 取一个
println(db.m('user').and({name: 'alice'}).one())
println(db.m('user').and({name: 'bob'}).update({age: 21}))    // 返回受影响行数
println(db.m('user').asc('age').limit(1).all())
println(db.m('user').and({name: 'alice'}).findOne())
println(db.m('user').find('name'))
println(db.m('user').toTable().toArray(true))
```

| 方法 | 说明 |
|---|---|
| `add(obj...)` | 插入一行或多行 |
| `find(fields...)` / `all()` | 查询（返回对象数组）；`fields` 是投影列 |
| `findOne(fields...)` / `one()` | 查询单条（首行）；`fields` 是投影列 |
| `and(obj)` | 追加等值条件 |
| `asc(field)` / `desc(field)` | 排序 |
| `limit(n)` / `offset(n)` | 分页 |
| `update(obj)` | 按当前条件更新，返回受影响行数 |
| `count(field?)` | 聚合（见下） |
| `toTable()` | 转 `PTable` |
| `showSql(bool)` | 打印生成的 SQL |

### count 的正确用法

`count()` 在实现上会把参数拼进 `SELECT <field>` 并取首行首列：

- `count()` 默认参数是 `(1)`，所以**总是返回 1**，不是行数。
- 要统计行数请用 `count('count(1)')` 或 `len(...all())`。

```zgg
db := @db.open('sqlite', 'file:/tmp/db_demo3.db')
db.execute('drop table if exists user')
db.execute('create table user(id integer primary key autoincrement, name text, age int)')
db.m('user').add({name: 'alice', age: 30}, {name: 'bob', age: 20})

println(len(db.m('user').all()))          // 推荐
println(db.m('user').count('count(1)'))   // 也可以
```

## 事务

```zgg
db := @db.open('sqlite', 'file:/tmp/db_demo4.db')
db.execute('drop table if exists user')
db.execute('create table user(id integer primary key autoincrement, name text, age int)')

// 自动提交/回滚
db.atom(() => {
    db.m('user').add({name: 'carol', age: 40})
    db.m('user').add({name: 'dave', age: 50})
})

// 手动控制
s := db.newSession()
s.m('user').add({name: 'eve', age: 60})
s.commit()      // 或 s.rollback()
```

## 类型映射

| 数据库 | ZGG |
|---|---|
| INTEGER | `Int` |
| REAL / FLOAT | `Float` |
| TEXT | `Str` |
| BOOLEAN | `Bool` |
| NULL | `nil` |
| DATETIME | `@time` 的 `Time` 对象 |

## 注意

- 表名/字段名在 SQLite 下也用反引号包裹（MySQL 方言），SQLite 兼容。
- `db.tables()` 生成的是 MySQL 方言 SQL，SQLite 下会报语法错误。
- 连接是全局的，长驻服务记得在退出时 `close()`。
