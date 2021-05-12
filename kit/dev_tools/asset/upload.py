#! /usr/bin/env python3
# coding:utf-8
import os
import re
import sys
import sched, time
import threading

print("hello python")
library_name = ""
# 需要编译Lib库的集合
lib_list = []

# 读取setting。gradle文件，将有注释的项目去掉
with open(os.getcwd() + "/settings.gradle", "r") as f:
    lib_lines = f.readlines()
    for line in lib_lines:
        if line.find(r"//") == -1:
            library_name += line
# setting.gradle下面的所有文件名
library = os.listdir(os.getcwd())

# 目录中含有gradle.properties的项目并且在setting.gradle可编译的文件
for library_item in library:
    if os.path.exists(os.getcwd() + "/" + library_item + "/maven.gradle"):
        if library_item in library_name:
            lib_list.append(library_item)

# ['moon_sdk_db',
#  'moon_common_ui',
#  'moon_ui_dialog',
#  'moon_upload_img_base',
#  'common-bankcard',
#  'moon_sdk_cache',
#  'moon_sdk_network',
#  'moon_sdk_kit',
#  'moon_ui_form_edit',
#  'moon_sdk_app',
#  'common-idcard',
#  'finance-ocr_card-online',
#  'moon_sdk_base',
#  'moon_sdk_page_router',
#  'moon_sdk_web_bridge',
#  'moon_share']
print ("可编译的module   ")
print (lib_list)


