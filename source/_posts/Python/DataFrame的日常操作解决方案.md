---
title: DataFrame的日常操作解决方案
date: 2019-11-25 20:23:57
tags: 
    - python module
---

## INSERT ROW 增加一行数据

### loc（不推荐）

```python
df = DataFrame(columns=('lib', 'qty1', 'qty2'))
for i in range(5):
    df.loc[i] = [randint(-1,1) for n in range(3)]
print(df)
#     lib  qty1  qty2
# 0    0     0    -1
# 1   -1    -1     1
# 2    1    -1     1
# 3    0     0     0
# 4    1    -1    -1
```

loc方法可以接受一个列index，获取该index对应的列记录。其使用方法与字典的`sample['12']`类似，也支持对原本不存在的index进行赋值。
**优点**：操作简便，和字典的操作习惯类似。
**缺点**：如果已存在该index的话，就会造成数据替换。可能会报warning：A value is trying to be set on a copy of a slice from a DataFrame。

### append（推荐）

```python
import pandas as pd
from numpy.random import randint
df = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
for i in range(5):
    s = pd.Series({'lib':randint(-1,1), 'qty1':randint(-1,1), 'qty2':randint(-1,1)})
    # 这里 Series 必须是 dict-like 类型
    df = df.append(s, ignore_index=True)
```

append方法接受一个与DataFrame中column一致的Series对象，将其添加到尾端，效果和list的append使用方法类似。另外，如果这个被插入的Series对象没有设置index值的话，必须将append方法的ignore_index参数设为True。
**优点**：操作简便，和列表的操作习惯类似。性能略优于loc方法。
**缺点**：无。

## INSERT COLUMN 增加一列数据

### loc（不推荐）

```python
# 准备数据
import pandas as pd
from numpy.random import randint
df = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
for i in range(5):
    s = pd.Series({'lib':randint(-1,1), 'qty1':randint(-1,1), 'qty2':randint(-1,1)})
# 增加列
sLength = len(df2['a'])
d = pd.Series(np.random.randn(sLength))
df.loc[:, 'qty3'] = d # 如果d是Series的话，赋予新列时会按index将d中的值赋值到新列中，如果是list的话，则依次赋值，没有index对应
```

**缺点**：可能会报warning：A value is trying to be set on a copy of a slice from a DataFrame。

### assign（推荐）

```python
# 准备代码与loc中一样，以下为插入代码
sLength = len(df2['a'])
d = pd.Series(np.random.randn(sLength))
df.assign(d1=d) # 如果d是Series的话，赋予新列时会按index将d中的值赋值到新列中，如果是list的话，则依次赋值，没有index对应
```

**优点**：稳定不会报错，是官方推荐的处理方式。
**缺点**：无
[该方法的官方文档](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.assign.html)

## SELECT WHERE 根据行字段值选择记录

### bool索引

```python
import pandas as pd
# 准备数据
d = {'foo':[100, 111, 222],
     'bar':[333, 444, 555]}
df = pd.DataFrame(d)
# df:
#    bar   foo
# 0  333   100
# 1  444   111
# 2  555   222

# bool 值索引
df[[True, False, True]] # 或 df.loc[[True, False, True]]
# 都可以得到
#   bar foo
#0  333 100
#2  555 222
```

DataFrame的索引可以为bool值的序列来选取数据行（但是该序列的长度必须和DataFrame中的行数相等，否则会报错ValueError。
bool选择语法：

- 列值等于某个值为筛选条件: `df[df['column_name'] == some_value]` 如果是数值型，也可以采用`>`和`<`
- 列值等于某几个值中的一个: `df[df['column_name'].isin(some_values)]` some_values 可以是单个变量，也可以是list 或者迭代器。
- 多个筛选条件：`df[(df['column_name' == some_value) & (df['column_name'].isin(some_values)]`。注意&和|的优先级高于==，要给每个条件加括号。
- 不等于或某个值的筛选：`df[df['column_name'] != some_value]`和`df[~df['column_name'].isin(some_values)]`

**优点**：性能高
**缺点**：代码可读性略差

### query

```python
n = 10
df = pd.DataFrame(np.random.randint(n, size=(n, 2)), columns=list('bc'))
#    b  c
# 0  9  0
# 1  1  2
# 2  2  4
# 3  7  6
# 4  6  4
# 5  4  7
# 6  2  9
# 7  4  8
# 8  6  2
# 9  9  0

df.query('index > b > c')
#   b   c
# 8 6   2

#可以采用的表达式很多,比如
df.query('(a < b) & (b < c)')
df.query('a < b and b < c')
df.query('color == "red"')
```

**优点**：官方的推荐方法，可读性更好。
**缺点**：性能比起bool索引稍微差一些。
[query方法的官方文档](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.query.html?highlight=query#pandas.DataFrame.query)

## 查重

### duplicated和drop_duplicates

```python
# 准备数据
df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'two', 'two', 'three', 'four'],
                    'b': ['x', 'y', 'x', 'y', 'x', 'x', 'x'],
                    'c': np.random.randn(7)})
df2
#       a   b   c
# 0    one  x  1.469359
# 1    one  y -0.509652
# 2    two  x -0.438074
# 3    two  y -1.252795
# 4    two  x  0.777490
# 5  three  x -1.613898
# 6   four  x -0.212740
df2.duplicates('a')
df2.duplicates(['b'], keep='last')
df2.duplicates(['a', 'b'])
df2.duplicates(['a', 'b'], 
```

duplicate方法返回与原DataFrame行数相等的bool序列，指明对应的行是否是重复数据，可以用于传入DataFrame的索引进行数据过滤。
duplicated方法则会移除重复数据。
默认会保留重复数据中的第一个，可以通过给keep参数赋值为'last'保留最后一个或False来丢弃所有重复数据。
[drop_duplicates的官方文档](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop_duplicates.html?highlight=drop_duplicate)

## 参考文章

- [Comparison with SQL](http://127.0.0.1:53366/Dash/raultaft/doc/comparison_with_sql.html)
- [跟着stackoverflow学Pandas：add one row in a pandas.DataFrame -DataFrame添加行](https://blog.csdn.net/tanzuozhev/article/details/76735660)
