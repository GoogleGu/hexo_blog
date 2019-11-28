---
title: python日志
date: 2019-11-27 19:28:52
tags:
    - best practice
---

## 日志级别

python的日志级别分为6个，其对应的值是：

- NOTSET 0：不体现在应用层面。
- DEBUG 10：一般为大量的、debug用途的信息类日志，比如在迭代中某个值的变化这样的日志，在生产环境中一般会忽略DEBUG级别的日志。
- INFO 20：一般为查看程序进程的日志，比如到达某个程序节点，收到某条请求等信息。
- WARNING 30：警告信息，即程序没有出错，但是一些值得开发者注意的事件，比如用户登录时账号密码错误，或是某个网络请求超时等。
- ERROR 40：用于记录程序中的异常和错误，一般该级别的日志要记录错误的trace信息以便于debug。
- CRITICAL 50：用于记录程序中非常严重的错误，比如会导致整个程序崩溃的异常。

用户可以设置的是除了NOTSET以外的五个级别。
<!-- more -->

## logger类

logger类是用来传入日志的具体类，具体进行日志记录使用的就是logger的debug、info、warning、error、critical方法。

### 获取

获取logger对象用的是`logging.getLogger(name)`，name应为字符串。该方法会返回一个名字为name的logger实例，注意每个logger都有一个独特的名字，因此如果传入的名字已经有对应的logger的话则不会创建新logger。

### 属性

logger有几个重要的属性：
**propagate**: 默认为真，是否向上层logger传递日志。
**level**: 日志等级，用于过滤传入的日志，任何等级低于此设置的日志都不会被展示。但是从子logger传来的日志不会被检查。
**Handlers**: 用于存放该logger用于处理日志的handler，如果想要向多个端写入日志的话，比如同时写入文件和终端，则需要在这里放置多个handler。

### 等级

logger之间是有等级的，低级的logger和高级的logger之间名字以`.`标识，如果父级logger不存在，则父logger默认为root logger。

## Handler类

handler是用来将日志进行记录的类，日志信息在传入logger后，logger将日志委托给Handlers中存储的handler，由这些handler对传入的日志进行处理。

### 种类

#### 写入到流对象

`logging.StreamHandler(stream=None)`
默认的handler，默认会将日志写入到stdout，可以在构建时传入一个流对象，则后续会将日志写入到该流中。

#### 写入到文件

`logging.FileHandler(filename, mode='a', encoding=None, delay=False)`
将日志写入到文件的handler，默认用a的方式将日志写入，文件大小没有限制。

`logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False)`
在FileHanlder的基础上添加备份和最大文件大小的选项，当当前日志文件大小超过maxBytes的时候，会打开一个新的日志文件，并将之前的日志文件命名为原文件名.1，最多会保留backupCount个备份，而当前进行日志记录的文件永远为原文件名的文件。如果maxBytes和backupCount任一值为0，则该handler的行为模式和原FileHanlder一样。

`logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None)`
在FileHanlder的基础上添加了按照时间间隔轮换记录日志的功能。when参数传入的是时间单位，分别为S-秒，M-分钟，H-小时，D-天，W0到W6->一周中的某一天，midnight->每个零点，atTime可以用于计算初次的轮换时间。如果backupCount不为0，最多会有backupCount份日志被保存。

## Formatter类

`logging.Formatter(fmt=None, datefmt=None, style='%')`
将传入的日志对象以特定的字符串形式输出。

## Best Practice

目前个人对日志的使用方法是创建一个独立模块logutil，在模块中构建一个单例类，在python读取该模块时该单例类即被创建，之后使用logutil.info等方法来记录日志，实际上是委托给该单例日志类进行日志的记录。需要对该单例类进行的格式设置以及输出源配置可以在构建时完成也可以对外提供接口后续完成。
好处是不需要在各个模块中单独创建logger类，节省了很多代码，且记录日志时额外进行的一些特殊的操作（比如向websocket发送日志）可以在logutil中统一添加。
