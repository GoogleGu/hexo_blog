---
title: python正则表达式
date: 2019-11-27 19:30:01
tags:
    - python module
---


## 1. 基本知识

在python中，处理正则表达式的包是re。re提供包级的正则处理函数，也支持把正则表达式编译成正则对象，在正则对象上调用实例方法进行正则匹配。
在进行正则匹配时，最好把代表正则表达式的字符串以raw string的形式传入，使用raw string时不需要对 # todo
<!-- more -->
## 2. 进行正则操作的函数/方法

### 搜索第一次匹配的search

`search(pattern, string, flags=0)`
search会对string进行搜索，返回首次匹配到pattern的match对象；如果没有匹配的话，则返回None。

```python
>>> re.search(r'\d+', 'a1b2c3d4e5f')
<_sre.SRE_Match object; span=(1, 2), match='1'>   # match对象
```

### 搜索头匹配的match

`match(pattern, string, flags=0)`
和search类似，不过更加严格，只会在字符串开头搜索匹配，如果匹配的内容不在开头则视为无匹配。

```python
>>> re.match(r'[abc]+', 'a1b2c3d4e5f')
<_sre.SRE_Match object; span=(0, 1), match='a'>   # match对象
>>> re.match(r'\d+', 'a1b2c3d4e5f')
# 无匹配，返回None
```

### 搜索完全匹配的fullmatch

`fullmatch(pattern, string, flags=0)`
比search更严格，只有目标字符串整个完全与正则表达式匹配时返回match对象，否则返回None。

```python
>>> re.fullmatch(r'\w+', 'a1b2c3 d4e5f')
# 不是完全匹配，返回None

>>> re.fullmatch(r'(\w| )+', 'a1b2c3 d4e5f')
<_sre.SRE_Match object; span=(0, 12), match='a1b2c3 d4e5f'>  # 完全匹配
>>> re.fullmatch(r'\w|+| ', 'a1b2c3 d4e5f')
# 分段完全匹配，依然返回None，必须一次全部匹配到才行
```

### 多次匹配的findall

`findall(pattern, string, flags=0)`
会对目标字符串用正则式进行多次的不重叠的匹配，各次匹配到的字符串内容依次存在一个list中返回，如果没有匹配则返回空列表。

```python
>>> re.findall(r'\w+', 'Words, words, words.')
['Words', 'words', 'words']
>>> re.findall(r'\d+', 'Words, words, words.')
[]
```

另外还有一个方法`finditer(pattern, string, flags=0)`版本，与findall类似，但是返回的一个生成器，每次迭代返回一次匹配内容的match对象。

### 切割字符串的split

`split(pattern, string, maxsplit=0, flags=0)`
与str.split类似，但是更为强大：可以接受一个正则表达式为分割点，在所有匹配的地方将原字符串切断，将切割后的各个片段存入list中返回。如果在正则中有捕获组的话，会把捕获组匹配到的字符串也存入结果list中。

```python
>>> re.split(r'\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
>>> re.split(r'(\W+)', 'Words, words, words.')
# 有捕获组，捕获组也被存到了结果list中，如果捕获组匹配到了字符串结尾，返回的list最后一个元素将是空字符串，如果匹配到了开头，返回的list首个元素将是空字符串。
['Words', ', ', 'words', ', ', 'words', '.', '']  
```

### 替换字符串的sub

`re.sub(pattern, repl, string, count=0, flags=0)`
返回一个新字符串，将每次匹配的内容替换为repl，不会改动原字符串string。如果没有匹配的话，原样返回字符串string。

```python
>>> re.sub('\w', '@', 'Words, words, words.')
'@@@@@, @@@@@, @@@@@.'
```

这里的repl可以传入一个函数而不是字符串，如果传入的是函数，该函数在每次要进行替换时被调用，该函数的入参是match对象，返回的字符串将被替换进匹配的地方。

```python
>>> def dashrepl(matchobj):
>>>     ''' 如果匹配到一个-，则返回空格，否则返回一个- '''
>>>     if matchobj.group(0) == '-': return ' '
>>>     else: return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'
```