class Library(object):

    def __init__(self, name):
        self.__name = name
        self.__update_relation = []
        self.__bedepend_relation = []

    def get_name(self):
        return self.__name

    def get_artifactId(self):
        return self.__artifactId

    def get_CurrentVersion(self):
        return self.__currentVersion

    def get_high(self):
        return self.__high

    def get_middle(self):
        return self.__middle

    def get_low(self):
        return self.__low

    def get_dependon(self):
        return self.__dependon

    def get_bedependon(self):
        return self.__bedepend_relation

    def set_name(self, name):
        self.__name = name

    def set_artifactId(self, artifactId):
        self.__artifactId = artifactId

    def set_CurrentVersion(self, currentVersion):
        self.__currentVersion = currentVersion

    def set_high(self, high):
        self.__high = high

    def set_middle(self, middle):
        self.__middle = middle

    def set_low(self, low):
        self.__low = low

    def set_dependon(self, dependon):
        self.__dependon = dependon

    def set_bedependon(self, bedependon):
        self.__bedepend_relation.append(bedependon)

    def registerUpdateListener(self, allModels, lib_name):
        if (lib_name not in self.__update_relation):
            self.__update_relation.append(lib_name)
        print ("升级的项目   " + self.__name)
        #     继续发送其他dependons的registerUpdateListener方法
        print ("当前项目关联的升级项目")
        print (self.__bedepend_relation)
        if len(self.__bedepend_relation) > 0:
            for depend in self.__bedepend_relation:
                # print "name   "+allModels[depend].get_name()
                allModels[depend].registerUpdateListener(allModels, self.__name)

    def removeUpdateListener(self, allModels, lib_name):
        self.__update_relation.remove(lib_name)
        if len(self.__update_relation) == 0:
            #     升级前 首先需要一下几步 判断当前的库的状态
            #     0 未升级过 继续正常流程
            #     1 升级成功了 直接跳过所有流程直接继续发送请求
            #     2 升级失败了 直接做升级操作 跳过准备工作
            currStatus = getStatus(self.__name)
            print "currStatus"
            print      currStatus
            # 只有未升级过才走升级准备操作
            if currStatus == 0:
                recordStatus(self.__name,"false");
            #     1，修改关联库的gradle.properties 中的MAVEN_VERSION，
                #     2，默认将最后一个版本号加一 后期看是否要添加其他规则
                if os.path.exists(os.getcwd() + "/" + self.__name + "/maven.gradle"):
                    with open(os.getcwd() + "/" + self.__name + "/maven.gradle", 'r+') as maven:
                        lines = maven.readlines()
                    data = ""
                    # 默认升级小版本号，读取到最后一位 然后升级一个写入进文件
                    for line in lines:
                        if line.find("def MAVEN_VERSION") == 0 and line.find(r"//") == -1:
                            key = re.compile(r'def MAVEN_VERSION = \'(.+?)\'')
                            model_name = key.findall(line)
                            line = "def MAVEN_VERSION = '%s%s'" % (
                                model_name[0][0:-1], str(int(model_name[-1][-1]) + 1))
                        data += line
                with open(os.getcwd() + "/" + self.__name + "/maven.gradle", 'w') as maven:
                    maven.writelines(data)

                # 查看依赖库的版本是不是最新版本
                # 只要是build.gradle依赖的 都替换为最新的版本
                for item in allModels[self.__name].get_dependon():
                    print self.__name + "  依赖库   " + item[0] + "  依赖库版本  " + item[1] + "." + item[
                        2] + "." + item[3]
                    if item[0] in artifact_list:
                        # 只要存在库 就将依赖库更新成记录的最高版本
                        print item[0] + " 的依赖的库的的最高版本为  " + high_version[item[0]]
                        if os.path.exists(os.getcwd() + "/" + self.__name + "/build.gradle"):
                            with open(os.getcwd() + "/" + self.__name + "/build.gradle",
                                      "r+") as car_gradle:
                                lib_data = ""
                                lines = car_gradle.readlines()
                                for line in lines:
                                    if line.find(r"implementation") != -1 and line.find(r"//") == -1:
                                        if line.find(item[0]) != -1:
                                            model_name = re.sub(r'\d.\d.\d', high_version[item[0]],
                                                                line)
                                            print "替换之后   " + model_name
                                            line = model_name
                                    lib_data += line
                            with open(os.getcwd() + "/" + self.__name + "/build.gradle",
                                      "w") as car_write:
                                car_write.writelines(lib_data)
            #   只要不是成功就执行升级操作
            if currStatus != 1 :
                print (self.__name + "开始升级")
                # print ("打包的版本信息   " + data)
                s = sched.scheduler(time.time, time.sleep)
                s.enter(2, 1, func, (self.__name,))
                s.run()
                r = 10 / 0
                # os.system("gradle :%s:uploadArchives" % self.__name)
                print (self.__name + "升级结束")
                # 升级成功后将状态改为success
                recordStatus(self.__name,"success");
                #   更新model , 更新自己的最新版本在libVersion.properties文件中
                # 更新allModels的最新依赖的版本号
                allModels[self.__name].set_low(str(int(allModels[self.__name].get_low()) + 1))
                # 更新一下 HighlibVersionReview.properties
                readGradleProperties()
            #   升级完成之后 继续发送其他dependons的removeUpdateListener方法

            #     开始升级
            for depend in self.__bedepend_relation:
                allModels[depend].removeUpdateListener(allModels, self.__name)

    def get_update_relation(self):
        return self.__update_relation


