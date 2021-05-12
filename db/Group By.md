# Group By
SQLite 的 GROUP BY 子句用于与 SELECT 语句一起使用，来对相同的数据进行分组。
在 SELECT 语句中，GROUP BY 子句放在 WHERE 子句之后，放在 ORDER BY 子句之前。

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

如果你想要查找薪水按照名字分组
``` 
val List = mDBImpl.table.selector(COMPANY::class) {
                select(listOf("SALARY"))
            }
                    .groupBy("Name") { build() }
                    .findAll()
```
结果如下
```
  NAME       SALARY
 ----------  ----------
Paul          20000.0
Allen         15000.0
Teddy         20000.0
Mark          65000.0
David         85000.0
Kim           45000.0
James         10000.0
```
类比SQL语句
`SELECT SALARY FROM COMPANY GROUP BY NAME`