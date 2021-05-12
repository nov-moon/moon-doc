# MoonTools
MoonTools是为了皓月库快速开发而出现的gradle插件。
MoonTools主要提供了如下功能  

* **Module**的demo和lib模式切换，app模式下进行库的功能开发和测试，lib模式下进行库的打包和依赖.自动初始化demo所需文件。
* **Project**中的全局maven依赖和project依赖切换，支持快速全局切换项目是project依赖还是maven依赖
* 本地maven与公司maven快速切换

### 1. 快速集成
1. 在Project根目录的**build.gradle**中添加插件的依赖配置，如下:

     ```groovy
    buildscript {
        repositories {
            //添加公司的maven私服
            maven { url MAVEN_URL_PUBLIC }
        }
        dependencies {
            //添加MoonTools的插件包
            classpath 'com.meili.moon.gradle:moon-tools:1.0.0'
        }
    }
    ```  
2. 引入插件
在Module的build.gradle中，删除原来引入的`apply plugin: 'com.android.library'`，并将MoonTools插件引入：
      
    ```groovy
    //删除谷歌的Lib插件
    //apply plugin: 'com.android.library'
    
    //添加MoonTools插件
    apply plugin: 'moon-tools'
    ```  
-------
### 2. Module模式切换
当我们在开发一个Library项目时，有必要有一个配套的Demo对Library提供的api、功能¯¯进行调试、调优和回归。而通常情况下我们的一个Library会作为一个git项目进行版本管理，这样做的好处是一个Project中可以管理多个不同git的Module进行开发，坏处是这种管理方式很难优雅有效的管理配套Demo。  
MoonTools提供了Module级别的demo和library的快速切换功能。可以通过一个配置将当前Module设置为library或者demo模式。
> 由于我们是根据配置自动引入Android插件，所以在gradle中不兼容同时配置Android插件

#### 2.1. 开始使用
MoonTools提供了moonTools代码块作为配置入口。
* 在模式切换功能下，我们提供了配置，指定当前是否为demo模式，如下：

    ```groovy
    moonTools {
        //是否使用demo模式，默认为false
        useDemo true
        //是否使用kotlin插件，默认为true
        useKotlin true
    }
    ```

* 在开发demo时，难免会需要依赖一些第三方库。而谷歌提供的官方引入方式会导致我们在打包lib时存在冗余依赖，从而可能导致不必要的麻烦，增大引入体积。  
    针对这种情况，我们添加了 **demo** 关键字进行引入声明。使用 **demo** 方式引入的依赖，只有在DemoApp中可用，而在打包maven时会被过滤掉。具体的使用方式如下：
    ```groovy
    dependencies {
        // 只在demo中生效的库依赖
        demo 'com.android.support.constraint:constraint-layout:1.1.3'
    }
    ```
* 在引入MoonTools插件时，为了保证编译通过，我们会在Module的**src**目录下创建如下内容：
    * **src/demo/java/你的package/demo/MainActivity.kt** 用做启动页
    * **src/demo/res/drawable** 用于存放资源文件
    * **src/demo/res/drawable-xxhdpi/ic_launcher.png** 用于作为app启动图标
    * **src/demo/res/layout/activity_main.xml** 用于首页布局
    * **src/demo/res/values/(colors、strings、styles)** 用于存放资源文件
    * **src/demo/AndroidManifest.xml** 作为manifest文件，同时将添加部分初始化内容。设置了demo的包名为：**lib的包名 + demo**的形式。设置了Application节点和启动Activity，你可以自行修改相关内容。  

    demo生成App的名称为：**你的包名最后子包单词首字母大写 + Demo**，例如：com.meili.moon.sdk，生成的app名称为**SdkDemo**

至此，你就可以用配置Application项目的方式配置demo目录内容，从而得到一个可运行的demo项目。而在发布maven时，只需要关闭demo模式即可正常发布。

-------

### 3. Project的全局Maven/Project依赖切换
在大量开发有依赖关系的组件群时，有时我们为了增快开发节奏，需要直接以project的方式进行依赖，从而免去跨库修改代码而需要的频繁发布。而在代码相对稳定或者发布时，又需要将project的依赖方式改为maven的方式。整个过程繁琐，呆板，且容易出错。

