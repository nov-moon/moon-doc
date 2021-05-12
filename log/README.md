# 日志管理
在我们平时的子库开发中，在调试阶段需要在关键节点进行日志打印，方便跟踪数据变化，调试代码。所以往往子库可能会封装自己的日志工具，导致代码重复，且易重名，在上层应用中可以找到很多重名日志工具，浪费人力且容易造成困扰。皓月日志管理工具提供了如下功能：
1. 支持多子库的日志打印，子库可动态注册/解注打印器。
2. 支持默认日志打印器，方便快速接入
3. 支持Kotlin的扩展方式进行日志打印，方便随时随处插入日志

我们默认的日志输出格式如下：
```
<------------------------------------- demo2 ------------------------
from TestLog.log1 (TestLog.kt:19)

日志内容
--------------------------------------- End -------------------------
```
日志上下会有一个空行，以`<---- tag -----`开头，以`------- End ------`结尾。内容区第一行为此Log的代码调用位置。再下面为要输出的日志内容。

## 1. 快速集成
日志管理工具是kit库中实现的功能，所以引入kit库就默认集成了日志打印功能。具体kit库的引入方式请参见：[kit引入文档](kit/kit_import.md)

-------

## 2. 使用方式
皓月日志的主要功能定义在`Logcat`类中，他提供两类功能：**日志打印器的注册**和统一的**日志打印**方法。下面我们分别介绍这两类功能的使用方式。
### 2.1. 注册日志打印器
皓月日志的设计初衷是为了方便不同子库的日志管理。为了区分不同的子库，我们采用了子库主包名作为子库id，在调用日志api时，会尝试分析调用代码所在类的包名，用来匹配不同子库打印器。为了提供子库定制化日志的能力，我们提供了日志打印器的注册功能。在日志打印前，我们强烈推荐你调用注册方法，用来初始化子库打印器。注册方法的入参分以下情况：
1. 如果入参是ILogger对象，则此对象作为自定义的日志打印器。
2. 如果入参是其他类型，则入参的包名将作为此子库的注册Id使用，如果后续日志调用是在此包名下，则会分配给此对象去处理

> 我们也想了很多如何方便的区分不同类库，例如使用固定日志对象处理，使用自定义资源文件处理等等。最终还是感觉使用包名作为区分id是最简单的方式，后续如果发现什么问题，再做修正和优化

