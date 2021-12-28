from pynput.mouse import Button, Controller, Listener
from threading import Event
from time import sleep

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
        
        self.mouse = Controller()
        self.scroll_mode = Event()
        self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()
        
    def on_move(self, x, y):
        if self.scroll_mode.is_set():
            delta = self.pos[1] - y
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
            self.pos = (x, y)
            self.direction = 0
            self.interval = 0.5
            self.scroll_mode.set()
        elif button == self.BUTTON_STOP and pressed and self.scroll_mode.is_set():
            self.scroll_mode.clear()
    
    def start(self):
        while True:
            self.scroll_mode.wait()
            sleep(self.interval)
            self.mouse.scroll(0, self.direction)

autoscroll = Autoscroll()
autoscroll.start()