from pynput.mouse import Button, Controller, Listener
from threading import Event, Thread
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPixmap
from pathlib import Path
import sys

class AutoscrollIconSvg(QSvgWidget):
    scroll_mode_entered = pyqtSignal()
    scroll_mode_exited = pyqtSignal()
    
    def __init__(self, path, size):
        super().__init__(path)
        self.size = size
        self.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.resize(self.size, self.size)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.scroll_mode_entered.connect(self.show)
        self.scroll_mode_exited.connect(self.close)
    
    def show(self):
        x = self.pos[0] - self.size // 2
        y = self.pos[1] - self.size // 2
        self.move(x, y)
        super().show()

class AutoscrollIconRaster(QLabel):
    scroll_mode_entered = pyqtSignal()
    scroll_mode_exited = pyqtSignal()
    
    def __init__(self, path, size):
        super().__init__()
        self.size = size
        self.resize(self.size, self.size)
        self.img = QPixmap(path).scaled(self.size, self.size, Qt.KeepAspectRatio)
        self.setPixmap(self.img)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.scroll_mode_entered.connect(self.show)
        self.scroll_mode_exited.connect(self.close)
        
    def show(self):
        x = self.pos[0] - self.size // 2
        y = self.pos[1] - self.size // 2
        self.move(x, y)
        super().show()

class Autoscroll():
    def __init__(self):
        # modify this to adjust the speed of scrolling
        self.DELAY = 5
        # modify this to change the button used for entering the scroll mode
        self.BUTTON_START = Button.middle
        # modify this to change the button used for exiting the scroll mode
        self.BUTTON_STOP = Button.middle
        # modify this to change the size (in px) of the area below and above the starting point where scrolling is paused
        self.DEAD_AREA = 30
        # modify this to change the scroll mode icon
        # supported formats: svg, png, jpg, jpeg, gif, bmp, pbm, pgm, ppm, xbm, xpm
        # the path MUST be absolute
        self.ICON_PATH = str(Path(__file__).parent.resolve()) + "/icon.svg"
        # modify this to change the size (in px) of the icon
        # note that only svg images can be resized without loss of quality
        self.ICON_SIZE = 30
        
        if self.ICON_PATH[-4:] == ".svg":
            self.icon = AutoscrollIconSvg(self.ICON_PATH, self.ICON_SIZE)
        else:
            self.icon = AutoscrollIconRaster(self.ICON_PATH, self.ICON_SIZE)
        
        self.mouse = Controller()
        self.scroll_mode = Event()
        self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()
        self.looper = Thread(target=self.loop)
        self.looper.start()
        
    def on_move(self, x, y):
        if self.scroll_mode.is_set():
            delta = self.icon.pos[1] - y
            if abs(delta) <= self.DEAD_AREA:
                self.direction = 0
            elif delta > 0:
                self.direction = 1
            elif delta < 0:
                self.direction = -1
            if abs(delta) <= self.DEAD_AREA + self.DELAY * 2:
                self.interval = 0.5
            else:
                self.interval = self.DELAY / (abs(delta) - self.DEAD_AREA)

    def on_click(self, x, y, button, pressed):
        if button == self.BUTTON_START and pressed and not self.scroll_mode.is_set():
            self.icon.pos = (x, y)
            self.direction = 0
            self.interval = 0.5
            self.scroll_mode.set()
            self.icon.scroll_mode_entered.emit()
        elif button == self.BUTTON_STOP and pressed and self.scroll_mode.is_set():
            self.scroll_mode.clear()
            self.icon.scroll_mode_exited.emit()
    
    def loop(self):
        while True:
            self.scroll_mode.wait()
            sleep(self.interval)
            self.mouse.scroll(0, self.direction)

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
autoscroll = Autoscroll()
sys.exit(app.exec())
