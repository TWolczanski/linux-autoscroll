from pynput.mouse import Button, Controller, Listener
from threading import Event
import time

def on_move(x, y):
    global pos, scroll_mode, direction, delay
    if scroll_mode.is_set():
        delta = pos[1] - y
        if delta > 0:
            direction = 1
        elif delta < 0:
            direction = -1
        else:
            direction = 0
        delay = 2 / (abs(delta) + 1)

def on_click(x, y, button, pressed):
    global pos, scroll_mode, direction, delay, end
    if button == Button.right:
        end = True
        scroll_mode.set()
        return False
    elif button == Button.middle and pressed:
        if scroll_mode.is_set():
            scroll_mode.clear()
        else:
            pos = (x, y)
            direction = 0
            delay = 0
            scroll_mode.set()
        
def autoscroll():
    global mouse, scroll_mode, direction, delay, end
    while not end:
        scroll_mode.wait()
        while scroll_mode.is_set() and not end:
            time.sleep(delay)
            mouse.scroll(0, direction)

mouse = Controller()
scroll_mode = Event()
listener = Listener(on_move = on_move, on_click = on_click)
pos = mouse.position
direction = 0
delay = 0
end = False

listener.start()
autoscroll()