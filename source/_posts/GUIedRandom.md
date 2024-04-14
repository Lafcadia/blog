---

title: 利用PySide2和random模块制作简单的摇人机
date: 2022-05-14 09:50:34
tags: 
  - Python
  - 编程

---

## 一、前言与废话

这次是我在学校里写的，所以没有我和土土的废话。

我感觉我透过镜子看事物，仿佛一切都是那么的真实，但是却触摸不到事情的本质，因此，这镜子使我目盲。

直到我发现这镜子是我眼睛中的晶状体。
<!--more-->
## 二、代码（主体部分）

```python
import random
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtCore
from ui import Ui_MainWindow

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.solve)

    def solve(self):
        num = int(self.ui.inputer.toPlainText())
        with open('bonus.txt') as f:
            data = f.read().split('\n')
        samples = random.sample(data, num)
        self.ui.outputer.setText(";".join(samples))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

写这个的时候，在听的是“飞翔在空中的不可思议的巫女的每日”。真是美妙的曲子，让人感觉卸下了眼睛，只用耳朵感受天空的世界。

## 三、UI部分

```python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 368)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(9, 9, 192, 72))
        font = QFont()
        font.setFamily(u"\u54e5\u7279\u5f0f\u5b57\u4f53")
        font.setPointSize(48)
        self.label.setFont(font)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(11, 308, 481, 34))
        font1 = QFont()
        font1.setFamily(u"\u65b9\u6b63\u7c97\u9ed1\u5b8b\u7b80\u4f53")
        font1.setPointSize(16)
        self.pushButton.setFont(font1)
        self.outputer = QTextBrowser(self.centralwidget)
        self.outputer.setObjectName(u"outputer")
        self.outputer.setGeometry(QRect(10, 201, 482, 101))
        font2 = QFont()
        font2.setFamily(u"8514oem")
        font2.setPointSize(28)
        self.outputer.setFont(font2)
        self.outputer.setCursorWidth(0)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(9, 87, 120, 25))
        font3 = QFont()
        font3.setFamily(u"\u65b9\u6b63\u7c97\u9ed1\u5b8b\u7b80\u4f53")
        font3.setPointSize(15)
        self.label_2.setFont(font3)
        self.inputer = QPlainTextEdit(self.centralwidget)
        self.inputer.setObjectName(u"inputer")
        self.inputer.setGeometry(QRect(9, 118, 482, 41))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 170, 120, 25))
        self.label_3.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6447\u4eba\u673a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6447\u4eba\u673a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u6447\u4eba\u55bd", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8981\u6447\u51e0\u4e2a\u4eba\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6447\u51fa\u6765\u7684\u4eba\uff1a", None))
    # retranslateUi
```

## 四、末语

土土在帮我测试代码的时候，因为他使用的是装载M1芯片的MacBook Air，装不了PySide2，所以我把所有的PySide2改成了PySide6。

代码照常运行。（neta自《太阳照常升起》）