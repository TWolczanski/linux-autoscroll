from pynput.mouse import Button, Controller, Listener
from threading import Event, Thread
from time import sleep
from functools import partial
from queue import Queue
import subprocess


class Autoscroll:
    def __init__(self):
        # modify this to adjust the speed of scrolling
        self.DELAY = 5
        # modify this to change the button used for entering the scroll mode
        self.BUTTON_START = Button.middle
        # modify this to change the button used for exiting the scroll mode
        self.BUTTON_STOP = Button.middle
        # modify this to change the size (in px) of the area below and above the starting point where scrolling is paused
        self.DEAD_AREA = 30
        # modify this to change the time you have to hold BUTTON_START for in order to enter the scroll mode
        self.TRIGGER_DELAY = 0
        # set this to True if you want the clipboard to be cleared before entering the scroll mode
        # applicable only if you are using Button.middle for BUTTON_START or BUTTON_STOP
        # requires xsel
        self.CLEAR_CLIPBOARD = False
        # set this to True if you want to autoscroll only while BUTTON_START is held down
        self.HOLD_MODE = False

        self.mouse = Controller()
        self.scroll_mode = Event()
        self.queue = Queue()
        self.cancelled = Event()
        self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
        self.consumer = Thread(target=self.consume)

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
            self.queue.put(partial(self.enter_scroll_mode, x, y))
            self.started = True
        elif button == self.BUTTON_START and not pressed and self.started:
            self.cancelled.set()
            self.started = False
            if self.HOLD_MODE:
                self.queue.put(partial(self.exit_scroll_mode))
        elif button == self.BUTTON_STOP and not pressed and self.scroll_mode.is_set():
            self.queue.put(partial(self.exit_scroll_mode))

    def enter_scroll_mode(self, x, y):
        if self.CLEAR_CLIPBOARD:
            subprocess.run(["xsel", "-c"])
        self.pos = (x, y)
        self.direction = 0
        self.interval = 0.5
        self.scroll_mode.set()

    def exit_scroll_mode(self):
        self.scroll_mode.clear()

    def consume(self):
        while True:
            f = self.queue.get(block=True)
            if f.func == self.enter_scroll_mode:
                self.cancelled.clear()
                self.cancelled.wait(self.TRIGGER_DELAY)
                if not self.cancelled.is_set():
                    f()
            elif f.func == self.exit_scroll_mode:
                f()

    def start(self):
        self.consumer.start()
        self.listener.start()
        while True:
            self.scroll_mode.wait()
            sleep(self.interval)
            self.mouse.scroll(0, self.direction)


autoscroll = Autoscroll()
autoscroll.start()