注册方法的声明如下（在**Logcat**中）：
```kotlin
/**
 * 注册一个logger
 *
 * 入参[entry]支持三种类型：主包下的对象、String类型的主包名、ILogger对象
 *
 * 当为前两种类型时会自动使用[DefLogger]作为日志打印器，使用入参[entry]的包名作为打印器的id。
 * 后续打印只有在此包名以及子包下的调用才会使用此打印器。
 *
 * 当为ILogger对象时，则直接使用此对象作为日志打印器
 *
 * [defTag]参数用来定义此打印器的默认tag，如果不进行设置，则会使用主包名的最后一段作为默认tag
 */
fun register(entry: Any, defTag: String? = null)
```
同时提供解注方法：
```kotlin
 /**
 * 解注一个logger
 *
 * 入参接收三种类型：主包下的对象、String类型的主包名、ILogger对象
 *
 * 解注以后，对应logger将不能进行日志打印
 */
fun unregister(entry: Any)
```
通常，注册日志打印器时，只需要提供当前子库的包名或者子库下的对象即可，而不需要提供ILogger实现。如果没有提供自定义的ILogger实现，则默认使用**DefLogger**，它的定义如下：
```kotlin
/**
 * 默认的日志打印器
 *
 * 提供标准的[ILogger]规定功能
 *
 * 为了让打印内容更容易区分，做了如下打印内容优化：
 * 1. 会以[top]作为开头，并且在top中插入自定义tag，强化开头，[end]作为结尾
 * 2. 打印的第二行会输出 '调用日志打印的代码位置'，方便代码回溯
 * 3. 提供了headerInfo作为扩展信息，方便对日志添加扩展信息
 * 4. 如果打印对象为集合或者map，则会采用json形式进行打印，方便集合等内容打印
 * 5. 打印内容如果本身有换行，则使用两行进行打印，方便对齐打印内容
 *
 * 根据上述第4条我们可以知道，日志打印对集合和map做了特殊功能处理，这里考虑为什么不对所有对象做json处理呢？
 * 我们考虑到：1.你有可能想定制自己的toString进行日志内容管理。2. 你有可能是想看他的内存地址。3. 过于消耗性能。
 * 所以我们只提供了针对特殊情况的特殊处理
 */
class DefLogger(override var id: String) : ILogger
```
### 2.2. 开始打印日志
皓月日志主要是为日志打印做服务，简化日志的统一管理和接入。我们提供了常见的d、e、v、w、i的不同级别日志打印，同时提供了json方式的日志打印，分别对应**Logcat**的中的同名方法，如：
```kotlin
// 打印日志
Logcat.d("I am log")
```
在我们很多日志的应用场景中，其实不是所有位置都提前写好了要打印的日志。而是在出现问题时，需要在特定的代码处添加日志，方便查看此时的数据信息。例如：
方法sum提供参数加1的功能
```kotlin
fun sum(param: Int):Int {
    return param + 1
}

// 得到的结果应该是4
sum(3)
```
这时候我们想查看sum方法是否得到的结果为4，通常我们如下修改：
```kotlin
// 得到的结果应该是4
val result = sum(3)
Logcat.d(result)
//或者
Logcat.d(sum(3))
```
可见，添加日志通常需要修改代码调用结构。针对这种情况，我们提供了对象扩展的日志方式：
```kotlin
/**
 * 打印日志，级别：debug
 *
 * 默认使用当前调用的包名作为loggerSubId
 *
 * 更多定制参考[Logcat.d]、[Logcat]
 */
fun <T> T.log(tag: String? = null): T
```
类似的其他级别日志方法为：**logE()、logW()、logV()、logI()、logJson()**。通过这种扩展方式的日志功能，上述情况我们可以如下实现：
```kotlin
// 打印sum(3)的结果，并且返回此结果
sum(3).log()
```
通过这种方式，你可以方便的随时插入自己的日志，而不用修改调用结构。
扩展方法只是提供了一些简单的日志打印能力，如果要更多的定义日志打印，需要直接使用**Logcat**中的api：
```kotlin
/**
 * 打印日志，级别：debug
 *
 * 如果msg == null 则会打印："log is null"
 * 对日志内容的不同处理，可能会是不同的，因为真正的打印会分派到对应[loggerSubId]的打印器中。
 * 如果没有自定义打印器，则会使用[DefLogger]作为默认的日志打印器。
 *
 * [msg] 打印的日志信息
 * [tag] 日志的tag信息
 * [headerInfo] 日志的头信息
 * [loggerSubId] 指定的日志器id，默认使用上层调用的包路径
 */
@JvmStatic
fun d(msg: Any?, tag: String? = null, headerInfo: String? = null,
      loggerSubId: String? = null)
```
还有类似的其他级别日志api。

-------
## 2.3. 自定义trace打印数量
我们在打印日志的时候，默认会先打印当前日志调用的trace信息。

默认打印一层trace信息，也就是日志所在位置。

你也可以通过设置全局配置进行日志的trace数量设置，如下：
``` kotlin
// 一般在application中设置一次即可
Logcat.config().traceCount = 3
```

根据上面的设置，效果如下：
```
<------------------------------------- demo2 ------------------------
from OnClickListenerFilter.onClick (AndroidUtils_.kt:312)
        MainActivity$onCreate$2.invoke (MainActivity.kt:17)
            TestLog.log1 (TestLog.kt:19)

日志内容
--------------------------------------- End -------------------------
```
最后一行为触发日志打印的方法，整体顺序为调用堆栈顺序。

你也可以在单次日志打印时定义trace数量，如下
``` kotlin
// 设置trace数量
Logcat.e("logTest", traceCount = 2)

// 设置trace数量
"logTest".log(traceCount = 2)
```

如果在调用日志打印时，不设置打印trace的数量，则默认使用全局config中的配置。

