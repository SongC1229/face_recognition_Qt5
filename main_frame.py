# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(680, 30, 136, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.init_people_info = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.init_people_info.setObjectName("init_people_info")
        self.verticalLayout.addWidget(self.init_people_info)
        self.start_monitor = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.start_monitor.setObjectName("start_monitor")
        self.verticalLayout.addWidget(self.start_monitor)
        self.see_info = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.see_info.setObjectName("see_info")
        self.verticalLayout.addWidget(self.see_info)
        self.stop_monitor = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stop_monitor.setObjectName("stop_monitor")
        self.verticalLayout.addWidget(self.stop_monitor)
        self.shotpic = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.shotpic.setObjectName("shotpic")
        self.verticalLayout.addWidget(self.shotpic)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 645, 485))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.scene = QtWidgets.QGraphicsScene()
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setDigitCount(10)
        self.lcdNumber.setGeometry(QtCore.QRect(670, 20, 151, 31))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.display(time.strftime("%X", time.localtime()))
        self.init_timer()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        p = QtGui.QPixmap()
        p.load('img/219.jpg')
        self.setinitimage(p)
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(
            QPixmap('img/83.jpg')))  # 设置背景图片
        self.setPalette(palette1)

    def init_timer(self):
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.start()
        self.timer1.timeout.connect(self.update_time)

    def update_time(self):
        self.lcdNumber.display(time.strftime("%X", time.localtime()))

    def setinitimage(self, p):
        item = QtWidgets.QGraphicsPixmapItem(p)
        self.graphicsView.scene.clear()
        self.graphicsView.scene.addItem(item)
        self.graphicsView.setScene(self.graphicsView.scene)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "监控中心"))
        self.init_people_info.setText(_translate("MainWindow", "更新信息"))
        self.start_monitor.setText(_translate("MainWindow", "开始监控"))
        self.see_info.setText(_translate("MainWindow", "查看记录"))
        self.stop_monitor.setText(_translate("MainWindow", "停止监控"))
        self.shotpic.setText(_translate("MainWindow", "抓拍图像"))
