# Order By 子句
SQLite 的 ORDER BY 子句是用来基于一个或多个列按升序或降序顺序排列数据。您可以在 ORDER BY 子句中使用多个列。确保您使用的排序列在列清单中。

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
下面是一个实例，它会将结果按 SALARY 升序排序：
```
val List = mDBImpl.table.selector(COMPANY::class)
                    .orderBy(ISelector.OrderBy("SALARY", false))
                    .findAll()
```
这将产生以下结果：

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
7           James       24          Houston     10000.0
2           Allen       25          Texas       15000.0
1           Paul        32          California  20000.0
3           Teddy       23          Norway      20000.0
6           Kim         22          South-Hall  45000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
```

类比SQL语句
`SELECT * FROM COMPANY ORDER BY SALARY ASC;`