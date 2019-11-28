---
title: python异常汇总
date: 2019-11-27 19:25:31
tags:
     - best practice
---


python中自带了各种标准异常，如果对这些异常不够了解的话，往往在试图捕获异常时无法清晰地写出要捕获的异常类，自己编写代码时也不能依照python规范抛出应有的异常。了解异常的具体分类对于自定义异常也有很大的帮助，能够让自定义的异常分类更加合理，名称更加规范。因此在这里整理了python中常见的异常类以及常见的场合，作为对python异常学习的总结。
<!-- more -->

```python
BaseException
 +-- SystemExit: 由sys.exit()抛出，在捕获Exception时不会捕捉到该异常，因此调用sys.exit()时可以确保程序退出。
 +-- KeyboardInterrupt: 由键盘输入（比如Ctrl+C）导致的程序退出时抛出的异常。
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration: 迭代器中没有更多元素可以返回时抛出此异常。生成器或协程函数返回时会顺带抛出该异常，但是如果显示抛出该异常则会被转为RuntimeError。
      +-- StopAsyncIteration: 由异步迭代器返回来停止迭代。
      +-- ArithmeticError: 数学计算错误时抛出。
      |    +-- FloatingPointError: 目前没有使用。
      |    +-- OverflowError: 浮点计算和少量整数计算过大时会抛出此异常。（注意大部分整数计算过大会抛出MemoryError）
      |    +-- ZeroDivisionError: 进行了除以0的操作时抛出。
      +-- AssertionError: 断言失败时抛出。
      +-- AttributeError: 当查找属性或为属性赋值失败时抛出。如果对象压根不支持属性查找或赋值会抛出TypeError。
      +-- BufferError
      +-- EOFError: 当input方法没有读取到任何数据就遇到了EOF时抛出。
      +-- ImportError: import语句出错时抛出。
      |    +-- ModuleNotFoundError: ImportError的子类，当模块无法找到时抛出。
      +-- LookupError: 进行查询操作失败时抛出
      |    +-- IndexError: 序列下标越界时抛出。（如果传入的下标不是整数的话，会抛出TypeError）
      |    +-- KeyError: 当进行查询的key不在字典内时抛出。
      +-- MemoryError: 当某个操作内存不足时抛出。
      +-- NameError: 某个本地或全局变量名无法找到时抛出
      |    +-- UnboundLocalError: 当试图访问某个本地变量但是该本地变量没有绑定值时抛出。
      +-- OSError: 所有与IO异常、文件系统异常等系统层级有关的异常都与此相关。
      |    +-- BlockingIOError: 某个非阻塞操作将被某个操作阻塞时抛出。
      |    +-- ChildProcessError: 子进程中某个操作失败时抛出。
      |    +-- ConnectionError: 发生与连接有关的错误时抛出。
      |    |    +-- BrokenPipeError: 试图在另一端已关闭的通道上写入数据时抛出。
      |    |    +-- ConnectionAbortedError: 当尝试的连接被对方放弃时抛出。
      |    |    +-- ConnectionRefusedError: 当连接的另一方拒绝连接时抛出。
      |    |    +-- ConnectionResetError: 当连接的另一方将连接重置时抛出。
      |    +-- FileExistsError: 尝试创建的文件已经存在时抛出。
      |    +-- FileNotFoundError: 尝试读取的文件不存在时抛出。
      |    +-- InterruptedError: ？？
      |    +-- IsADirectoryError: 在目录上进行文件操作时抛出。
      |    +-- NotADirectoryError: 在非目录上进行目录操作时抛出。
      |    +-- PermissionError: 尝试执行的操作系统权限不足时抛出。
      |    +-- ProcessLookupError: 当查询的进程不存在时抛出。
      |    +-- TimeoutError: 当某个系统级别的方法在系统层面上失败时抛出。
      +-- ReferenceError: 试图访问某个被系统回收的弱引用对象时抛出。
      +-- RuntimeError: 不属于其他类别的异常时抛出此异常
      |    +-- NotImplementedError: 当抽象类的抽象方法没有被实现或某个某个类仍在开发阶段表示某个功能实现尚未添加时抛出。
      |    +-- RecursionError: 递归超过系统限制次数时抛出。
      +-- SyntaxError: 出现python语法错误时抛出。
      |    +-- IndentationError: 出现python无法解析的不合理缩进时抛出。
      |         +-- TabError: 出现不一致地交替使用tab和空格时抛出。
      +-- SystemError: 编译器本身出现异常时抛出。
      +-- TypeError: 当进行操作的对象类型不合时抛出，例如传参类型不对等。
      +-- ValueError: 当某个操作或函数的参数类型正确但是值不合适时抛出。
      |    +-- UnicodeError: 当unicode相关的编码或解码错误出现时抛出。
      |         +-- UnicodeDecodeError: unicode编码错误时抛出。
      |         +-- UnicodeEncodeError: unicode解码错误时抛出。
      |         +-- UnicodeTranslateError: unicode翻译时抛出。
      +-- Warning
           +-- DeprecationWarning: 使用某些过时的特性时抛出的警告。
           +-- PendingDeprecationWarning: 使用某些即将过时的特性时抛出的警告。
           +-- RuntimeWarning: 可疑的运行时行为抛出的警告。
           +-- SyntaxWarning: 可疑的语句抛出的警告。
           +-- UserWarning: 由用户代码抛出的警告。
           +-- FutureWarning: 给python代码写的应用的用户发出的使用过时特性的警告。
           +-- ImportWarning: 导入时可能发生的错误的警告。
           +-- UnicodeWarning: 与unicode相关的警告。
           +-- BytesWarning: 与bytes和bytearray相关的警告。
           +-- ResourceWarning: 与资源使用有关的警告，会被默认警告过滤器过滤掉。
```