针对以上需求，MoonTools为我们提供了如下功能：
1. Project级别的全局切换所有Module中指定依赖的maven/project
2. Module级别的自定义依赖方式，优先级高于全局配置
3. 依赖级别的maven/project自定义配置，优先级高于Module配置
4. Module级别的强制依赖方式，优先级高于依赖自定义配置
5. Project级别的强制全局依赖方式，优先级高于Module级别的强制依赖方式

我们提供的以上配置方式，从上到下，优先级依次提高。当有高优先级配置时，低优先级配置不生效。在此声明，他们的优先级如下：
`全局 < module < 特定依赖 < module强制 < project强制`

#### 3.1. 依赖的声明方式
为了便于管理配置，我们提供了用于依赖方式切换的依赖声明关键字：**projectMaven**。他的声明方式为两段式，用来提供project和maven的依赖配置，例如：

```groovy
dependencies {
    projectMaven 'moon_sdk_base|com.meili.moon.sdk:base:1.11.0'
}
```
如上举例，我们的声明格式为：`projectMaven 'module名称 + 竖线(|) + maven依赖'`

当配置决定使用module依赖时，则使用前半部分。在使用maven依赖时，则使用后半部分。

#### 3.2. 配置依赖方式
前文提到，我们提供5种不同优先级的依赖定义方式，他们具体的配置方式如下：

* 全局配置  
    在Project中的**gradle.properties**中可以通过moon.isAllMaven进行设置，例如：
    
    ```
    #设置全局配置为使用maven
    moon.isAllMaven=true
    ```
* Module配置  
    在Module中的**build.gradle**中，可以在**moonTools**代码块进行设置，例如：
    ```groovy
    moonTools {
        //当前项目依赖方式：0 maven依赖(默认)，1 project依赖。其他值都认为是maven依赖
        allMaven 0
    }
    ```
    
    在此情况下，如果当前配置和全局配置有冲突，则以当前配置为准

* 依赖级别配置  
    全局配置和Module配置可以满足不同级别的整体配置，而在个别情况下，你可能希望只针对个别依赖设置依赖方式。我们提供在依赖前添加 **^** 符号进行特殊设置。带有 **^** 符号的将忽略全局配置和module配置，直接使用被标记的依赖方式作为依赖。例如：  
    ```groovy
    dependencies {
        projectMaven 'moon_sdk_base|^com.meili.moon.sdk:base:1.11.0'
    }
    ```
    这种情况下，就算配置了module中的 `allMaven 1` ，当前依赖也会使用maven的方式进行依赖。全局配置同理。  
    如果两段配置都有 **^** 标记，则project依赖上的标记会起作用。
    
* Module中的强制方式
    如果在配置过程中，配置较复杂，不想对Module中的内容逐一更改，可以使用此方式强制指定当前Module的依赖方式，如下：  
    ```groovy
    moonTools {
        //当前项目依赖方式：0 maven依赖(默认)，1 project依赖
        allMaven 1
        
        //当前项目依赖方式，如果设置此值，则上面的allMaven会无效，：0 maven依赖，1 project依赖，其他值 等同于没有设置此值
        forceAllMaven 1
    }
    ```  
    当前配置会忽视上3种配置，直接使用当前配置作为依据
    
* Project中的强制方式  
    如果在配置过程中，配置较复杂，不想对所有Module的内容进行逐一修改，可使用此方式强制指定所有Module的依赖方式。  
    此功能需要在Project级别的**gradle.properties**文件中进行配置，如下：  
    ```groovy
    //强制项目中所有module的依赖方式，有三种设置方式：true 强制为maven，false 强制为project，不设置 不强制任何方式
    moon.forceAllMaven=false
    ```  
    在例子中我们知道，如果不需要强制，则请删除此配置，或者注释掉配置，true和false都是有特殊含义的。  
    如果有此配置，则上述4种配置将被忽略，直接使用强制指定的配置方式
    
-------

### 4. Maven的本地/服务器发布快速切换
功能暂未完成