## 3.1. 更多自定义
你可以使用更多api做更多的功能性定制
### 3.2. 定义自己的日志打印器
例如你不满足DefLogger提供的日志功能，想自定义更好的日志效果，例如使用Logger做真正的日志输出，可以通过注册自定义ILogger的方式扩展打印方式。
#### 3.2.1. 第一步：新建ILogger实例类
首先，你需要自己实现一个继承自**ILogger**的类，它是我们的打印api定义接口类，具体声明如下：
```kotlin
/**
 * 日志标准接口
 *
 * 提供打印器的id设置、是否可用、默认tag。提供日志打印（级别参见[Level]），日志json、xml格式打印
 */
interface ILogger
```
在对应的log方法中转调到Logger中：
```kotlin
override fun log(msg: Any?, level: ILogger.Level, tag: String?, headerInfo: String?, fixedMethodCount: Int?) {
        val p = when (level) {
            D -> Logger.DEBUG
            V -> Logger.VERBOSE
            I -> Logger.INFO
            W -> Logger.WARN
            E -> Logger.ERROR
        }
        Logger.log(p, tag, msg?.toString(), null)
    }
```
#### 3.2.2. 第二步：注册自己的ILogger
将第一步实现的ILogger进行实例化，并注册到**Logcat**中：
```kotlin
//第一步：初始化自定义ILogger
val logger = LoggerProvider()
logger.id = "com.meili.moon.sdk.demo"
logger.defaultTag = "Meili"

//第二步：注册自定义ILogger
Logcat.register(logger)
```
注册完成后，`com.meili.moon.sdk.demo`包下的所有日志将使用新的日志打印器进行处理。

-------

### 3.3. 定义日志的头信息
有时候在日志打印的时候，我们希望获取到上下文的代码调用位置。例如，在打印从网络返回的数据时，我们在日志中只会输出当前的打印位置，其实我们更多的时候是想打印出发起网络的代码位置，而不仅仅是网络日志的位置。皓月日志在打印日志时提供了**headerInfo**参数用来扩展日志打印信息，请参见**Logcat**类中的日志方法。同时**Logcat**中提供了两个便捷的工具方法用来获取指定的代码调用位置，如下：
```kotlin
/**
 * 获取当前调用位置的日志头信息。
 *
 * 获取到的格式如下：类名 + . + 调用方法名 + ( + 文件名称 + : + 行号)。
 * 例如：MainActivity$onCreate$5.onClick (MainActivity.kt:30)
 *
 * 一般用来获取代码调用的日志格式信息，在打印日志是进行头信息设置
 *
 * [fixedIndex] 修复的方法堆栈的调用index，默认只取调用此方法的位置
 */
fun getLogInvokeInfo(fixedIndex: Int = 0): String
/**
 * 获取当前调用位置的日志头信息。
 *
 * 获取到的格式如下：类名 + . + 调用方法名 + ( + 文件名称 + : + 行号)。
 * 例如：MainActivity$onCreate$5.onClick (MainActivity.kt:30)
 *
 * 一般用来获取代码调用的日志格式信息，在打印日志是进行头信息设置
 *
 * [invokePath] 目标方法的调用路径，例如：com.meili.moon.sdk.log.Logcat.d，不要有方法的括号
 */
fun getLogInvokeInfo(invokePath: String): String?
```
通过上面的方法，可以方便的获取到当前代码的位置信息，并结合我们的默认日志打印器**DefLogger**，在日志中进行打印，如下：
```kotlin
fun log() {
    //获取当前代码位置，并传给log1
    log1(Logcat.getLogInvokeInfo())
}

fun log1(headerInfo: String?) {
    //打印日志，并添加头信息
    Logcat.d("TestLog.log()", headerInfo = headerInfo)
}
```
最终打印的日志如下：
```
<------------------------------------- demo2 ------------------------
TestLog.log (TestLog.kt:15)
 
from TestLog.log1 (TestLog.kt:19)

TestLog.log()
--------------------------------------- End -------------------------
```
`TestLog.log (TestLog.kt:15)`就是我们添加的头日志信息，至此我们就可以方便快捷的添加多个可能需要关注的代码位置信息。当然你也可以添加其他的头信息。