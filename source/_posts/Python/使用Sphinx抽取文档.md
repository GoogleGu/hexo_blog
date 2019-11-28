---
title: 使用Sphinx抽取文档
date: 2019-11-27 19:23:29
tags:
    - best practice
---


sphinx是一个抽取python代码注释生成python文档的模块。由于最近在整理项目的文档，因此研究了一下sphinx，以便于生成可读性更好的，更加美观的项目文档。
<!-- more -->

## 第一步：安装sphinx

非常简单，直接用pip命令`pip install sphinx`。

## 第二步：用sphinx的快速启动来创建文档目录

cd到想要创建文档目录的地方，然后输入`sphinx-quickstart`，之后sphinx会抛出一系列的问题来让你回答，大部分只要按回车选择默认或者选择y即可。建议在选择是否分离源文件和生成的文件时选择y，不然目录会变得很杂乱。
全部完成后，会发现目录下面生成了一些文件夹以及一个conf.py文件和一个index.rst文件，还有一个Makefile文件。
conf.py文件是用来配置sphinx用的，index.rst文件是用来配置生成的文档用的。

## 第三步：调整conf.py文件

conf.py其实就是个python文件，其中配置了一系列的sphinx配置项。

### 将需要生成文档的项目在conf.py中加入到系统路径中

在原来的文件中有这样三行被注释掉的代码：

```python
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
```

将其注释回来并将第三行修改为`sys.path.insert(0, os.path.abspath('/your/project/root/path'))`即可，其中`/your/project/root/path`为你的项目根目录的相对路径或是绝对路径。

### 将Napoleon加入到sphinx的扩展中

sphinx在初始配置下只能解析传统的reStructuredText语法，而这种语法其实不是那么的好写或那么的易读。相比之下，Numpy或Google形式的纯文本要好的多，为了让Sphinx能理解这些格式的纯文本，西药酱sphinx.ext.napoleon添加到extensions列表中，也就是改成这样(根据之前快速启动时的配置不同，extensions中的东西会不一样，但是最后一项也就是napoleon扩展是要添加进去的。)：

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
```

## 第四步：更新index.rst

到了这一步，我们应该开始在index.rst中告诉sphinx我们想给哪些模块和类生成文档。
打开index.rst文件会发现以下的内容：

```
.. Getting Started with Sphinx documentation master file, created by
   sphinx-quickstart on Mon Nov 13 11:41:03 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
Welcome to Getting Started with Sphinx's documentation!
=======================================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:
Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

我们要做的就是在toctree这一栏上面添加我们要的模块和类，格式如下：

```
Welcome to Getting Started with Sphinx's documentation!
=======================================================
.. automodule:: my_project.main
    :members:
.. toctree::
   :maxdepth: 2
   :caption: Contents:
Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

这样写就是将myproject.main中的所有方法和类全部抽取出文档。

## 第六步：生成文档

cd到sphinx文档的根目录中（也就是之前执行sphinx-quickstart的地方）输入`make html`，等待命令行运行完毕即可。之后就可以去查看生成的html文件了。

## 第七步：自动生成所有文档

这样一个模块一个模块加到rst文件中太慢也太蠢了，我们其实跑一个命令让sphinx自动为我们把项目里的模块和类全部加入到rst中。
命令是这样的：
`sphinx-apidoc -f -o 输出目录 源代码目录`
`-f`指令会让sphix-apidoc强制用新生成的文件覆盖旧文件。
`-o 输出目录`会将生成的输出放置到输出目录中去。一般是将输出引入到sphinx文档根目录下的source目录中去。
