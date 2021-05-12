# 1. WHERE条件语句
SQLite的WHERE子句用于指定一个表或者多个表中获取数据的条件
如果满足给定的条件，即为真，则从表中返回特定的值，您可以使用WHERE子句来过滤记录，只获取需要的记录。WHERE子句不仅可在SELECT语句中，它也可以用在UPDATE，DELETE语句中。

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

## 1.2. AND运算符
AND运算符允许在一个 SQL 语句的 WHERE 子句中的多个条件的存在,使用 AND 运算符时，只有当所有条件都为真（true）时，整个条件为真（true）
下面的例子是请求 AGE 大于等于 25 且工资大于等于 65000.00 的所有记录
在框架中我们应该这么做
```
mDBImpl.table.update(COMPANY::class,Pair("age","28")){
                and("AGE", ">=", "25")
                and("SALARY", ">=", "65000")
            }
```
查询出来的结果
```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
```

AND的参数解析
```
* @param columnName 表中的字段名称
* @param op 操作符号
* @param value column具体的值
```
类比SQL语句
`SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000`
## 1.3. OR运算符
OR 运算符也用于结合一个 SQL 语句的 WHERE 子句中的多个条件。使用 OR 运算符时，只要当条件中任何一个为真（true）时，整个条件为真（true）。
下面的例子是请求 AGE 大于等于 25 或工资大于等于 65000.00 的所有记录
在框架中我们应该这么做
```
mDBImpl.table.update(COMPANY::class,Pair("age","28")){
                or("AGE", ">=", "25")
                or("SALARY", ">=", "65000")
            }
```
查询出来的结果

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0

```

OR的参数解析
```
* @param columnName 表中的字段名称
* @param op 操作符号
* @param value column具体的值
```
类比SQL语句
`SELECT * FROM COMPANY WHERE AGE >= 25 OR SALARY >= 65000;`
# 2 op 操作符号
`OR`和`AND`都需要` op `操作符配合完成查询
* 1. <> 不等于
* 2. &gt; 大于
* 3. <  小于
* 4. &gt;= 大于等于 />
* 5. <= 小于等于
* 6. BETWEEN 在范围之间,**直接使用BETWEEN，不要带AND**
* 7. LIKE 搜索,like可使用通配符( _ 只有一个)（ %或者* 任意多个），例如LIKE '_K%'代表第二个字母是K的
* 8. IS NOT NULL 不为空
* 9. IS NULL 为空
* 10. IN () 在例举之中
* 11. NOT IN () 不在例举之中**不支持NOT IN**