另外还有一个subn版本，与sub使用一样，但是返回结果是一个元组，其内容为(替换后的字符串，进行替换的次数)

## 3. 正则表达式对象

### 3.1. 正则表达式对象

`compile(pattern, flags=0)`
pattern为正则表达式字符串，flags的用法 # todo
所有可以以re.func的方式调用的正则处理函数都可以以实例方法的形式在正则对象上调用，调用方式几乎是一样的。

```python
>>> string = '12345'
>>> pattern = r'\d+'
>>> prog = re.compile(pattern)
>>> result = prog.match(string)
<_sre.SRE_Match object; span=(0, 5), match='12345'>   # match对象
```

### 3.2. match对象

很多正则函数进行匹配后会返回match对象，对match对象进一步操作才能获得需要的字符串内容等，以下是match对象一些有用的属性和方法。

#### 获取指定匹配组group()

`Match.group([group1, ...])`
返回一个或多个匹配结果的子组。如果传入一个数字，则返回对应子组的字符串，如果传入多个，则返回对应各个子组字符串组成的元组。如果不传参，默认为取第0组，也即整个匹配结果对应的字符串。

```python
>>> m = re.match(r"(\w+), (\w+)", "Waterdeep, City")
>>> m.group(0)       # 返回整个匹配组
'Waterdeep, City'
>>> m.group(1)
'Waterdeep'
>>> m.group(2)
'City'
>>> m.group(1,2)
('Waterdeep', 'City')
```

如果正则中对捕获组用`(?P<name>...)`语法进行了命名，则可以在group中传入捕获组名字而不是数字。

```python
>>> m = re.match(r"(?P<name>\w+), (?P<type>\w+)", "Waterdeep, City")
>>> m.group('name')
'Waterdeep'
>>> m.group('type')
'City'
```

如果同一个捕获组捕获到多次，只有最后一次捕获可以被单独获取到。

```python
>>> m = re.match(r"(..)+", "a1b2c3")
>>> m.group(1)
'c3'
```

#### 获取所有匹配组groups()

`Match.groups(default=None)`
返回所有的捕获组，如果没有匹配到的捕获组会置为None，或是传入的default值。

```python
>>> m = re.match(r"(\d+)\.?(\d+)?", "24")
>>> m.groups()
('24', None)
>>> m.groups('0')  
('24', '0')
```

#### 返回所有命名捕获组的groupdict()

`Match.groupdict(default=None)`
返回所有的命名捕获组名字与捕获内容组成的字典。

```python
>>> m = re.match(r"(?P<name>\w+), (?P<type>\w+)", "Waterdeep, City")
>>> m.groupdict()
{'name': 'Waterdeep', 'type': 'City'}
```

## 4. 备忘：python正则表达式语法

```txt
| 或
(?P<name>...) 对捕获组命名为name，如果不加的话，捕获组用\1,\2来获取
content(?=lookaround) content后面是lookaround，返回content
content(?!lookaround) content后面不是lookaround，返回content
(?<=lookaround)content content前面是lookaround，返回content
(?<!lookaround)content content前面不是lookaround，返回content
```

**匹配内容**
匹配内容的正则所对应的内容会出现在匹配结果中。

```
\d 一位数字
\D 一位非数字
\w 一个字母或数字
\W 一个非字母非数字字符
\s 一个空白字符
\S 一个非空白字符
. 任何字符
[abcd] a或b或c或d
[^abcd] 不是a、b、c、d
```

**匹配数量**
python中，默认使用贪婪的匹配模式，要改用保守模式需要在数量表达式后加上`?`，比如`*?`

```txt
* 任意个
+ 一个以上
? 0个或1
{m} m个
{m, } m到无限个
{m, n} m到n个
```

**匹配限制**
匹配限制所匹配的是类似于边界的内容，对应的内容不会保存到匹配结果中。

```txt
\b 一个词语边界
\B 一个非词语边界
^ 字符串开头
$ 字符串结尾
```
