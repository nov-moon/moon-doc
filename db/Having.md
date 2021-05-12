# Having
HAVING 子句允许指定条件来过滤将出现在最终结果中的分组结果。
WHERE 子句在所选列上设置条件，而 HAVING 子句则在由 GROUP BY 子句创建的分组上设置条件。
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
下面是一个实例，它将显示名称等于kim的所有记录：
```
val List1 = mDBImpl.table.selector(PersonModel::class)
                    .groupBy("Name") {
                        having {
                            and("name", "=", "Kim")
                        }
                    }
                    .findAll()
```
这将产生以下结果：
```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
6           Kim         22          South-Hall  45000.0
```
类比 SQL 语句
`SELECT * FROM COMPANY GROUP BY name HAVING count(name) < 2;`