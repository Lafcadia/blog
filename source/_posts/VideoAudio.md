---
title: 视音频转换器
date: 2022-07-13 21:50:40
tags:
	- Python
	- 编程

---

## 零、前言

前面其实说过了，我要做视音频转换器，终于在旅途的车上挤出来了这段代码。

土土作为头号测试员（小白鼠），表示非常满意。
<!--more-->
## 一、代码

以下是main.py的代码:

```python
import sys
import pathlib
from pydub import AudioSegment
from gui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PySide6 import QtCore
import cv2

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
MUSIC = ["MP3", "FLAC", "WAV", "OGG", "WMA", "M4A"]
VIDEO = ["MP4", "FLV", "MOV", "WMV", "AVI"]
loadtext = """食用说明: 
1. 文件的保存位置一般为原文件位置。
2. 部分格式之间的互换未经过完整测试。
3. 支持视频转视频，视频转音频，音频转音频。
4. 请勿作死尝试将音频转成视频。
5. 未在Windows/Linux上经过测试，理论上支持这两个平台。
6. 有bug可反馈至作者博客: https://chuishen.xyz/。
7. 请通过源代码安装的用户自行安装ffmpeg。地址: https://ffmpeg.org/。
8. 支持导出的文件格式有: MP3, FLAC, WAV, OGG, WMA, M4A, MP4, FLV, MOV, WMV, AVI等，支持导入的文件格式更加多样，且未来将支持更多导出格式。"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.TransNow.clicked.connect(self.tran)
        self.ui.ChooseFile.clicked.connect(self.choicebox)
        self.filename = None
        self.func = None
        QMessageBox.information(self, "食用说明", loadtext, QMessageBox.Ok)

    def fext(self, f):
        file_extension = pathlib.Path(f).suffix
        EXT = file_extension.strip('.')
        return EXT
    
    def to_video(self, filepath, input_type, output_type):
        try:
            cap = cv2.VideoCapture(filepath)
            frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            weight = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            size = (weight, height)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filepath+"."+output_type, fourcc, fps, size)
            for n in range(frame_cnt):
                _, frame = cap.read()
                out.write(frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            cap.release()
            out.release()
            return 1
        except:
            return 0
    
    def to_audio(self, filepath, input_type, output_type):
        try:
            song = AudioSegment.from_file(filepath)
            print(song)
            filename = filepath.split(".")[-2]
            song.export(f"{filename}.{output_type}", format=f"{output_type}")
            return 1
        except Exception as e:
            return 0
    
    def choicebox(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "选择音乐、视频", ".", "*")
        self.file = filePath

    def tran(self):
        text = self.ui.comboBox.currentText()
        suffix = self.fext(self.file).upper()
        if text in MUSIC:
            self.func = self.to_audio
        elif text in VIDEO:
            self.func = self.to_video
        if self.func(self.file, suffix, text) == 0:
            QMessageBox.information(self, "出错啦!", "出错啦!请检查配置与输入有无错误。", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "成功!", "成功!", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

以下是gui.py的代码:

```python
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(302, 108)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(70, 60, 101, 31))
        font = QFont()
        font.setFamilies([u"Weibei SC"])
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        self.comboBox.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 60, 71, 31))
        font1 = QFont()
        font1.setFamilies([u"Weibei SC"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.label.setFont(font1)
        self.TransNow = QPushButton(self.centralwidget)
        self.TransNow.setObjectName(u"TransNow")
        self.TransNow.setGeometry(QRect(180, 60, 111, 41))
        font2 = QFont()
        font2.setFamilies([u"Weibei SC"])
        font2.setPointSize(24)
        font2.setBold(True)
        self.TransNow.setFont(font2)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 211, 41))
        font3 = QFont()
        font3.setFamilies([u"Weibei SC"])
        font3.setPointSize(24)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setStrikeOut(False)
        self.label_2.setFont(font3)
        self.ChooseFile = QPushButton(self.centralwidget)
        self.ChooseFile.setObjectName(u"ChooseFile")
        self.ChooseFile.setGeometry(QRect(180, 10, 111, 41))
        self.ChooseFile.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Van能转换器", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"MP4", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"MP3", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"FLV", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"MOV", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"FLAC", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"OGG", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"WMA", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"AVI", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"WMV", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"WAV", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"M4A", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u5316\u4e3a\uff1a", None))
        self.TransNow.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Van\u80fd\u8f6c\u6362\u5668", None))
        self.ChooseFile.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
```

## 二、结语

我对于某些很无聊的线上转换网站感到很不快，明明是「免费」的，却要加广告，上传下载速度都慢，结果到最后下载的时候一个503代码，浪费了我生命中的十分钟。

我之所以一直在做轻量的实用工具，实际上也只是因为现在的服务太臃肿，我和某些人需要而已，事实上，很多人可以忍受这种虚假的免费，但我们不能。