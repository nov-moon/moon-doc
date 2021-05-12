# Rainbow
Rainbow库是皓月中的**页面路由管理库**。取彩虹的优雅、连通、无限之意。

Rainbow库的功能开发参考了阿里和美团的路由库设计理念，再结合我们本身的业务特点和开发习惯进行了实现。Rainbow库的页面基于Fragment开发，提供了基于Fragment的页面跳转等路由操作。后续我们会考虑支持Activity的路由管理。

Rainbow库有如下特点：
1. 解耦页面间强依赖
2. 提供基础页面，便于快速开发
3. 支持滑动关闭
4. 支持打开页面在当前做回调处理
5. 支持以注解方式添加页面到路由
6. 支持路由拦截器
7. 支持自定义页面跳转处理
8. 支持页面动画自定义
9. 结合皓月，支持更多功能扩展

## 1. 快速集成
下述配置都在当前Module的**build.gradle**中完成。Rainbow使用了编译期注解处理，用来收集页面的注解信息，所以在添加库依赖的同时，需要配置注解处理器，如下：
``` groovy
// 第一步：添加Kapt插件，kotlin的官方插件
apply plugin: 'kotlin-kapt'

// 第二步：添加依赖
dependencies {
    // module的其他依赖项 ...
    // rainbow库依赖
    api "com.meili.moon.sdk:page-router:版本号"
    
    // 注解处理器依赖
    annotationProcessor "com.meili.moon.sdk:page-router-processor:版本号"
    kapt "com.meili.moon.sdk:page-router-processor:版本号"
}
```
---------------

## 2. 使用方式
Rainbow库的使用主要分三步：**初始化、页面开发、页面跳转**。
### 2.1. 初始化
**Rainbow**类提供了Rainbow库大部分Api的入口，包括初始化方法。
初始化方法只需要调用一次即可，一般在**Application**的**onCreate**方法中进行，如下：
``` kotlin
// 在Application的onCreate中进行Rainbow初始化
Rainbow.init(this)
```
> 初始化方法会将收集到的注解信息在Rainbow中进行注册，并做一些运行上下文环境的初始化

修改Application主题，将Application主题设置为继承自RainbowAppTheme主题。在RainbowAppTheme主题中，使用了无ActionBar的浅色模式，主要设置了window的半透明。使用方式如下：
``` xml
<style name="AppTheme" parent="RainbowAppTheme">
    // 其他主题的属性设置
</style>
```
> 如果不设置此主题，可能导致页面背景颜色错误等问题

### 2.2. 页面开发
* **继承RainbowFragment** Rainbow库要求注册管理的页面是**RainbowFragment**类型，所以你的业务页面都应该是**RainbowFragment**的子类，例如声明一个登陆页面：
``` kotlin
class LoginFragment : RainbowFragment() {}
```
> 一般情况下，你应该实现一个继承自**RainbowFragment**的自定义通用Fragment，例如**PageFragment**、**BaseFragment**等等，其他业务页面继承自定义的基类，方便进行页面的统一功能定制与扩展

* **PageName注解** 在完成页面的声明之后，给页面添加**PageName注解**，指定他的**PageName**，例如：
``` kotlin
@PageName("login")
class LoginFragment : RainbowFragment() {}
```
> 在Rainbow库中，每个页面的**PageName必须全局唯一**。PageName作为页面Id使用，表示唯一的一个页面，后续的页面跳转也会基于PageName跳转。
> **PageName**注解中的"login"就是当前页面的PageName，并且会自动在代码编译期，在**PageConfig**类中生成LOGIN常量，其值为：login。后续的页面跳转我们推荐使用PageConfig.LOGIN进行页面跳转。更多相关信息，请参考PageName章节

* **实现onPageCreated()** 在继承**RainbowFragment**时，必须实现其**onPageCreated()**方法，此方法相当于Activity的onCreate方法，一般在其中做一些页面初始化逻辑等内容，如下：
``` kotlin
@PageName("login")
class LoginFragment : RainbowFragment() {
    /**
     * 当页面已经创建 回调方法
     */
    override fun onPageCreated(view: View, savedInstanceState: Bundle?) {
        //  处理业务逻辑
    }
}
```

* **指定布局** 我们可以通过**Layout**注解，指定当前页面布局；也可以通过重写**getLayoutResId()**方法指定页面布局，如下：
``` kotlin
@PageName("login")
@Layout(R.layout.login_fragment)
class LoginFragment : RainbowFragment() {}
```

至此，我们就完成了一个页面的基本设置，并可以在其上开发业务逻辑了。

### 2.3. 页面跳转
我们继续使用上面Login的例子。在上面注解章节中我们已经添加了**PageName注解**，框架将根据注解自动在**PageConfig**类中生成**LOGIN**常量，用做跳转LoginFragment的PageName入参。下面的例子中我们会使用此常量进行跳转。
* **不带参数的跳转** 如下：
``` kotlin
// 跳转到login页面
gotoPage(PageConfig.LOGIN)
```
* **带参数的页面跳转** 我们提供了两种页面跳转的入参方式，你可以根据使用习惯任意使用
    * 方式一：Bundle方式入参
    ``` kotlin
    // 页面入参
    val args = Bundle()
    args.putString("userId", "xxxxxx")
    gotoPage(PageConfig.LOGIN, args)
    ```
    * 方式二：扩展方式入参
    ``` kotlin
    // 页面入参
    gotoPage(PageConfig.LOGIN) {
        putExtra("userId", "xxxxxxx")
    }
    ```
* **forResult的页面跳转** 在“A页面 -> B页面，当B页面完成业务逻辑后，A页面处理B页面的结果信息“这个案例中，B页面通过**setResult(result)**方法设置结果内容。在A页面中我们提供两种接收结果的方式
    * 方式一：多用在不需要页面入参，或者页面入参是已经现有的Bundle对象时。
    ``` kotlin
    fun openLogin(args: Bundle) {
        // 打开login页面
        gotoPage<Boolean>(PageConfig.LOGIN, args) { result ->
        }
    }
    ```
    在上面的例子中，我们新增了方法泛型**<Boolean>**和接收结果回调的lambda。此泛型是由目标页面的**setResult()**方法入参类型决定的，同时lambda中result的类型也由泛型推导得出，如图：
<img src="media/Rainbow%E4%B8%AD%E7%9A%84result%E6%B3%9B%E5%9E%8B1.png" width = 60% height = 60%/>

    * 方式二：推荐的使用方式，在lambda中扩展入参和回调
    ``` kotlin
    mBtnGotoLogin.onClick {
        // 打开login页面
        gotoPage(PageConfig.LOGIN) {
            // 设置入参
            putExtra("from", "test")
            //获取回调
            onResult<Boolean> { result -> 
                // 回调结果
            }
        }
    }
    ```
    在上面的例子中，**onResult()**方法的泛型和lambda中的入参都和目标页面的**setResult()**参数类型一致，可以参考方式一的图，不再赘述。
    