# 初始化model数据 对象 项目名称 MAVEN_ARTIFACT_ID 当前版本 高 中 低 三个版本号 权重
model_properties = {}
lib_dependon = []
for item in lib_list:
    dependencies = ""
    if item != "":
        if os.path.exists(os.getcwd() + "/" + item + "/maven.gradle"):
            with open(os.getcwd() + "/" + item + "/maven.gradle") as maven:
                properties = maven.read()
                key = re.compile(r'MAVEN_ARTIFACT_ID = \'(.+?)\'')
                artifactId = key.findall(properties)
                key1 = re.compile(r'MAVEN_VERSION = \'(.+?)\'')
                versions = key1.findall(properties)
        model_properties[item] = Library(name=item)
        if os.path.exists(os.getcwd() + "/" + item + "/maven.gradle"):
            with open(os.getcwd() + "/" + item + "/maven.gradle", 'r+') as maven:
                lines = maven.readlines()
                data = ""
                record_version = ""
                # 默认升级小版本号，读取到最后一位 然后升级一个写入进文件
                for line in lines:
                    if line.find("def MAVEN_VERSION") == 0 and line.find(r"//") == -1:
                        key = re.compile(r'MAVEN_VERSION = \'(.+?)\'')
                        model_name = key.findall(line)
                        # 格式标准不标准 异常处理
                        # print (model_name[0])
                        # line = "MAVEN_VERSION='%s%s'" % (
                        #     model_name[0][0:-1], str(int(model_name[-1][-1])))
                        model_properties[item].set_high(model_name[0].split('.')[0])
                        model_properties[item].set_middle(model_name[0].split('.')[1])
                        model_properties[item].set_low(model_name[0].split('.')[2])
                        model_properties[item].set_CurrentVersion(model_name[0])

        model_properties[item].set_artifactId(artifactId[0])
# 所有项目的artifactId集合
artifact_list = []
for item in lib_list:
    artifact_list.append(model_properties[item].get_artifactId())

# 向对象中添加依赖的库，过滤调项目中第三方的依赖项目
for item in lib_list:
    if os.path.exists(os.getcwd() + "/" + item + "/build.gradle"):
        with open(os.getcwd() + "/" + item + "/build.gradle") as model:
            dependencies = model.read()
            p = re.compile(r':(.+):(\d+).(\d+).(\d+)')
            # 不是
            dependons = p.findall(dependencies)
            lib_dependon = []
            for itt in dependons:
                if itt[0] in artifact_list:
                    lib_dependon.append(itt)
    model_properties[item].set_dependon(lib_dependon)

# 添加 被依赖 bedependon
for item in model_properties:
    for item2 in model_properties:
        for dependon in model_properties[item2].get_dependon():
            if dependon[0] == model_properties[item].get_artifactId():
                model_properties[item].set_bedependon(item2)

print ("++++++++++输出数据+++++++++++++++++++++")

# 将每个库的当前版本号写入HighlibVersionReview.properties
high_version = {}


# 更新HighlibVersionReview.properties 和 high_version 每次升级库之后都更新成最新的
def readGradleProperties():
    with open(os.getcwd() + "/HighlibVersionReview.properties", "w") as w:
        for item in model_properties:
            version_name = model_properties[item].get_artifactId() + " = " + model_properties[
                item].get_high() + "." + model_properties[item].get_middle() + "." + \
                           model_properties[item].get_low()
            high_version[model_properties[item].get_artifactId()] = model_properties[
                                                                        item].get_high() + "." + \
                                                                    model_properties[
                                                                        item].get_middle() + "." + \
                                                                    model_properties[item].get_low()
            w.write(version_name + '\n')


if os.path.exists(os.getcwd() + "/CurrentVersionTemp.properties"):
    var =""
else:
    with open(os.getcwd() + "/CurrentVersionTemp.properties", "w") as w:
        w.write("")

class status():
    ORIGINAL = 0
    SUCEESS = 1
    FAIL = 2

# 记录升级库的状态，
def recordStatus(name,status):
    data = ""
    with open(os.getcwd() + "/CurrentVersionTemp.properties", "r+") as r:
        readlines = r.readlines()
        for line in readlines:
            key = re.compile(name + ' = (.+?)@')
            version = key.findall(line)
            if len(version) != 0:
                line = name+" = "+status+"@"+'\n'
            data += line
        if name not in data:
            sta = name+" = "+status+"@"+'\n'
            data += sta
    with open(os.getcwd() + "/CurrentVersionTemp.properties", "w") as w:
            w.write(data+'\n')



def getStatus(name):
    with open(os.getcwd() + "/CurrentVersionTemp.properties", "r+") as r:
        readline = r.read()
        key = re.compile(name + ' = (.+?)@')
        model_name = key.findall(readline)
        print "---->>>>>>>>>>-------------"
        if len(model_name) == 0:
            return status.ORIGINAL
        else:
            if model_name[0] == "success":
                return status.SUCEESS
            else:
                return status.FAIL


