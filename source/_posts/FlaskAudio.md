---

title: 利用Flask和ffmpeg制作简单的音乐转换器
date: 2022-05-14 09:50:34
tags: 
  - Python
  - 编程

---

## 一、前言与废话

我跟土土聊了一会天，然后我说：“要不我们俩写个音频转换器，用Python+Flask？”

“没问题。”

下午，我写完了。

土土懵了（说好一起写的呢Q w Q）。
<!--more-->
## 二、代码（python部分）

```python
import os
import pathlib
from pydub import AudioSegment
from flask import Flask, request, render_template

app = Flask(__name__)

def trans_any_audio_types(filepath, input_audio_type, output_audio_type):
    song = AudioSegment.from_file(filepath, input_audio_type)
    filename = filepath.split(".")[0]
    if os.getcwd() != "/Users/zhengwanlun/Desktop/Python/音乐转换器/static":
        print(os.getcwd())
        os.chdir('./static/')
    song.export(f"{filename}.{output_audio_type}", format=f"{output_audio_type}")

@app.route('/conv/')
def convert_page():
    with open('index.html') as f:
        html = f.read()
    return html

@app.route('/upload',methods=['POST'])
def upload():
    global file_extension
    f = request.files['file']
    file_extension = pathlib.Path(f.filename).suffix
    EXT = file_extension.strip('.')
    f.save('temp'+file_extension)
    trans_any_audio_types('temp'+file_extension,EXT,'mp3')
    return render_template('page1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
```

顺便一提，trans_any_audio_types函数是我改变自某个之前看到过的知乎的帖子里的，但是帖子好像没了。知道出处的可以留个言来帮我找到出处。

## 三、HTML部分

```html
<html>
<head>
  <title>File Upload</title>
</head>
<body>
    <form action="http://localhost:5000/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file"  />
        <input type="submit" value="提交" />
    </form>
</body>
</html>
```

其实这段没啥，也可以看出Python程序是在自娱自乐，HTML部分压根没参与一点动态的活。

## 四、末语

土土：啊，这么快就写完了，写个“迅捷转换器”之类的东西吧。

根据“和土土说过要写啥就能很快的写出来”的原则，下一个好像要做视频转换+Flask？个人觉得不会有人会用线上的视频和音频转换吧。这个音频转换已经足够不实用了，我还能写出什么更加不实用的东西？

还真能，社会课的老师说自己的U盘里原来的抽人软件里有病毒（你懂的，P2P下载器之类的），于是我要写一个班级抽人使用的带GUI的抽奖程序。这代码写着写着都出剧情了（笑）。这个时代已经充斥着许多同类型产品（对于这个项目来说，则是线上的随机数网站，它从各个方面上都可以碾压我的抽奖程序），但是有很多人就是看不到，我想要送给一些人这样一句话。

“带着会不会发现什么有用的东西的想法来看，这样是不会注意到真正有用的东西的。”

——ZUN