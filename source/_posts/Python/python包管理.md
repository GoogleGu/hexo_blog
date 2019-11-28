---
title: python包管理
date: 2019-11-27 19:27:05
tags:
    - best practice
---

## 根据project内的依赖生成requirements.txt

requirements.txt最早的时候是靠自己手打敲出来，经常忘了修改，导致requirements.txt内的依赖和实际依赖不符。作为一个程序员，这种机械式的工作不能自动化也是蛮耻辱的。
利用pip的freeze功能，可以使用`pip freeze > requirements.txt`将当前环境下的所有依赖都放进requirements.txt文件里，但是往往我们的项目只用到了其中的一部分，那么这个时候，最方便的方法是使用pipreqs。
<!-- more -->
上官方文档：

```python
Usage:
    pipreqs [options] <path>

Options:
    --use-local           Use ONLY local package info instead of querying PyPI
    --pypi-server <url>   Use custom PyPi server
    --proxy <url>         Use Proxy, parameter will be passed to requests library. You can also just set the
                          environments parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard output
    --force               Overwrite existing requirements.txt
    --diff <file>         Compare modules in requirements.txt to project imports.
    --clean <file>        Clean up requirements.txt by removing modules that are not imported in project.
```

使用例子：

```txt
$ pipreqs /home/project/location
Successfully saved requirements file in /home/project/location/requirements.txt
Contents of requirements.txt：
wheel==0.23.0
Yarg==0.1.9
docopt==0.6.2
```

## 使用`__init__.py`来管理导入

众所周知`__init__.py`的基本功能是指明所在的文件夹是一个python模块，但是除此以外，还可以用来方便导入工作和预处理。

### 导入子模块中的类

如果是很深的嵌套层的话，可以在__init__里加入子模块中类的导入语句，比如`from sub_module import SubModuleClass`，这样的话不用把sub_module导入也可以导入SubModuleClass了。

### 控制`import *`的导入

如果只有部分变量想在`from module import *`中导入，在__init__里定义__all__（这是一个list），将想要导入的变量名称以字符串的形式存入即可。
