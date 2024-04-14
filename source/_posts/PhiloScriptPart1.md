---
title: 脚本哲学(1) Minecraft 服务器区块与备份脚本
date: 2024-03-16 18:42:30
tags:
    - Minecraft
    - Python
    - 编程
    - 关于我自己
---

## 开始之前
我好久没写技术类的推文了，原因很简单，我有些跟不上大伙的节奏，我技术力过于低下。但仔细想想，发一些技术文章还是可以精进自己的技术的，于是便打算重新开始，于是就有了这么一个新系列，叫做“脚本哲学”。

另外，在最新的决定中，我将这个博客分为了三个网站，一个是本站，主要发技术文章；一个是 [Legacy](https://legacy.chuishen.xyz/)，是旧物的堆积地；以及 [Memoria](https://memoria.top/) ，是我与远冬的文学博客。《御伽之国的鬼岛》《白银树之恋》等文章已被迁至 Legacy。《日记八集》中的部分篇目，已被永久删除。
<!--more-->
## 要求与解析
这次是接了一位好朋友的单，他的要求很简单，每隔6小时，将 world 文件夹的每一个变动的文件都复制到 backup 文件夹的压缩包中以达成备份。

那么首先是造个backup文件夹（如果已存在还要处理错误），用 watchdog 看着，然后再在每一次侦测到 Snapshot 改变的时候复制到 backup 文件夹的 zip 文件里。非常轻松。

代码部分如下：

```python
import time
import os
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import zipfile
import sys
import threading

class HD(watchdog.events.FileSystemEventHandler):
    def __init__(self, aim_path):
        super().__init__()
        self.timer = None
        self.aim_path = aim_path
        self.snapshot = DirectorySnapshot(self.aim_path)
        self.second = 120

    def checkSnapshot(self):
        snapshot = DirectorySnapshot(self.aim_path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None
        if not os.path.exists("./backup"):
            os.mkdir("./backup")
        zip_file = zipfile.ZipFile('./backup/%s.zip' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())),'w')
        for x in diff.files_modified:
            print(x)
            zip_file.write(x, compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()

    def on_modified(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(120, self.checkSnapshot)
        self.timer.start()

def observe(path="./observing", timer=120):
    observer = Observer()
    observer.start()
    event_handler = HD(path)
    event_handler.second = timer
    observer.schedule(event_handler, path, recursive=True)
    try:
        while True:
            time.sleep(timer)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    observe(path=sys.argv[1], timer=int(sys.argv[2]))
```

## 用例及仓库
```shell
python3 main.py {侦测的目录} {Snapshot间隔时间}
```

仓库地址：(GitHub)[https://github.com/Lafcadia/MCServerBackup]

## 后记
脚本需要可复用性，为了省事而直接在脚本中设定 path 和 Snapshot 时间间隔是不可取的。

顺带一提，我得蹲着服务器等好几个小时才能知道这东西到底有没有生效，当然最终的结果是有效。就目前而言，朋友疑似相当满意，证明了它的效果还不错。
