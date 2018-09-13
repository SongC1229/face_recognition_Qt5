from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
from main_frame import Ui_MainWindow
import datetime
import threading
from face_recognition import load_image_file, face_locations, face_encodings, compare_faces
import numpy as np
import cv2
from recording import *
import sys
import requests


class SaveGuestProcess(threading.Thread):

    def __init__(self, frame, name):
        threading.Thread.__init__(self)
        self.frame = frame
        self.name = name

    def trigger_hello(self):

        url = "http://192.168.1.6/pwm.cgi?status=0"
        r = requests.get(url)
        print("回传信息，hello")

    def run(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        filename = str(nowTime) + self.name + ".jpg"
        cv2.imwrite("result/guest/" + filename, self.frame)
        print("save guest info finished:", self.name)
        self.trigger_hello()


class SaveWarningProcess(threading.Thread):

    def __init__(self, frame):
        threading.Thread.__init__(self)
        self.frame = frame

    def trigger_warning(self):

        url = "http://192.168.1.6/pwm.cgi?status=1"
        r = requests.get(url)
        print("回传信息，开启警报")

    def run(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        filename = str(nowTime) + ".jpg"
        cv2.imwrite("result/warning/" + filename, self.frame)
        print("save waring info finished")
        self.trigger_warning()


class record_frame(QtWidgets.QWidget, Ui_Form):
    # 从自动生成的界面类继承
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def show_w2(self):  # 显示窗体2
        self.init_timer()
        self.init_guest()
        self.init_unknown()
        self.init_shot()
        self.show()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.init_people_info.setIcon(QIcon("img/info.png"))
        self.init_people_info.clicked.connect(self.re_init_people_info)
        self.start_monitor.clicked.connect(self.start_monitor_fun)
        self.start_monitor.setIcon(QIcon("img/start.png"))
        self.stop_monitor.clicked.connect(self.stop_monitor_fun)
        self.stop_monitor.setIcon(QIcon('img/stop.png'))
        # self.see_info.clicked.connect(self.see_info_fun)
        self.see_info.setIcon(QIcon("img/see.png"))
        self.shotpic.setIcon(QIcon('img/camera.png'))
        self.shotpic.clicked.connect(self.shotpic_fun)
        self.timer_camera = QTimer(self)
        self.timer_camera.timeout.connect(self.show_pic)
        self.cap = ''
        self.ismot = False
        self.namelist = []
        self.infolists = []
        self.sum_unknown = 0
        self.sum_known = {}
        self.isprocess = False
        self.issave = False

    def shotpic_fun(self):
        if self.ismot:
            self.issave = True
        else:
            QMessageBox.information(
                self, "监控未开启", "请开启监控后抓拍。", QMessageBox.Yes)

    def start_monitor_fun(self):
        if not self.ismot:
            self.cap = cv2.VideoCapture(0)
            # self.cap = cv2.VideoCapture(
            #     'http://192.168.1.6:8080/?action=stream')
            self.load_known_people_info()
            self.sum_unknown = 0
            self.sum_known = {}
            for peo in self.namelist:
                self.sum_known[peo] = 0
            self.timer_camera.start(10)
            self.ismot = True
        else:
            QMessageBox.information(self, "监控中", "无需重复打开。", QMessageBox.Yes)

    def stop_monitor_fun(self):
        if self.ismot:
            self.timer_camera.stop()
            if self.cap:
                self.cap.release()
                self.ismot = False
            p = QtGui.QPixmap()
            p.load('219.jpg')
            self.setinitimage(p)
        else:
            QMessageBox.information(self, "监控未开启", "无需关闭。", QMessageBox.Yes)

    def re_init_people_info(self):
        print("init peopel info......")
        infopath = "knowninfo/"
        for filename in os.listdir(infopath):
            print("del people info:", filename)
            os.remove(infopath + filename)
        knownpath = "known/"
        for filename in os.listdir(knownpath):
            people = load_image_file(knownpath + filename)
            peopleinfo = face_encodings(people)[0]
            f = open(infopath + filename[:-4], 'wb')
            print("save people info:", filename[:-4])
            peopleinfo.tofile(f)
            f.close()
        print("people info init finished")
        QMessageBox.information(
            self, "人脸信息库", "数据库初始化成功,请停止监控，重新打开以使用最新信息。", QMessageBox.Yes)

    def see_info_fun(self):
        pass

    def load_known_people_info(self):
        self.namelist = []
        self.infolists = []
        infopath = "knowninfo/"
        for filename in os.listdir(infopath):
            f = open(infopath + filename, 'rb')
            peopleinfo = np.fromfile(f)
            self.namelist.append(filename)
            self.infolists.append(peopleinfo)
            f.close()
        print("load people info finish")

    def repaintframe(self, frame, imgface_locations, face_names):
        for (top, right, bottom, left), name in zip(imgface_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (255, 0, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, 'n:' + name, (left + 6, bottom - 6),
                        font, 1.0, (0, 0, 255), 1)

    def show_pic(self):
        if not self.isprocess:
            self.isprocess = True
            ret, frame = self.cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            imgface_locations = face_locations(small_frame)
            imgface_encodings = face_encodings(small_frame, imgface_locations)
            face_names = []
            for face_encoding in imgface_encodings:
                matches = compare_faces(self.infolists, face_encoding, 0.01)
                name = "unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.namelist[first_match_index]
                    self.sum_known[name] += 1
                    self.sum_unknown = 0
                    if self.sum_known[name] == 10:
                        # savepic = SaveGuestProcess(frame, name)
                        # savepic.start()
                        print(name)
                        for peo in self.namelist:
                            self.sum_known[peo] = 0
                else:
                    self.sum_unknown += 1
                    if self.sum_unknown == 10:
                        # savewar = SaveWarningProcess(frame)
                        # savewar.start()
                        self.sum_unknown = 0
                        for peo in self.namelist:
                            self.sum_known[peo] = 0
                face_names.append(name)
            if face_names:
                # 有人脸时重绘该帧显示名字
                self.repaintframe(frame, imgface_locations, face_names)
            # 显示该帧
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(
                show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.setimage(QPixmap.fromImage(showImage))
            if self.issave:
                saveshot = SaveshotProcess(frame)
                saveshot.start()
                self.issave = False
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('')
            self.isprocess = False

    def setimage(self, p):
        self.setinitimage(p)


class SaveshotProcess(MyWindow, threading.Thread):

    def __init__(self, frame):
        super().__init__()
        threading.Thread.__init__(self)
        self.frame = frame

    def run(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        filename = str(nowTime) + ".jpg"
        cv2.imwrite("result/shotpic/" + filename, self.frame)
        QMessageBox.information(self, "抓拍", "图片保存成功。", QMessageBox.Yes)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/app.png'))
    myshow = MyWindow()
    rce = record_frame()
    myshow.see_info.clicked.connect(rce.show_w2)
    myshow.show()
    app.exec_()
