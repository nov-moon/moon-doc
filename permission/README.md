# MoonPermission
**MoonPermission**是一套旨在简化、标准化Android动态权限的动态权限库。在Android6.0以后，对系统权限大体分为两类：**正常、危险**。正常权限只需要在Manifest文件中进行声明即可，系统会在应用安装时，默认授权。危险权限是有可能涉及用户隐私，危害系统安全的权限，需要**在Manifest中进行声明，并且在使用处，明确申请所需权限**。

在MoonPermission中，我们简化了动态权限的申请操作，并提供了部分交互，使整体流程更清晰，更人性化，具体特点如下：
1. 支持注解方式，对方法添加所需权限
2. 支持直接调用方式，可自由选择结果回调方式
3. 支持拒绝权限时的用户交互，以及交互定制

## 1. 快速集成
### 1.1. Gradle
```api "com.meili.moon.sdk:permission:x.x.x" ```
具体版本详见：[版本更新日志](UpgradeLog.md)
### 1.2. 初始化
可以在**Application的onCreate**中进行初始化：```MoonPermissionImpl.init(application)```
## 2. 使用方式
**MoonPermission**提供两种使用方式：**直接调用、方法上的注解**。在一次权限请求过程中，有三种请求结果：**请求成功、权限被拒、权限被拒并且不再提醒**。针对后两种情况，在MoonPermission中，提供了两个弹窗，用来引导用户授权，流程如图：

<img src="media/%E5%8A%A8%E6%80%81%E6%9D%83%E9%99%90-%E5%A4%A7%E4%BD%93%E6%B5%81%E7%A8%8B%20-1-.png" width = 60% height = 60%/>

你可以通过后续的Config选项来定制你的交互细节。

### 2.1. 直接调用方式
在我们的请求中，可以通过**CommonSdk.permission()**直接进行MoonPermission上的api调用。例如我们在打开摄像头前，需要请求摄像头权限，如下：
``` kotlin
mCameraBtn.onClick {
    CommonSdk.permission().request(Manifest.permission.CAMERA) {
        // 成功后的回调
        // openCamera()
    }
}
```
如上所示，这种调用方式只有当所需权限都被授权时，回调方法才会触发。如果没有被授权，其中被拒交互将使用默认交互。如果你需要关注被拒的权限列表和被拒时机，你可以调用**requestWithFailed()**方法，如：
``` kotlin
CommonSdk.permission().requestWithFailed(Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA) { isAllGranted, granted, denied ->
    // isAllGranted 是否所有权限都被授予
    // granted 已经授权的权限列表
    // denied 已经拒绝的权限列表
}
```
> 以上提供的两个方法的入参，都是可变长参数，根据需要的权限数进行入参

### 2.2. 注解方式
在MoonPermission中，我们支持对**方法添加注解**，并在注解上说明此方法所需权限，当其他方法调用此方法时，**会先触发授权，在授权成功后再调用此方法**。这种处理方式是基于编译期的字节码插桩，修改被注解的方法实现的，所以需要添加如下配置：
1. 在项目根目录的**build.gradle**中添加**classPath**
    ``` groovy
    // 在buildscript节点的repositories中添加meili库，并在buildscript节点添加classPath
    buildscript { 
        repositories {
            // 其他库信息
            maven { url MEILI_MAVEN }
        }
        dependencies {
            classpath 'com.meili.moon.gradle:moon-tools:x.x.x'
        }
    }
    ```
    具体moon-tools版本号详见：[moon-tools版本更新日志](../kit/dev_tools/moon_tools/UpgradeLog.md)
2. 在使用权限的**Module中的build.gradle**添加插件
    ``` groovy
    apply plugin: 'moon-kit'
    ```

至此插件相关配置已经完成。
 
在需要权限的方法上，添加**Permission注解**，还是以camera为例：
```kotlin
@Permission(Manifest.permission.CAMERA)
private fun openCamera() {
    // 正常的打开操作
}
 ```

关于Permission支持的更多功能，可以参照[Permission文档](Permission注解.md)

> 注意，使用注解的方法，返回类型必须为void，否则将报错

