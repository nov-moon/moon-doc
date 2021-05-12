# Kit库快速集成
### 快速集成
1. 在Project根目录的**build.gradle**中添加全局的依赖配置，如下:

     ```groovy
    allprojects {
        repositories {
            //添加公司的maven私服
            maven { url MAVEN_URL_PUBLIC }
        }
    }
    ```  
2. 引入kit库
在Module的**build.gradle**中，添加kit库的Maven依赖：
```groovy
dependencies {
        implementation("com.meili.moon.sdk:kit:版本号")
}
```
如果使用的是moon-tools插件，添加kit库的Maven依赖方式为：
```groovy
dependencies {
        projectMaven("moon_sdk_kit|com.meili.moon.sdk:kit:版本号")
}
```

kit库的版本号，请参见：[kit更新文档](UpgradeLog.md)

-------
