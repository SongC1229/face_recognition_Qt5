# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
# import sys
import time
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QBrush, QPixmap


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, filename):
        super(QtWidgets.QDialog, self).__init__()
        self.filename = filename
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(645, 484)
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 645, 485))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.scene = QtWidgets.QGraphicsScene()
        p = QtGui.QPixmap()
        p.load(self.filename)
        item = QtWidgets.QGraphicsPixmapItem(p)
        self.graphicsView.scene.addItem(item)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "图像信息"))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 580)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 10, 90, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(380, 10, 90, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(730, 10, 90, 30))
        self.label_3.setObjectName("label_3")
        self.listView = QtWidgets.QListWidget(Form)
        self.listView.setGeometry(QtCore.QRect(30, 45, 330, 500))
        self.listView.setObjectName("listView")
        self.listView.itemDoubleClicked.connect(self.showpic)
        self.listView_2 = QtWidgets.QListWidget(Form)
        self.listView_2.setGeometry(QtCore.QRect(380, 45, 330, 500))
        self.listView_2.setObjectName("listView_2")
        self.listView_2.itemDoubleClicked.connect(self.showunpic)
        self.listView_3 = QtWidgets.QListWidget(Form)
        self.listView_3.setGeometry(QtCore.QRect(730, 45, 330, 500))
        self.listView_3.setObjectName("listView_3")
        self.listView_3.itemDoubleClicked.connect(self.showshotpic)

        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setDigitCount(10)
        self.lcdNumber.setGeometry(QtCore.QRect(900, 10, 150, 30))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.display(time.strftime("%X", time.localtime()))

        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(),
                          QBrush(QPixmap('img/2.jpg')))  # 设置背景图片
        self.setPalette(palette1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def showshotpic(self):
        filename = "result/shotpic/" + \
            self.listView_3.item(self.listView_3.currentRow()).text() + ".jpg"
        imgDialog = Ui_Dialog(filename)
        imgDialog.exec_()

    def showpic(self):
        filename = "result/guest/" + \
            self.listView.item(self.listView.currentRow()).text() + ".jpg"
        imgDialog = Ui_Dialog(filename)
        imgDialog.exec_()

    def showunpic(self):
        filename = "result/warning/" + \
            self.listView_2.item(self.listView_2.currentRow()).text() + ".jpg"
        #print(filename)
        imgDialog = Ui_Dialog(filename)
        imgDialog.exec_()

    def init_shot(self):
        knownpath = "result/shotpic/"
        self.listView_3.clear()
        for filename in os.listdir(knownpath):
            self.listView_3.addItem(filename[:-4])

    def init_guest(self):
        knownpath = "result/guest/"
        self.listView.clear()
        for filename in os.listdir(knownpath):
            self.listView.addItem(filename[:-4])

    def init_unknown(self):
        knownpath = "result/warning/"
        self.listView_2.clear()
        for filename in os.listdir(knownpath):
            self.listView_2.addItem(filename[:-4])

    def init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        self.lcdNumber.display(time.strftime("%X", time.localtime()))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "监控记录"))
        self.label.setText(_translate("Form", "访客"))
        self.label_2.setText(_translate("Form", "陌生人"))
        self.label_3.setText(_translate("Form", "抓拍照片"))


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_Form()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     app.exec_()
