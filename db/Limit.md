# Limit 子句
SQLite 的 LIMIT 子句用于限制由 SELECT 语句返回的数据数量。 LIMIT 子句与 OFFSET 子句一起使用。

以下的查询都是基于 COMPANY 表有以下记录：

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

下面是一个实例，可能需要从一个特定的偏移开始提取记录，从第三位开始提取 3 个记录：

```
val selector = mDBImpl.table.selector(PersonModel::class) {
                limit = 3
                offset = 2
            }
            selector.findAll()
```

这将产生以下结果：

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
```

类比SQL语句
`SELECT * FROM COMPANY LIMIT 3 OFFSET 2;`