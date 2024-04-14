---
title: Markdown转换器
date: 2022-07-13 21:51:45
tags: 
	- Python
	- 编程
---

## 零、紧跟时事

听说WPS塌房了，我的内心没有一丝波澜，毕竟一直在用Markdown写作，但是由于需要，还是要写一个方便的Markdown转换器。主要是为了方便手机阅读，其次则是方便给他人传阅。
<!--more-->
## 一、代码

下面是main.py的内容:

```python
import markdown
import pypandoc
from ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import sys
import os

def BabyMode():
    os.system("pip3 install pypandoc_binary")
    os.system("pip3 install PySide6")
    os.system("pip3 install markdown")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.mdopener.clicked.connect(self.opener)
        self.ui.transform.clicked.connect(self.trans)
        self.ui.trword.clicked.connect(self.tr2word)
        
    def opener(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "打开Markdown文件", ".", "*")
        self.file = filePath
        
    def trans(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            html = markdown.markdown(f.read())
        with open(self.file+".html","w") as f1:
            f1.write(html)
        QMessageBox.information(self, "完成！", "完成", QMessageBox.Ok)
    
    def tr2word(self):
        pypandoc.convert_file(self.file, 'docx', 'md', outputfile=self.file+'.docx')
        QMessageBox.information(self, "完成！", "完成", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

下面是ui.py的内容:
```python
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(210, 168)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.transform = QPushButton(self.centralwidget)
        self.transform.setObjectName(u"transform")
        self.transform.setGeometry(QRect(10, 90, 191, 32))
        self.mdopener = QPushButton(self.centralwidget)
        self.mdopener.setObjectName(u"mdopener")
        self.mdopener.setGeometry(QRect(10, 10, 191, 32))
        self.trword = QPushButton(self.centralwidget)
        self.trword.setObjectName(u"trword")
        self.trword.setGeometry(QRect(10, 50, 191, 32))
        self.trpdf = QPushButton(self.centralwidget)
        self.trpdf.setObjectName(u"trpdf")
        self.trpdf.setGeometry(QRect(10, 130, 191, 32))
        sizePolicy.setHeightForWidth(self.trpdf.sizePolicy().hasHeightForWidth())
        self.trpdf.setSizePolicy(sizePolicy)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Markdown\u8f6c\u6362", None))
        self.transform.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u5316\u4e3aHTML", None))
        self.mdopener.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00MD\u6587\u4ef6", None))
        self.trword.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u5316\u4e3aWord", None))
        self.trpdf.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u5316\u4e3aPDF", None))
```

## 二、结语

金山活该被骂，干的那点破事，大家众所周知。今天被拎出来骂一顿，是极好的事情，可以使它长长记性。WPS的服务本身就不好，加广告就算了，怎么能侵犯用户私人的数据呢？个人认为目前替代WPS的最好的解决方案应该是开源的软件，但这在商业与便民使用的领域又不现实。某种意义上来说，PDF应该是目前常规使用的最安全、最有效的办公易用格式了。