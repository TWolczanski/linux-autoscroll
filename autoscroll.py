import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pynput.mouse import Button, Controller, Listener
from threading import Event
import time

xpos,ypos = Controller().position
crosssizepx=30

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer

from tkinter import Tk
import subprocess

class QMouseListener(QObject):
    mouse_moved = pyqtSignal(int, int)
    mouse_clicked = pyqtSignal(int, int, Button, bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.listener = Listener(on_move=self.mouse_moved.emit, on_click=self.mouse_clicked.emit)

    def start(self):
        self.listener.start()

class Autoscrollsymbol(QtWidgets.QWidget):
    def __init__(self, parent=None, windowSize=0, penWidth=0):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput | QtCore.Qt.Tool)
        self.setStyleSheet("background:transparent")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(xpos, ypos, 50, 50)
        self.pen = QtGui.QPen(QtGui.QColor(0,255,0,255))
        self.pen.setWidth(penWidth)
        self.mouse_listener = QMouseListener(self)
        self.mouse_listener.mouse_moved.connect(self.on_move)
        self.mouse_listener.mouse_clicked.connect(self.on_click)
        self.mouse_listener.start()
        self.scroll_mode = 0
        self.mouse = Controller()
        self.pos = self.mouse.position
        self.direction = 0

        # modify this to adjust the speed of scrolling
        self.DELAY = 3000
        # modify this to change the button used for using scroll mode
        self.BUTTON_Scroll = Button.middle
        # modify this to change the size (in px) of the area below and above the starting point where the scrolling is paused
        self.DEAD_AREA = 20

        #Trigger Delay 250ms to avoid instant changes
        self.Triggerdelay = 0.25
        self.Timestart = 0
        self.Timeend = 0
        self.Timedelta = 0

        self.autoscroll()

    def on_move(self, x, y):
        if self.scroll_mode:
            delta = self.pos[1] - y
            if abs(delta) <= self.DEAD_AREA:
                self.direction = 0
            elif delta > 0:
                self.direction = 1
            elif delta < 0:
                self.direction = -1
            if abs(delta) <= self.DEAD_AREA:
                self.timer.setInterval(500)
            else:
                self.timer.setInterval(int(self.DELAY / (abs(delta) - self.DEAD_AREA)))
        if not self.scroll_mode:
            self.move(x -int(crosssizepx/2),y -int(crosssizepx/2))

    def clearclip(self):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append('')
        r.update()
        r.destroy()
        subprocess.run(["xsel","-c"])

    def on_click(self, x, y, button, pressed):
        if button == self.BUTTON_Scroll and pressed and not self.scroll_mode:
            self.setWindowOpacity(1.0)
            self.pos = (x, y)
            self.direction = 0
            self.timer.setInterval(100)
            self.scroll_mode = 1
            self.timer.start()
            self.Timestart = time.time()
        elif button == self.BUTTON_Scroll and not pressed and self.scroll_mode:
            self.Timeend = time.time()
            self.Timedelta = self.Timeend - self.Timestart
            if self.Timedelta>self.Triggerdelay:
                self.scroll_mode = 0
                self.timer.stop()
                self.setWindowOpacity(0.0)
        elif (button == self.BUTTON_Scroll or button==Button.left) and pressed and self.scroll_mode:
            self.scroll_mode = 0
            self.timer.stop()
            self.setWindowOpacity(0.0)
        
        if (button == Button.middle) and pressed:
            self.clearclip()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtCore.Qt.green, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        #painter.setPen(self.pen)
        painter.drawEllipse(0, 0, (crosssizepx), (crosssizepx))
        painter.drawLine(0, int(crosssizepx/2), crosssizepx, int(crosssizepx/2))#-
        painter.drawLine(int(crosssizepx/2), 0, int(crosssizepx/2), crosssizepx)#|
        self.setWindowOpacity(0.0)
        
    def scrolldown(self):
        self.mouse.scroll(0, self.direction)

    def autoscroll(self):
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.scrolldown)
        self.timer.start()

    def mouselistener(self):
        self.listener=Listener(on_move=self.on_move)
        self.listener.start()

app = QtWidgets.QApplication(sys.argv)
widget = Autoscrollsymbol(windowSize=1, penWidth=10)
widget.show()
sys.exit(app.exec_())
