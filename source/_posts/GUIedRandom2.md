---

title: 摇人机2007
date: 2022-05-15 19:50:34
tags: 
  - Python
  - 编程

---

## 一、前言与废话

书接[上文](https://chuishen.xyz/2022/05/14/GUIedRandom/)。这个玩意被我们班的人玩烂了，我"突发奇想"打算加点功能。

上次可能没把这个bonus.txt的功能讲清楚，bonus.txt的每一行都会被读取然后被random.sample函数读取，然后生成随机数。其实本来想要用更加复杂的算法生成抽人动画的，想想觉得没意思。

然后这次写了一下初始化（防止bonus.txt不存在）和整数数列生成。
<!--more-->
## 二、函数代码

### 数列生成器
```python
def generator(self):
    min = int(self.ui.min.toPlainText())
    max = int(self.ui.max.toPlainText())
    array = list(range(min,max+1))
    strarr = [str(x) for x in array]
    sth = "\n".join(strarr)
    with open('bonus.txt',"w") as f:
        f.write(sth)
```
### 比数列生成器更水的初始化，但是很有必要
```python
def first(self):
    f = open('bonus.txt', 'x')
    f.close()
# 没有这个初始化会出现chmod 777都拯救不了的BUG，
# 如 [WinError 5]
# 懂的大佬可以来说一下原因吗？
# 很不理解为什么老是会出现文件的权限错误
```

## 三、末语

这个项目的第二个版本的名字——摇人机2007其实是源于它的图标颇具Office 2007/Windows 7的风格。

PySide6的运行速度还是很慢……让人伤脑筋。难道要我去学C#吗……

土土收到这个更新之后很快就开始了测试，不知道结果如何，目前来看，应该没有几个大bug。

话说为什么我要给这么垃圾的程序更新，而不是之前说过要写的视频转换器……恐怕是因为我很懒吧。