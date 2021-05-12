# DB文档
Db数据库是为存储在SQLite中的数据提供面向对象的接口，你只需要创建Java数据对象即可为你创建对应的数据库，可以让你更容易的使用SQLite数据库，你不需要编写SQL语句就可以完成对数据库的操作。
<img src="../db/assest/DB图.png" width = 60% height = 60%/>
## 1. 快速集成
### 1.1. Gradle
 ```implementation "com.meili.moon.sdk:db:x.x.x" ```
### 1.2. 初始化
在application的onCreate()方法中进行初始化环境
```
class DemoApp : Application() {
    override fun onCreate() {
        super.onCreate()
        MoonDB.init(this)
    }
}
```
注：如果项目中引入了整体皓月库，则不需要在单独初始化。
## 2. 快速使用
### 2.1. 创建数据库
`val mDBImpl = DBImpl.getInstance(this)`
如果你要设置数据库的路径，自定义数据库的名称可以参考[配置](配置.md)
### 2.2. 创建表
#### 2.2.1. 创建存储对象实体类
使用皓月数据库存储数据，只需要在你存储的数据类前面声明@Table注解
```
@Table        
class Person {
    //id为主键
    @Column(isId = true)   
    var id: String = ""
    var name: String = ""
   }
```
更多注解[注解](注解.md)
#### 2.2.2 新建数据库表
声明完实体类之后，通过`save()`可以创建出数据库表同时保存一条数据。
```
val user = Person()
user.id = "1"
user.name = "mljr"
mDBImpl.table.save(user)
```
这样一个Person的表就新建起来了。
创建之后格式是这样的 
```
 ID          NAME       
----------  ----------  
1            mljr
```
#### 2.2.3. 添加数据
上面我们通过`save()`创建出来数据库表的同时添加了一条数据，如果我们想要继续添加数据，可以继续调用`save()`
 ```
val user = Person()
            user.idd = "2"
            user.name = "Paul"
             mDBImpl.table.save(user)
val user = Person()
            user.id = "3"
            user.name = "Allen"
            mDBImpl.table.save(user)
 ```
 使用上面的语句之后将在Person表中创建两个记录
```
 ID          NAME       
----------  ---------- 
1           mljr
2           Paul        
3           Allen      
```
### 2.3. 更新数据 
#### 3.3.1 `save()`方式更新
`save()`不仅能添加数据，可以用来更新一个实体，如果插入主键在数据库已经存在的数据，即视为更新这条数据。
下面的语句是更新`id=2`的人员的名字为`Peter`
```
val user = Person()
            user.id = "2"
            user.name = "Peter"
            mDBImpl.table.save(user)
```
使用上面的语句之后将在Person表中更新一个记录
```
 ID          NAME        
----------  ----------  
1           Paul        
2           Peter
3           Allen       
```
添加和更新数据的规则是
##### 1. 如果实体类的主键不为空的情况下
*   如果已经存在，则进行数据更新
*   如果不存在，则进行数据插入

##### 2.如果实体类的主键为空的情况下
*   如果id为自增长，插入数据后，赋值id到entity中
*   如果id不是自增长，则插入失败

注： **id**要为Long类型

#### 2.3.2. `Update()`方式更新
用Update()修改已有的记录，可以使用WHERE条件限定来查找选定行，否则所有的行都会被更新。例：
如果我们要将id为3的员工姓名更新为Kate
但是在框架中我们只要这么做就可以了
```
mDBImpl.table.update(Person::class,Pair("name","Kate")){
                and("id", "=", "3")
            }
```
更多筛选条件[where条件语句](WHERE条件语句.md)
如果更新某一个实体推荐使用`save()`
### 2.4. 查询
#### 2.4.1. 查询所有数据
```
val personList = mDBImpl.table.get(Person::class)
```
#### 2.4.2. 按照ID查询
```
val person = mDBImpl.table.get("3",Person::class)
```
#### 2.4.3. 按照条件查询
查找id等于1的人员
```
val person = mDBImpl.table.get(Person::class) {
                and("id", "=", "1")
            }
```
更多筛选[where条件语句](WHERE条件语句.md)
更多查询[高级查询](高级查询.md)
### 2.5. 删除数据
删除表中已有的数据，可以使用WHERE条件限定来删除选定行。
如果我们要删除id是1岁的用户,但是在框架中我们只要这么做就可以了
```
mDBImpl.table.delete(Person::class){
                and("id", "=", "1")
            }
```
更多筛选[where条件语句](WHERE条件语句.md)
### 2.6. 关闭数据库
```
mDBImpl.close()
```
### 2.7. 删除数据库
```
mDBImpl.dropDB()
```
### 2.8. 删除指定的表
```
mDBImpl.dropTable(PersonModel::class)
```


