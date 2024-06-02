---

title: 利用 Flask 和 Captcha 制作简单的验证码生成器
date: 2022-05-14 09:50:34
tags: 
  - Python
  - 编程

---

## 一、前言与废话

多年之前，我曾经给土土发过一个神奇的本地验证码生成器。当时我有一个习惯，写什么都要加个GUI，但是因为我想想觉得验证码生成器没必要有GUI，所以就没写。但是我写了一个叫BabyMode的函数，这个函数其实很简单，就是在Module无法导入的时候把所有模块全都下载安装一遍（用pip）。这个函数后来成为了我们俩之间的梗。
<!--more-->
土土后来写了一个Flask实现的验证码生成器，我觉得自己很菜，连Flask都不会还学个啥Python，所以我当天就写出了验证码生成器（话说这样不算内卷吧），还学会了很多东西，果然竞争的存在是提高自己学习能力的必要条件。

## 二、代码

```python
from captcha.image import ImageCaptcha
from flask import Flask, render_template, request
import string
import random

app = Flask(__name__)
imgsrc = '<img src="https://www.z4a.net/images/2022/05/03/%s.png" loading="eager" border="0">'

def generator(name="code.png"):#ImageCaptcha库实现的验证码生成，之前和土土用的是我自己写的算法，回头看看不堪入目
    token = string.digits + string.ascii_letters
    cap = random.sample(token,8)
    token_str = ''.join(cap)
    img = ImageCaptcha(width=400,height=150)
    image = img.generate_image(token_str)
    image.save(name)
    return token_str

@app.route('/', methods=['GET','POST'])
def index():
  	#index.html，分GET和POST，我把输入验证码和验证码正确错误的返回坐在一起了，debug的时候只需要重新进入网页就可以重新开始测试
    global real_str
    if request.method == 'POST':
        result = request.form
        r = result.get('yanzheng').lower() == real_str.lower()
        if r:
            return imgsrc % '183127ad86d33bc4a.md'
        else:
            return imgsrc % '2731445bae82f42e5'
    else:
        with open("index.html") as f:
            content = f.read()
        return content

@app.route('/code.png')
def view():#显示code.png，其实这个函数写的很烂，会的都知道可以怎么写来提升代码整体质量
    global real_str
    real_str = generator()
    with open('code.png', 'rb') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='2333') #启动服务器
```

## 三、使用方法

打开程序，打开浏览器，输入localhost:2333。

或者你是一个聪明人，你可以从代码或者注释中自己找到该干嘛。

如果是大佬的话，那我只能说，这篇文章对您几乎毫无营养，如果您不喜欢这种风格的代码分享，请慎重考虑要不要继续浏览本博客的其他内容。