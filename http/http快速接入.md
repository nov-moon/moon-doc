
# 皓月网络库
皓月网络库是使用kotlin语言实现，基于okhttp3封装的网络框架，拥有以下特点：
1. 支持Http/Https协议/自定义Https证书认证
2. 支持同步/异步请求
3. 提供基于RequestParam定制化的请求体验
4. 提供基于泛型的数据集解析能力。
5. 提供批量定制化参数能力。
6. 提供快速缓存接入。
7. 提供UI绑定的请求回收机制
8. 提供请求参数以及返回结果的快速拦截
9. 提供网络请求的通用设置
10. 自定义线程池，使用自己的线程池管理网络请求

# 1. 快速集成
## 1.1. Gradle
 ```api "com.meili.moon.sdk:http:x.x.x" ```
## 1.2. 初始化
在application的onCreate()方法中进行初始化环境
```
class DemoApp : Application() {
    override fun onCreate() {
        super.onCreate()
        HttpSdk.init(this)
    }
}
```
注：如果项目中引入了moon_sdk_app，则不需要在单独初始化。
# 2. 使用方式
## 2.1 简单调用
在我们请求网络时，有时我们只是简单的访问服务器的一个接口，为此我们提供最简便的调用，例如下面是一个简单的get请求：
### 2.1.1. **get请求**
```kotlin 
httpGet{
    val param = DefHttpParams()
    //设置Url 例如“www.mljr.com/example/mock”
    param.setUrl("xxx")
    //设置请求头
    param.addHeader("header","xxx")
    //设置参数
    param.addParam("param","xxx")
    params = param
    //定义解析的返回数据类型的model
    onSuccess<解析的model>{
    }
}
``` 
### 2.1.2. **post请求**
post请求同理get请求
```kotlin
httpPost{
    val param = DefHttpParams()
        params = param
    onSuccess<解析的model>{ 
    }
}
``` 
框架会根据你提供的model自动帮你解析数据返回
## 2.2. 推荐接入方式
在我们做网络请求时，通常我们喜欢把通用的配置提取出来在application中全局配置，例如：请求头和通用url的设置，这样以后你的每个请求都不需要在去做重复的操作，我们推荐以下的接入方式，例如：
```kotlin
 val config = Config.newBuilder()
                .setBaseUrl("http://www.mljr.com/")
                .addHead("mljr","mljr")
                .build()
                
HttpImpl.config(config)
```
关于全局配置更多的信息可以参考[配置](配置.md)

接下来为了使我们的每一个请求都更加清晰明了，我们建议对于每一个请求都新建一个Params的类，继承DefHttpParams，我们可以在类中设置url,参数，拼接路径等操作,例如我们想要做一个登录的操作如下示例：
```kotlin 
@HttpRequest("mock/login")
class LoginParams() : DefHttpParams() {
    val username = "mljr"
    val password = "mljr123"
}

 httpGet {
    val param = LoginParams()
    params = param
    onSuccess<LoginUserModel> {  }
    onError { errorMessage, exception ->   }
 }
``` 
如果想更多了解配置参数的问题可以参考 [参数的详情](参数.md)
如果想更多了解配置请求头的的问题可以参考 [请求头的详情](头.md)

## 2.3. 另一种接入方式
我们在做网络请求时，如果你在一个app中有几类BaseUrl的请求，而全局config只能配置一个统一的，不满足需求，如果使用每一个请求都要重新设置，又大大的增加了开发量，这时候我们推荐你用另外一种继承的方式去实现请求。[更多接入](项目中接入.md)

# 3. 交互
在我们做网络请求时，通常如果你不想在每次请求前都做打开progress，请求完成式关闭progress的操作，或者在每次请求时都需要添加一些通用的操作，可以在你的base页面实现 UEHttpHolder接口，添加UI交互
```kotlin
interface UEHttpHolder : IDestroable {

    /**显示一个error的message，[ueType]为发起请求是定义的type*/
    fun showUEErrorMessage(msg: String?, ueType: Int)

    /**显示一个加载的进度，[ueType]为发起请求是定义的type*/
    fun showUEProgress(msg: String?, ueType: Int)

    /**取消一个加载的进度，[ueType]为发起请求是定义的type*/
    fun dismissUEProgress(ueType: Int)

    /**当前是否可交互*/
    var isUEnable:Boolean
}
```
# 4. 同步请求
我们在做网络请求时，如果你需要同步调用，可以使用如下方式：
## 4.1. 同步调用get方式
```kotlin
val param = DefHttpParams()
param.setUrl("xxx")
param.addHeader("header","xxx")
param.addParam("param","xxx")
var result = HttpSdk.http().getSync(param, xxxModel::class.java)
```
如果请求返回类型是List类型用如下方式：
```kotlin
val param = DefHttpParams()
var result = HttpSdk.http().getSyncList(param, xxxModel::class.java)
```
## 4.2. 同步调用post方式
```kotlin
val param = DefHttpParams()
var result = HttpSdk.http().postSync(param, xxxModel::class.java)
```
如果返回类型是List类型用如下方式：
```kotlin
val param = DefHttpParams()
var result = HttpSdk.http().postSyncList(param, xxxModel::class.java)
```

# 5. 其他
如果想了解更多个性化配置，请参考[个性化配置](配置.md)