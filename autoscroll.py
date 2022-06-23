#!/home/kusti420/Downloads/git/linux-autoscroll/.autoscroll/bin/python3

from pynput.mouse import Button, Controller, Listener
from threading import Event, Thread
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPixmap
from pathlib import Path
import sys
import pyXCursor
import tkinter as tk
from tkinter import ttk
import os
import hashlib

CURSOR_REFRENCE_IMAGE = "hand_cursor_refrence.png"
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class CursorInfo():
    def __init__(self) -> None:
        self.cursor_refrence_image_exists = CURSOR_REFRENCE_IMAGE in os.listdir(os.path.dirname(os.path.realpath(__file__)))
        self.cursor = pyXCursor.Xcursor()
        self.imgarray = self.cursor.getCursorImageArrayFast()
        self.root = None
        self.sense()

    def sense(self) -> None:
        self.imgarray = self.cursor.getCursorImageArrayFast()
        if not self.cursor_refrence_image_exists:
            self.root = tk.Tk()
            ttk.Button(self.root, text = "Click here to calibrate.\nKeep your cursor still on this button.",\
                width = 40, command = self.save_cursor_image, cursor = "hand1").pack(padx = 50, pady = 50)
            self.root.mainloop()

    def save_cursor_image(self, filename = CURSOR_REFRENCE_IMAGE) -> None:
        if not self.cursor_refrence_image_exists and filename == CURSOR_REFRENCE_IMAGE or filename != CURSOR_REFRENCE_IMAGE:
            # print(f"saving '{filename}' to '{os.getcwd()}'")
            self.cursor.saveImage(self.imgarray, filename)
            # print("saved")
            if filename == CURSOR_REFRENCE_IMAGE:
                self.cursor_refrence_image_exists = True
                self.root.destroy()

    def is_hand_cursor(self) -> bool:
        with open("hand_cursor_refrence.png", "rb") as f:
            cursor_image_hash = hashlib.md5(f.read()).hexdigest()
            f.close()
        with open("cursor_image.png", "rb") as f:
            cursor_image_hash_2 = hashlib.md5(f.read()).hexdigest()
            f.close()
        if cursor_image_hash != cursor_image_hash_2:
            print("cursor image hash mismatch")
            return False
        else:
            print("cursor image hash match")
            return True

cursorInfo = CursorInfo()

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
        cursorInfo.sense()
        cursorInfo.save_cursor_image("cursor_image.png")
        isHand = cursorInfo.is_hand_cursor()
        if button == self.BUTTON_START and pressed and not self.scroll_mode.is_set() and not isHand:
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