## 3. 请求配置
在**MoonPermission**中，我们提供了**Config**用来进行**全局配置**和**单次请求配置**，例如在初始化后，可以进行如下配置：
``` kotlin
// 初始化
MoonPermissionImpl.init(this)
// 全局配置
MoonPermission.Config.newInstance().apply { 
    // 是否使用被拒后的dialog交互，默认为true
    isDeniedUEAvailable = false
    
    // 是否使用被拒并且不再提示后的dialog交互，默认为true
    isDeniedRememberUEAvailable = false
    
    // 是否直接使用 'deniedRemember权限交互'，舍弃使用 'denied权限交互'。
    // 如果你不希望用户拒绝后，再弹出授权界面，可设置此项为true。
    // 此项为true时，当用户拒绝权限，不管是否被记住，都只会弹出去设置弹窗
    isDirectDeniedRememberUE = true
    
    // 设置被拒后的弹窗上的title
    onDeniedTitle = "权限申请"
    
    // 设置被拒后的弹窗上的描述信息，此String以拼串的方式使用，接收两个string：
    // 第一个为被拒权限名称列表例如：定位、电话，
    // 第二个为被拒权限影响的功能名称，例如：地图、打电话。
    onDeniedDescription = "请开启%s权限，以正常使用%s功能"
    
    // 设置被拒并且不再提示后的弹窗上的描述信息，此String以拼串的方式使用，接收三个string：
    // 第一个为app名称占位符
    // 第二个为被拒权限名称列表例如：定位、电话，
    // 第三个为被拒权限影响的功能名称，例如：地图、打电话。
    onDeniedRememberDescription = "在设置-应用-%s-权限中开启%s权限，以正常使用%s功能"

    // 当被拒时，不使用框架默认的交互方式，自定义交互方式
    // denied 被拒绝的权限列表
    // permissionDesc 被拒绝的权限列表的描述信息
    // onCancel 当取消下一步操作时，回调此方法，一般在弹窗的取消按钮上调用
    // onSubmit 当继续下一步操作时，回调此方法，一般在弹窗的确定按钮上调用
    onDeniedUECallback = {denied, permissionDesc, onCancel, onSubmit ->  
        
    }
    
    // 当被拒并且不再提示时，不使用框架默认的交互方式，自定义交互方式
    // denied 被拒绝的权限列表
    // permissionDesc 被拒绝的权限列表的描述信息
    // onCancel 当取消下一步操作时，回调此方法，一般在弹窗的取消按钮上调用
    // onSubmit 当继续下一步操作时，回调此方法，一般在弹窗的确定按钮上调用
    onDeniedRememberUECallback = {denied, permissionDesc, onCancel, onSubmit ->  
        
    }
}.commit()
```

在提示用户某些权限被拒绝，影响某些功能时，我们需要将Android中的**系统权限转换为语义文本**，我们提供一套默认的**string-array资源**，用来进行控制，定义在权限库的string中，他的格式如下：
``` xml
<string-array name="moon_permission_accounts">
    <item>通讯录</item><!-- 被拒绝权限名称 -->
    <item>名片</item><!-- 影响的功能名称 -->
    <item>android.permission.GET_ACCOUNTS</item>
    <item>android.permission.READ_CONTACTS</item>
    <item>android.permission.WRITE_CONTACTS</item>
</string-array>
```
此数组中，**第一个item为转换的权限名称**，**第二个为影响的功能名称**，**后续为此名称下的具体权限**。当在此组中的权限被拒绝时，将进行类似提示：**"请开启通讯录权限，以正常使用名片功能"**。此提示格式可以通过**Config**中的**onDeniedDescription**进行设置。
在框架中，由于对于某些权限并不清楚在app中影响的功能，所以我们暂时使用中划线**‘-’**进行标记，表示此权限组影响的功能不明确，在提示时将把**影响的功能说明隐藏**，例如：**"请开启通讯录权限，以正常使用App功能"**。

你也可以自己**定义自己的xml进行资源扩展**，按照如上格式定义完成后，可使用**Config**上的**registerPermissionGroups()**方法进行注册。当然你也可以**覆写已经定义的资源id**进行定义。
具体的资源id和更多配置方式，参见[配置说明](配置说明.md)

如果你配置完成全局配置后，需要在某次请求中单独设置，可使用如下方式：
``` kotlin
val config = MoonPermission.Config.newInstance().apply {
    // 自定义配置
}

// 关注失败的调用
CommonSdk.permission().requestWithFailed(Manifest.permission.CAMERA, config = config) { isAllGranted, granted, denied ->
    // 回调方法
}

// 只关注成功的回调
CommonSdk.permission().request(Manifest.permission.CAMERA, config = config) {
    // 成功回调
}
```

也可以使用**扩展方式**进行调用：
``` kotlin
// 进行单次配置，并且只关注成功的回调
CommonSdk.permission().requestWithConfig(Manifest.permission.CAMERA) { 
    isDeniedUEAvailable = false
    onSuccess { 
        // 成功回调
    }
}

// 进行单次配置，并且关注成功和失败回调
CommonSdk.permission().requestWithConfig(Manifest.permission.CAMERA) {
    isDeniedUEAvailable = false
    onResult { isAllGranted, granted, denied -> 
        // 结果回调
    }
}
```
**以上两种回调方式不能兼容，只能使用一种方式，如果在开发期间，发现使用了两种回调方式，则会报错。**

## 4. 更多请求权限方式
我们提供了全局声明的方式，进行了方法扩展，提供了**三个便捷方法**，如下：
``` kotlin
// 请求权限，只关注成功
requestPermission(Manifest.permission.CAMERA) {
    // 成功回调
}

// 请求权限，关注成功和失败
requestPermissionWithFailed(Manifest.permission.CAMERA) { isAllGranted, granted, denied ->
    // 结果回调
}

// 请求权限，并且进行配置，只关注成功
requestPermissionWithConfig(Manifest.permission.CAMERA) {
    // 配置
    isDeniedUEAvailable = true
    onSuccess {
        // 成功回调
    }
}

// 请求权限，并且进行配置，关注成功和失败
requestPermissionWithConfig(Manifest.permission.CAMERA) {
    // 配置
    isDeniedUEAvailable = true
    onResult { isAllGranted, granted, denied ->
        // 结果回调
    }
}
```


