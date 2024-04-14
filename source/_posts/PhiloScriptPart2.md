---
title: 脚本哲学(2) WaterMello, 一款壬性化的《合成大西瓜》启动器
date: 2024-03-16 18:43:00
tags:
    - Minecraft
    - Python
    - 编程
---

## 前言
我们学校有一款由某位已经离校的学长开发的，基于《合成大西瓜》代码的，名为“合成校长”的游戏，风靡一时。许多人想要制作一个自定义版本。于是我就决定把这个当作一个脚本来写。
<!--more-->
## 解析
1. 介于主要用户（即同学们）不一定有使用命令行的经验，所以**设计一个GUI是有必要的**。
2. 此外，要能够直接启动游戏，意味着将**生成后的游戏可运行在本地服务器上**。
3. 另外，**要求用户提供裁剪到合适尺寸的圆形PNG文件，是不合实际的**(我对此深有感触)，所以要自动剪裁图片到合适尺寸和格式。
4. 另外需要多线程处理，防止程序未响应卡死。

## 代码
以下为 main.py 的内容，我们默认原版游戏的源代码放置在 ./original 文件夹 (建议前往 WaterMello 的 repo 下载)。
```python
import contextlib
import os
import random
import shutil
import socket
import sys
import webbrowser
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow
import cv2
from PIL import Image
from http.server import SimpleHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from functools import partial
from http.server import ThreadingHTTPServer
import threading


def start_thread(name, kwargs={}):
    thread = threading.Thread(target=name, kwargs=kwargs)
    thread.setDaemon(True)
    thread.start()

"规则：\n1. 图片从小到大排列。\n2. 生成按钮会在ready文件夹生成一个可以玩的版本的源文件；\n而部署按钮会将这个版本发送到站点上，让你可以在线上玩。"

class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

ext = ['.exr', '.webp', '.rgb', '.gif', '.pbm', '.pgm', '.ppm', '.tiff', '.rast', '.xbm', '.jpeg', '.bmp', '.png', '.webp', '.exr', '.jpg']
comparison = [52, 80, 108, 119, 153, 183, 193, 258, 308, 309, 408]
places = [
    "./ready/res/raw-assets/ad/ad16ccdc-975e-4393-ae7b-8ac79c3795f2.png",
    "./ready/res/raw-assets/0c/0cbb3dbb-2a85-42a5-be21-9839611e5af7.png",
    "./ready/res/raw-assets/d0/d0c676e4-0956-4a03-90af-fee028cfabe4.png",
    "./ready/res/raw-assets/74/74237057-2880-4e1f-8a78-6d8ef00a1f5f.png",
    "./ready/res/raw-assets/13/132ded82-3e39-4e2e-bc34-fc934870f84c.png",
    "./ready/res/raw-assets/03/03c33f55-5932-4ff7-896b-814ba3a8edb8.png",
    "./ready/res/raw-assets/66/665a0ec9-6c43-4858-974c-025514f2a0e7.png",
    "./ready/res/raw-assets/84/84bc9d40-83d0-480c-b46a-3ef59e603e14.png",
    "./ready/res/raw-assets/5f/5fa0264d-acbf-4a7b-8923-c106ec3b9215.png",
    "./ready/res/raw-assets/56/564ba620-6a55-4cbe-a5a6-6fa3edd80151.png",
    "./ready/res/raw-assets/50/5035266c-8df3-4236-8d82-a375e97a0d9c.png"
          ] #感谢来自于 liyupi 的源代码: https://github.com/liyupi/daxigua

def circle(img_path, cir_path):
    ima = Image.open(img_path).convert("RGBA")
    size = ima.size
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2))
    r3 = int(r2/2)
    imb = Image.new('RGBA', (r3*2, r3*2),(255,255,255,0))
    pima = ima.load()
    pimb = imb.load()
    r = float(r2/2)
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r)
            ly = abs(j-r)
            l = (pow(lx,2) + pow(ly,2))** 0.5
            if l < r3:
                pimb[i-(r-r3),j-(r-r3)] = pima[i,j]
    imb.save(cir_path)
    return cir_path

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = [""] * 11
        self.ui.Opener.clicked.connect(self.opening)
        self.ui.Deployer.clicked.connect(self.deploy)
        self.ui.Generator.clicked.connect(self.generate)
        self.ui.Activator.clicked.connect(self.activate)
        self.ui.About.clicked.connect(self.showAbout)
        self.ui.Remover.clicked.connect(self.remove)
        self.ui.Ruler.clicked.connect(self.rule)
        self.ui.Starter.clicked.connect(self.start)
        self.ui.Deployer.setEnabled(False)
        if os.path.exists("./tmp/"):
            self.ui.Starter.setEnabled(False)
        if os.path.exists("./ready/") == False:
            self.ui.Remover.setEnabled(False)
    
    def activate(self):
        def run(server_class=DualStackServer,
            handler_class=SimpleHTTPRequestHandler,
            port=8000,
            bind='127.0.0.1',
            cgi=False,
            directory=os.getcwd()
            ):
            """Run an HTTP server on port 8000 (or the port argument).

            Args:
                server_class (_type_, optional): Class of server. Defaults to DualStackServer.
                handler_class (_type_, optional): Class of handler. Defaults to SimpleHTTPRequestHandler.
                port (int, optional): Specify alternate port. Defaults to 8000.
                bind (str, optional): Specify alternate bind address. Defaults to '127.0.0.1'.
                cgi (bool, optional): Run as CGI Server. Defaults to False.
                directory (_type_, optional): Specify alternative directory. Defaults to os.getcwd().
            """
            if cgi:
                handler_class = partial(CGIHTTPRequestHandler, directory=directory)
            else:
                handler_class = partial(SimpleHTTPRequestHandler, directory=directory)
            with server_class((bind, port), handler_class) as httpd:
                webbrowser.open("http://127.0.0.1:8000")
                httpd.serve_forever()
        start_thread(run, kwargs={"directory": "./ready"})

    def rule(self):
        QMessageBox.information(self, "食用方法, 务必看完", """
初次启动需要“初始化”，之后不需要，然后“打开”一个装有11张图片的文件夹(其他什么都不要有)。
点击“生成”，然后等待跳出“已完成”提示窗口。
点击“启动”可启动游戏，部署功能还未写完，请勿使用。
生成完毕的游戏代码在"ready"文件夹中，请保管好。
如果要再次生成游戏，请点击“清除缓存”，这会导致上一次生成的游戏文件丢失，请保证自己已保管好。
                                """)
    def start(self):
        os.mkdir("./tmp")
        QMessageBox.information(self, "初始化完成", "初始化完成。")

    def remove(self):
        shutil.rmtree("./ready")
        QMessageBox.information(self, "已清除缓存", "已清除缓存。")

    def generate(self):
        def go():
            shutil.copytree(r'./original', r'./ready')
            for x in range(11):
                circle(self.file[x], "./tmp/"+str(x)+".png")
                img = cv2.imread("./tmp/"+str(x)+".png", cv2.IMREAD_UNCHANGED)
                img = cv2.resize(img, (comparison[x], comparison[x]))
                cv2.imwrite(places[x], img)
        start_thread(go)
    
    def showAbout(self):
        QMessageBox.information(self, "关于","""
WaterMello v0.1 Beta
开发: 玄云海 OblivionOcean
Special Thanks: liyupi, Fgaoxing.
Enjoy the game, thy life as well.
                                """)

    def opening(self):
        correction = True
        filepath = QFileDialog.getExistingDirectory(self, "打开装有11张图片的文件夹。", ".")
        files = os.listdir(filepath)
        for f in files:
            _, a = os.path.splitext(f)
            if a not in ext:
                correction = False
        if len(files) == 11 and correction:
            for i in files:
                self.file[files.index(i)] = os.path.join(filepath, i)
                print(self.file)
            QMessageBox.information(self, "成功！","已导入图片。")
        else:
            QMessageBox.information(self, "出错！","图片数量过多/过少，图片后缀名错误。")
    
    def deploy(self):
        QMessageBox.information(self, "我饿啦！","把这个功能吃了，下个版本还你们。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

以下为 ui_mainwindow.py 的内容。
```python
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(315, 113)
        icon = QIcon()
        icon.addFile(u"icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Opener = QPushButton(self.centralwidget)
        self.Opener.setObjectName(u"Opener")
        self.Opener.setGeometry(QRect(10, 50, 81, 41))
        self.Generator = QPushButton(self.centralwidget)
        self.Generator.setObjectName(u"Generator")
        self.Generator.setGeometry(QRect(90, 50, 71, 41))
        self.Deployer = QPushButton(self.centralwidget)
        self.Deployer.setObjectName(u"Deployer")
        self.Deployer.setGeometry(QRect(160, 50, 71, 41))
        self.Activator = QPushButton(self.centralwidget)
        self.Activator.setObjectName(u"Activator")
        self.Activator.setGeometry(QRect(230, 50, 71, 41))
        self.Starter = QPushButton(self.centralwidget)
        self.Starter.setObjectName(u"Starter")
        self.Starter.setGeometry(QRect(10, 10, 81, 41))
        self.Remover = QPushButton(self.centralwidget)
        self.Remover.setObjectName(u"Remover")
        self.Remover.setGeometry(QRect(230, 10, 71, 41))
        self.Ruler = QPushButton(self.centralwidget)
        self.Ruler.setObjectName(u"Ruler")
        self.Ruler.setGeometry(QRect(90, 10, 71, 41))
        self.About = QPushButton(self.centralwidget)
        self.About.setObjectName(u"About")
        self.About.setGeometry(QRect(160, 10, 71, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WaterMello", None))
        self.Opener.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
        self.Generator.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.Deployer.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u7f72", None))
        self.Activator.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8", None))
        self.Starter.setText(QCoreApplication.translate("MainWindow", u"\u521d\u59cb\u5316", None))
        self.Remover.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u7f13\u5b58", None))
        self.Ruler.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u89c4\u5219", None))
        self.About.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi
```

## 用例及仓库
用法见软件内部“食用方法”。

仓库地址：[GitHub](https://github.com/OblivionOcean/WaterMello)

## 后记
WaterMello 本身并没有受到关注，但是在班内，大伙非常喜欢我用它生成的“[合成哟西](https://yoxi.oblivionocean.top/)”小游戏(架设在玄云海域名上)，甚至已经有了班内竞赛，而我是最高分纪录保持者。

作为“自己的游戏”的最高分记录保持者，这值得骄傲吗？(笑)