readGradleProperties()
print ("_____________________________________________")
print ("最新的 版本信息  ")
print (high_version)
print ("______________________________________________")
for item in model_properties:
    print ("项目名称 " + model_properties[item].get_name())
    # print (model_properties[item].get_name() + "   artifactId   " + model_properties[
    #     item].get_artifactId() + '  '
    #        + model_properties[item].get_CurrentVersion() + "   "
    #        + model_properties[item].get_low() + "   ")
    print ("项目的dependon   ")
    print (model_properties[item].get_dependon())
    print ("项目被谁引用   ")
    print (model_properties[item].get_bedependon())

lib_name = sys.argv[1]
print ("gradle :%s:uploadArchives" % lib_name)
# 记录当前的库的版本信息，如果升级失败之后要重新升级 升级过版本号 就清空CurrentVersionTemp.properties文件
def recordOriginalStatus():
    with open(os.getcwd() + "/CurrentVersionTemp.properties", "r+") as r:
        readfile = r.read();
        key = re.compile("@"+model_properties[lib_name].get_name() + ' = (.+?)@@')
        version = key.findall(readfile)
        if len(version) != 0:
                # 判断存在的版本号和系统中的版本号是否一致 不一致要清空CurrentVersionTemp.properties
                if model_properties[lib_name].get_CurrentVersion() != version[0]:
                    uploadMoudle()
                    # 不一致 原始库需要升级
                    print "清空数据"
                    readfile = ""
                    # 替换
                    # readfile = model_properties[lib_name].get_name()+" = "+model_properties[lib_name].get_CurrentVersion()+"@@"+'\n'

        # if clean:
        #     readfile = ""
        #     print "清空数据"
        if "@"+model_properties[lib_name].get_name() not in readfile:
            uploadMoudle()
            # 不再 原始库需要升级 因为是第一次升级
            sta = "@"+model_properties[lib_name].get_name()+" = "+model_properties[lib_name].get_CurrentVersion()+"@@"+'\n'
            readfile += sta

    with open(os.getcwd() + "/CurrentVersionTemp.properties", "w") as w:
        w.write(readfile+'\n')



print ("要升级项目的信息  " + model_properties[lib_name].get_name() + "   artifactId   " + model_properties[
    lib_name].get_artifactId() + '  '
       + model_properties[lib_name].get_CurrentVersion() + "   "
       + model_properties[lib_name].get_low() + "   ")
print (model_properties[lib_name].get_dependon())

print ("++++++++++++++输出数据+++++++++++++++++++++")
print ("所有项目的artifactId集合")
print (artifact_list)
for item in model_properties[lib_name].get_bedependon():
    print "需要升级的项目   " + item
    model_properties[item].registerUpdateListener(model_properties, lib_name)

def func(a):
    print(time.time(), "Hello Sched!", a)

# 自己的升级操作  读取gradle.properties的版本号 记录在文件中 方便下一个库去比对
def uploadMoudle():
    print("----->>>升级开始")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(2, 1, func, (lib_name,))
    s.run()
    # os.system("gradle :%s:uploadArchives" % lib_name)
    print("----->>>升级结束")

recordOriginalStatus()

for item in model_properties[lib_name].get_bedependon():
    model_properties[item].removeUpdateListener(model_properties, lib_name)


# 清空CurrentVersionTemp.properties
os.remove(os.getcwd() + "/CurrentVersionTemp.properties")
# for item in model_properties:
#     print (model_properties[item].get_name())
#     # print (model_properties[item].get_name() + "   artifactId   " + model_properties[
#     #     item].get_artifactId() + '  '
#     #        + model_properties[item].get_CurrentVersion() + "   "
#     #        + model_properties[item].get_low() + "   ")
#     # print (model_properties[item].get_dependon())
#     print (model_properties[item].get_update_relation())
