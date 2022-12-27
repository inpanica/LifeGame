import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QPoint, QTimer
import sys


class MainWindow(QMainWindow):
    rectList = []

    def __init__(self):
        super().__init__()
        uic.loadUi('win.ui', self)
        self.masterTimer = QTimer()
        self.masterTimer.timeout.connect(self.lifeTick)

        self.btn_pos_anim = QPropertyAnimation(self.play_button, b'pos')
        self.btn_size_anim = QPropertyAnimation(self.play_button, b'size')

        self.btn_pos_anim1 = QPropertyAnimation(self.one_step_button, b'pos')
        self.btn_size_anim1 = QPropertyAnimation(self.one_step_button, b'size')

        self.btn_pos_anim2 = QPropertyAnimation(self.clean_button, b'pos')
        self.btn_size_anim2 = QPropertyAnimation(self.clean_button, b'size')

        self.btn_pos_anim.setDuration(100)
        self.btn_size_anim.setDuration(100)
        self.btn_pos_anim1.setDuration(100)
        self.btn_size_anim1.setDuration(100)
        self.btn_pos_anim2.setDuration(100)
        self.btn_size_anim2.setDuration(100)

        self.play_button.clicked.connect(self.playProcess)
        self.one_step_button.clicked.connect(self.oneStep)
        self.clean_button.clicked.connect(self.clean)
        coords = [0, 80]
        for i in range(26):
            self.rectList.append([])
            for j in range(34):
                s = PyQt5.QtWidgets.QPushButton('', self)
                s.setGeometry(coords[0], coords[1], 20, 20)
                s.setAccessibleName('btn_' + str(i) + '_' + str(j))
                s.setStyleSheet('background: rgb(255, 255, 255);border-radius: 40')
                s.life = 0
                s.wd = 0
                s.wb = 0
                if i != 0 and j != 0 and i != 25 and j != 33:
                    s.clicked.connect(self.rectColorize)
                else:
                    s.setStyleSheet('background: rgb(122, 122, 122);border-radius: 40')
                self.rectList[-1].append(s)
                coords[0] += 20
            coords[1] += 20
            coords[0] = 0

    def rectColorize(self):
        button = self.sender()
        if button.styleSheet() == 'background: rgb(255, 255, 255);border-radius: 40':
            button.setStyleSheet('background: rgb(0, 0, 0);border-radius: 40')
            button.life = 1
        else:
            button.setStyleSheet('background: rgb(255, 255, 255);border-radius: 40')
            button.life = 0

    def playProcess(self):
        flag = self.play_button.text() == '>'
        if flag:
            self.play_button.setText('||')
            self.lifeTick()
            self.masterTimer.start(50)
        else:
            self.play_button.setText('>')
            self.masterTimer.stop()
        self.btn_size_anim.stop()
        self.btn_pos_anim.stop()

        self.btn_size_anim.setEasingCurve(QEasingCurve.SineCurve)
        self.btn_pos_anim.setEasingCurve(QEasingCurve.SineCurve)

        self.btn_pos_anim.setStartValue(QPoint(30, 10))
        self.btn_pos_anim.setEndValue(QPoint(35, 15))

        self.btn_size_anim.setStartValue(QSize(61, 61))
        self.btn_size_anim.setEndValue(QSize(51, 51))

        self.btn_pos_anim.start()
        self.btn_size_anim.start()

    def oneStep(self):
        self.btn_size_anim1.stop()
        self.btn_pos_anim1.stop()

        self.btn_size_anim1.setEasingCurve(QEasingCurve.SineCurve)
        self.btn_pos_anim1.setEasingCurve(QEasingCurve.SineCurve)

        self.btn_pos_anim1.setStartValue(QPoint(110, 10))
        self.btn_pos_anim1.setEndValue(QPoint(115, 15))

        self.btn_size_anim1.setStartValue(QSize(61, 61))
        self.btn_size_anim1.setEndValue(QSize(51, 51))

        self.btn_pos_anim1.start()
        self.btn_size_anim1.start()
        self.lifeTick()
    def clean(self):
        self.btn_size_anim2.stop()
        self.btn_pos_anim2.stop()

        self.btn_size_anim2.setEasingCurve(QEasingCurve.SineCurve)
        self.btn_pos_anim2.setEasingCurve(QEasingCurve.SineCurve)

        self.btn_pos_anim2.setStartValue(QPoint(190, 10))
        self.btn_pos_anim2.setEndValue(QPoint(195, 15))

        self.btn_size_anim2.setStartValue(QSize(61, 61))
        self.btn_size_anim2.setEndValue(QSize(51, 51))

        self.btn_pos_anim2.start()
        self.btn_size_anim2.start()
        for y in range(1, len(self.rectList) - 1):
            for x in range(1, len(self.rectList[y]) - 1):
                self.rectList[y][x].life = 0
                self.rectList[y][x].wd = 0
                self.rectList[y][x].wb = 0
                self.rectList[y][x].setStyleSheet('background: rgb(255, 255, 255);border-radius: 40')

    def lifeTick(self):
        for y in range(1, len(self.rectList) - 1):
            for x in range(1, len(self.rectList[y]) - 1):
                self.rectDeath(x, y)
                self.rectBurn(x, y)
        for y in range(1, len(self.rectList) - 1):
            for x in range(1, len(self.rectList[y]) - 1):
                if self.rectList[y][x].wb == 1:
                    self.rectList[y][x].setStyleSheet('background: rgb(0, 0, 0);border-radius: 40')
                    self.rectList[y][x].life = 1
                    self.rectList[y][x].wb = 0
        for y in range(1, len(self.rectList) - 1):
            for x in range(1, len(self.rectList[y]) - 1):
                if self.rectList[y][x].wd == 1:
                    self.rectList[y][x].setStyleSheet('background: rgb(255, 255, 255);border-radius: 40')
                    self.rectList[y][x].life = 0
                    self.rectList[y][x].wd = 0

    def rectBurn(self, x, y):
        count = 0
        if not self.rectList[y][x].life:
            if self.rectList[y - 1][x - 1].life:
                count += 1
            if self.rectList[y - 1][x].life:
                count += 1
            if self.rectList[y - 1][x + 1].life:
                count += 1
            if self.rectList[y][x - 1].life:
                count += 1
            if self.rectList[y][x + 1].life:
                count += 1
            if self.rectList[y + 1][x - 1].life:
                count += 1
            if self.rectList[y + 1][x].life:
                count += 1
            if self.rectList[y + 1][x+1].life:
                count += 1
            if count == 3:
                self.rectList[y][x].wb = 1

    def rectDeath(self, x, y):
        count = 0
        if self.rectList[y][x].life:
            if self.rectList[y - 1][x - 1].life:
                count += 1
            if self.rectList[y - 1][x].life:
                count += 1
            if self.rectList[y - 1][x + 1].life:
                count += 1
            if self.rectList[y][x - 1].life:
                count += 1
            if self.rectList[y][x + 1].life:
                count += 1
            if self.rectList[y + 1][x - 1].life:
                count += 1
            if self.rectList[y + 1][x].life:
                count += 1
            if self.rectList[y + 1][x+1].life:
                count += 1
            if count > 3 or count < 2:
                self.rectList[y][x].wd = 1


def application_():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


application_()
